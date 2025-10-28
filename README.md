# flappy-mcp

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](pyproject.toml)
[![CI](https://github.com/yevheniikravchuk/flappy-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/yevheniikravchuk/flappy-mcp/actions/workflows/ci.yml)

Model Context Protocol (MCP) toolkit for the [Flappy](https://github.com/purdue-biorobotics/flappy) avian dynamics simulator. It exposes typed request models, CLI execution helpers, and python-sdk integration so agents can trigger Flappy runs or fall back to the built-in sinusoidal surrogate when the binary isn’t installed.

## Why you might want this

- **Exercise motion controllers** – generate trajectories without hand-wiring JSON configs every time you tweak gains.
- **Offer graceful degradation** – if `flappy_cli` isn’t deployed on a machine, the deterministic surrogate still returns a believable stroke trace for tests or demos.
- **Archive simulation context** – responses include the generated output path (CLI mode) or the synthetic trajectory so audit logs stay complete.

## Features

- Writes Flappy configuration JSON, invokes `flappy_cli`, and returns parsed trajectories.
- Includes a deterministic analytic fallback (sinusoidal stroke) when the binary is absent.
- FastAPI app factory and python-sdk helper for rapid MCP integration.
- Fully typed, MIT-licensed, and covered by tests.

## Installation

```bash
pip install "git+https://github.com/yevheniikravchuk/flappy-mcp.git"
```

## FastAPI usage

```python
from flappy_mcp.fastapi_app import create_app

app = create_app()
```

Run locally:

```bash
uv run uvicorn flappy_mcp.fastapi_app:create_app --factory --host 127.0.0.1 --port 8004
```

## python-sdk usage

```python
from mcp.server.fastmcp import FastMCP
from flappy_mcp.tool import build_tool

app = FastMCP("flappy-mcp", "Flappy dynamics simulator")
build_tool(app)

if __name__ == "__main__":
    app.run()
```

### Example STDIO request

```json
{
  "tool": "flappy-mcp.run",
  "arguments": {
    "scenario": {
      "simulation": {"duration_s": 2.0, "timestep_s": 0.02},
      "control": {"stroke_amplitude_rad": 0.3, "stroke_frequency_hz": 4.0}
    }
  }
}
```

## Environment variables

- `FLAPPY_BIN` (default `flappy_cli`) — set to the compiled Flappy executable.

## Local development

```bash
uv pip install --system -e .[dev]
uv run ruff check .
uv run pytest
```

Test cases illustrate both CLI and surrogate flows to guide readers who haven’t used Flappy before.

## License

MIT — see [LICENSE](LICENSE).
