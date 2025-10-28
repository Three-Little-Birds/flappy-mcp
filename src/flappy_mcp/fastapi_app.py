"""FastAPI application for the Flappy MCP service."""

from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException

from .core import FLAPPY_BIN, execute_flappy
from .models import FlappyRequest, FlappyResponse


def create_app() -> FastAPI:
    app = FastAPI(
        title="Flappy MCP Service",
        version="0.1.0",
        description="Run Flappy or generate a sinusoidal fallback trajectory.",
    )

    @app.post("/run", response_model=FlappyResponse)
    def run_flappy(request: FlappyRequest) -> FlappyResponse:
        try:
            return execute_flappy(request)
        except RuntimeError as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    @app.get("/health")
    def health() -> dict[str, str]:
        status = "available" if FLAPPY_BIN and os.path.exists(FLAPPY_BIN) else "stub"
        return {"status": status, "binary": FLAPPY_BIN}

    return app


app = create_app()


__all__ = ["create_app", "app"]
