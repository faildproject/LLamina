import httpx

global _current_model
_current_model: str | None = None  # Cache
API_BASE = "http://localhost:8484"  # URL deiner Control-API


def load_model_if_needed(model_name: str, tool: str) -> bool:
    """
    Ruft die FastAPI-Control-API auf (/load),
    um das gewünschte Modell zu laden, falls es sich geändert hat.
    """

    print(f"cm:{_current_model} - rm:{model_name}")
    if not model_name:
        print("No model_name provided, skipping load.")
        return False

    # Wenn bereits geladen: nichts tun
    if _current_model == model_name:
        return True

    if tool == "ollama":
        return load_model_on_ollama(model_name)
    if tool == "lmstudio":
        return load_model_on_lmstudio(model_name)
    return False


def load_model_on_lmstudio(model_name: str) -> bool:
    try:
        resp = httpx.post(
            f"{API_BASE}/load",
            json={"model_path": model_name},
            timeout=60.0,
        )
        resp.raise_for_status()
    except httpx.HTTPError as e:
        print(f"Model load failed via API for '{model_name}': {e}")
        return False

    # Optional: Rückgabe der API loggen
    try:
        data = resp.json()
        print(f"Control-API response: {data}")
    except Exception:
        print("Control-API returned non-JSON or parse error")

    _current_model = model_name
    print(f"Model switched (via API) to: {model_name}")
    return True


def load_model_on_ollama(model_name: str) -> bool:
    try:
        resp = httpx.post(
            f"http://localhost:11434/api/generate",
            json={"model": model_name},
            timeout=60.0,
        )
        resp.raise_for_status()
    except httpx.HTTPError as e:
        print(f"Model load failed via API for '{model_name}': {e}")
        return False

    # Optional: Rückgabe der API loggen
    try:
        data = resp.json()
        print(f"Control-API response: {data}")
    except Exception:
        print("Control-API returned non-JSON or parse error")

    _current_model = model_name
    print(f"Model switched (via API) to: {model_name}")
    return True
