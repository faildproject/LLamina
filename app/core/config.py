import yaml
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, List, Dict


class Server(BaseModel):
    name: str
    host: str
    port: int
    meta: Dict = {}


class Defaults(BaseModel):
    timeout_seconds: int = 30
    max_retries: int = 2


class Config(BaseModel):
    servers: List[Server]
    defaults: Defaults = Defaults()


def load_config(path: str | Path = "config.yaml") -> Config:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return Config(**raw)


config = load_config()

for server in config.servers:
    print(server.name, server.host, server.port, server.meta.get("gpu"))
