from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_BASE_URL = "https://api.openai.com/v1/sora"
CONFIG_DIR = Path(os.environ.get("SORA_CONFIG_DIR", Path.home() / ".config" / "sora_tool"))
CONFIG_FILE = CONFIG_DIR / "config.json"


@dataclass
class Config:
    api_key: str | None = None
    base_url: str = DEFAULT_BASE_URL
    timeout_s: int = 60

    def masked_api_key(self) -> str:
        if not self.api_key:
            return "(not set)"
        visible = self.api_key[-4:]
        return f"***{visible}"


def load_config() -> Config:
    data: dict[str, Any] = {}
    if CONFIG_FILE.exists():
        data = json.loads(CONFIG_FILE.read_text())

    api_key = os.environ.get("SORA_API_KEY", data.get("api_key"))
    base_url = os.environ.get("SORA_BASE_URL", data.get("base_url", DEFAULT_BASE_URL))
    timeout_s = int(os.environ.get("SORA_TIMEOUT", data.get("timeout_s", 60)))

    return Config(api_key=api_key, base_url=base_url, timeout_s=timeout_s)


def save_config(config: Config) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "api_key": config.api_key,
        "base_url": config.base_url,
        "timeout_s": config.timeout_s,
    }
    CONFIG_FILE.write_text(json.dumps(payload, indent=2))
