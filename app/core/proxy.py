# app/core/proxy.py
from __future__ import annotations

from typing import Iterable, Mapping

import httpx
from fastapi import HTTPException, Request
from fastapi.responses import Response

from .config import load_config
from ..api.model_switcher import load_model_if_needed

configuration = load_config()
servers = configuration.servers
server = servers[1]


EXCLUDED_HEADERS = {"content-length", "transfer-encoding", "connection"}


def _filter_response_headers(headers: Mapping[str, str]) -> dict[str, str]:
    return {k: v for k, v in headers.items() if k.lower() not in EXCLUDED_HEADERS}


def get_client_id(request: Request):
    ip = request.client
    print(ip.host)  # type: ignore
    return ip


async def proxy_to_backend(
    request: Request,
) -> Response:
    """
    Leitet den Request 1:1 zum LM Studio Backend weiter
    und gibt die Antwort zurück.
    Path und Querystring bleiben unverändert.
    """

    # Ziel-URL: backend_base_url + path + query
    # Beispiel:
    #   Request:   /api/v0/models?foo=bar
    #   Backend:   http://localhost:1234/api/v0/models?foo=bar
    get_client_id(request)
    path_and_query = request.url.path
    if request.url.query:
        path_and_query += f"?{request.url.query}"

    base = server.host + ":" + str(server.port)
    target_url = f"{base}{path_and_query}"
    print(f"Request to: {target_url}")

    # Body & Headers übernehmen
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)

    try:
        request_json = await request.json()
    except Exception:
        request_json = {}

    model_name = request_json.get("model")
    if model_name:
        print(f"[Proxy] Requested model: {model_name}")
        success = load_model_if_needed(model_name, server.tool)
        if not success:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load model via control API: {model_name}",
            )

    async with httpx.AsyncClient(timeout=None) as client:
        try:
            backend_response = await client.request(
                method=request.method,
                url=target_url,
                content=body,
                headers=headers,
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Backend nicht erreichbar: {e}",
            )

    response_headers = _filter_response_headers(backend_response.headers)

    return Response(
        content=backend_response.content,
        status_code=backend_response.status_code,
        headers=response_headers,
        media_type=backend_response.headers.get("content-type"),
    )
