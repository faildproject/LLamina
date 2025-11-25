# app/main.py
from __future__ import annotations

from fastapi import FastAPI

from .api import lmstudio_v0
from .api import openai_v1


app = FastAPI(
    title="LLamina Gateway",
    version="0.1.0",
)

# LM Studio REST API /api/v0/...
app.include_router(lmstudio_v0.router)

# LM Studio REST API /api/v1/...
app.include_router(openai_v1.router)


# # app/main.py
# from __future__ import annotations

# import os

# import json
# from fastapi import FastAPI, Request, HTTPException
# from fastapi.responses import Response
# import httpx
# from dotenv import load_dotenv

# # .env laden
# load_dotenv()

# BACKEND_URL = os.getenv("BACKEND_URL")

# if not BACKEND_URL:
#     raise RuntimeError("BACKEND_URL ist nicht gesetzt (siehe .env)")

# app = FastAPI(title="LLamina Minimal Proxy")


# def build_target_url(request: Request) -> str:
#     """
#     Baut die Ziel-URL:
#     z.B. /v1/chat/completions -> BACKEND_URL + gleicher Pfad
#     """
#     return f"{BACKEND_URL}{request.url.path}"


# @app.post("/v1/chat/completions")
# async def proxy_chat_completions(request: Request) -> Response:
#     # Original-Body 1:1 übernehmen
#     body = await request.body()

#     # Header übernehmen, aber `host` entfernen
#     headers = dict(request.headers)
#     headers.pop("host", None)

#     target_url = build_target_url(request)

#     async with httpx.AsyncClient(timeout=None) as client:
#         try:
#             backend_response = await client.post(
#                 target_url,
#                 content=body,
#                 headers=headers,
#             )
#         except httpx.RequestError:
#             # Backend ist nicht erreichbar
#             raise HTTPException(
#                 status_code=503,
#                 detail="Backend nicht erreichbar",
#             )

#     # Antwort 1:1 zurückgeben (Status + Body), Header minimal weiterreichen
#     response_headers = {
#         k: v
#         for k, v in backend_response.headers.items()
#         if k.lower() not in {"content-length", "transfer-encoding", "connection"}
#     }

#     # >>> HIER: usage auslesen, wenn vorhanden
#     prompt_tokens = completion_tokens = total_tokens = None

#     # nur versuchen zu parsen, wenn Content-Type nach JSON aussieht
#     content_type = backend_response.headers.get("content-type", "")
#     if "application/json" in content_type:
#         try:
#             data = backend_response.json()
#         except ValueError:
#             data = None

#         if isinstance(data, dict) and "usage" in data:
#             usage = data["usage"] or {}
#             prompt_tokens = usage.get("prompt_tokens")
#             completion_tokens = usage.get("completion_tokens")
#             total_tokens = usage.get("total_tokens")

#             print(
#                 f"LMStudio usage: prompt={prompt_tokens}, completion={completion_tokens}, total={total_tokens}"
#             )

#     return Response(
#         content=backend_response.content,
#         status_code=backend_response.status_code,
#         headers=response_headers,
#         media_type=backend_response.headers.get("content-type"),
#     )
