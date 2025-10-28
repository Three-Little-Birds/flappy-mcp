"""python-sdk MCP integration helper for Flappy."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .core import execute_flappy
from .models import FlappyRequest, FlappyResponse


def build_tool(app: FastMCP) -> None:
    """Register the Flappy tool on the given MCP instance."""

    @app.tool()
    def run(request: FlappyRequest) -> FlappyResponse:  # type: ignore[valid-type]
        return execute_flappy(request)


__all__ = ["build_tool"]
