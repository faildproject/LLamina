# app/api/openai_v1.py
from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from ..core.proxy import proxy_to_backend

router = APIRouter(prefix="/v1", tags=["openai-v1"])


@router.get("/models")
async def list_models_v1(
    request: Request,
):
    """
    Proxy für: GET /v1/models
    OpenAI-kompatibel, LM Studio hängt dahinter.
    """
    return await proxy_to_backend(request)


@router.post("/responses")
async def responses_v1(
    request: Request,
):
    """
    Proxy für: POST /v1/responses
    """
    return await proxy_to_backend(request)


@router.post("/chat/completions")
async def chat_completions_v1(
    request: Request,
):
    """
    Proxy für: POST /v1/chat/completions
    """
    return await proxy_to_backend(request)


@router.post("/embeddings")
async def embeddings_v1(
    request: Request,
):
    """
    Proxy für: POST /v1/embeddings
    """
    return await proxy_to_backend(request)


@router.post("/completions")
async def completions_v1(
    request: Request,
):
    """
    Proxy für: POST /v1/completions
    """
    return await proxy_to_backend(request)
