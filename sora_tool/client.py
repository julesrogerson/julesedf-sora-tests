from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib import request
from urllib.error import HTTPError

from sora_tool.config import Config


@dataclass
class ApiResponse:
    status: int
    payload: dict[str, Any]


class SoraClient:
    def __init__(self, config: Config) -> None:
        if not config.api_key:
            raise ValueError("API key is required. Run 'sora-tool configure --api-key ...' first.")
        self._config = config

    def create_video(self, prompt: str, duration_s: int | None = None, size: str | None = None) -> ApiResponse:
        payload: dict[str, Any] = {"prompt": prompt}
        if duration_s is not None:
            payload["duration"] = duration_s
        if size is not None:
            payload["size"] = size
        return self._post("/videos", payload)

    def export_draft(self, draft_id: str) -> ApiResponse:
        return self._get(f"/drafts/{draft_id}/export")

    def _get(self, path: str) -> ApiResponse:
        url = f"{self._config.base_url.rstrip('/')}{path}"
        req = request.Request(url, method="GET")
        req.add_header("Authorization", f"Bearer {self._config.api_key}")
        req.add_header("Content-Type", "application/json")

        try:
            with request.urlopen(req, timeout=self._config.timeout_s) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return ApiResponse(status=resp.status, payload=data)
        except HTTPError as exc:
            error_body = exc.read().decode("utf-8")
            raise RuntimeError(f"Request failed ({exc.code}): {error_body}") from exc

    def _post(self, path: str, payload: dict[str, Any]) -> ApiResponse:
        url = f"{self._config.base_url.rstrip('/')}{path}"
        body = json.dumps(payload).encode("utf-8")
        req = request.Request(url, data=body, method="POST")
        req.add_header("Authorization", f"Bearer {self._config.api_key}")
        req.add_header("Content-Type", "application/json")

        try:
            with request.urlopen(req, timeout=self._config.timeout_s) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return ApiResponse(status=resp.status, payload=data)
        except HTTPError as exc:
            error_body = exc.read().decode("utf-8")
            raise RuntimeError(f"Request failed ({exc.code}): {error_body}") from exc
