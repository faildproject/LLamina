# app/core/proxy.py
from __future__ import annotations

from typing import Iterable, Mapping

import httpx
from fastapi import HTTPException, Request
from fastapi.responses import Response


EXCLUDED_HEADERS = {"content-length", "transfer-encoding", "connection"}


def _filter_response_headers(headers: Mapping[str, str]) -> dict[str, str]:
    return {k: v for k, v in headers.items() if k.lower() not in EXCLUDED_HEADERS}


def get_client_id(request: Request):
    ip = request.client
    print(ip.host)  # type: ignore
    return ip


async def proxy_to_backend(
    request: Request,
    backend_base_url: str,
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

    base = backend_base_url.rstrip("/")
    target_url = f"{base}{path_and_query}"

    # Body & Headers übernehmen
    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)

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
