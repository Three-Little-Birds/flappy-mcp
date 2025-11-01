"""python-sdk MCP integration helper for Flappy."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .core import execute_flappy
from .models import FlappyRequest, FlappyResponse


def build_tool(app: FastMCP) -> None:
    """Register the Flappy tool on the given MCP instance."""

    @app.tool(
        name="flappy.simulate",
        description=(
            "Run the Flappy dynamics simulator for a mission profile. "
            "Provide wing morphology, control schedule, and duration. "
            "Returns pose histories, energy metrics, and solver provenance. "
            "Example: {\"scenario_id\":\"demo\",\"duration_s\":8.0}"
        ),
        meta={"version": "0.1.0", "categories": ["simulation", "dynamics"]},
    )
    def run(request: FlappyRequest) -> FlappyResponse:
        return execute_flappy(request)


__all__ = ["build_tool"]
