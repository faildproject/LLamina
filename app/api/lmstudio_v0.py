# app/api/lmstudio_v0.py
from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from ..core.config import get_settings, Settings
from ..core.proxy import proxy_to_backend

router = APIRouter(prefix="/api/v0", tags=["lmstudio-v0"])


@router.get("/models")
async def list_models(
    request: Request,
    settings: Settings = Depends(get_settings),
):
    return await proxy_to_backend(request, settings.lmstudio_base_url)


@router.get("/models/{model_id}")
async def get_model(
    model_id: str,
    request: Request,
    settings: Settings = Depends(get_settings),
):
    # path wird sowieso aus request.url.path genommen,
    # daher müssen wir model_id hier nicht extra verwenden.
    return await proxy_to_backend(request, settings.lmstudio_base_url)


@router.post("/chat/completions")
async def chat_completions_v0(
    request: Request,
    settings: Settings = Depends(get_settings),
):
    return await proxy_to_backend(request, settings.lmstudio_base_url)


@router.post("/completions")
async def completions_v0(
    request: Request,
    settings: Settings = Depends(get_settings),
):
    return await proxy_to_backend(request, settings.lmstudio_base_url)


@router.post("/embeddings")
async def embeddings_v0(
    request: Request,
    settings: Settings = Depends(get_settings),
):
    return await proxy_to_backend(request, settings.lmstudio_base_url)
