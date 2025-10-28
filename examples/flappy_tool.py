"""Example python-sdk tool for flappy-mcp."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from flappy_mcp.tool import build_tool

app = FastMCP("flappy-mcp", "Flappy dynamics simulator")
build_tool(app)


if __name__ == "__main__":
    app.run()
