# app/core/config.py
from __future__ import annotations

import os
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

_settings_cache: Settings | None = None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    backend_url: AnyHttpUrl  # z.B. http://localhost:1234

    @property
    def lmstudio_base_url(self) -> str:
        # als convenience, falls du später mehrere Backends hast
        return str(self.backend_url)


def get_settings() -> Settings:
    # simples Singleton
    global _settings_cache
    try:
        return _settings_cache
    except NameError:
        _settings_cache = Settings(_env_file=os.getenv("ENV_FILE", ".env"))
        return _settings_cache
