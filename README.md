# flappy-mcp - Bio-inspired flapping dynamics for MCP agents

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB.svg" alt="Python 3.10 or newer"></a>
  <a href="https://github.com/Three-Little-Birds/flappy-mcp/actions/workflows/ci.yml"><img src="https://github.com/Three-Little-Birds/flappy-mcp/actions/workflows/ci.yml/badge.svg" alt="CI status"></a>
  <img src="https://img.shields.io/badge/status-incubating-ff9800.svg" alt="Project status: incubating">
  <img src="https://img.shields.io/badge/MCP-tooling-blueviolet.svg" alt="MCP tooling badge">
</p>

> **TL;DR**: Control the Purdue BioRobotics "Flappy" simulator through MCP so agents can explore flapping-wing dynamics and log trajectories without headless GUIs.

## Table of contents

1. [Why agents love it](#why-agents-love-it)
2. [Quickstart](#quickstart)
3. [Run as a service](#run-as-a-service)
4. [Agent playbook](#agent-playbook)
5. [Stretch ideas](#stretch-ideas)
6. [Accessibility & upkeep](#accessibility--upkeep)
7. [Contributing](#contributing)

## Why agents love it

| Persona | Immediate value | Longer-term payoff |
|---------|-----------------|--------------------|
| **New users** | Run a flapping trajectory in two commands, retrieving position/velocity/attitude streams. | Provides learning-friendly surrogate dynamics without needing hardware-in-the-loop. |
| **Experienced teams** | Wrap the simulator in MCP transports (REST/STDIO) for automated sweeps and policy evaluation. | Deterministic JSON outputs (`trajectory.json`, `metrics.json`) integrate with `ctrltest-mcp` and the CEE pipeline.

## Quickstart

### 1. Install the wrapper

```bash
uv pip install "git+https://github.com/Three-Little-Birds/flappy-mcp.git"
```

Ensure the Flappy CLI is present; if not:

```bash
export FLAPPY_BIN=/path/to/flappy_cli
```

### 2. Simulate a trajectory

```python
from flappy_mcp import FlappyRequest, run_flappy

request = FlappyRequest(duration_s=5.0, timestep_s=0.01)
response = run_flappy(request)
print("Trajectory points:", len(response.trajectory))
```

## Run as a service

### CLI (STDIO transport)

```bash
uvx flappy-mcp  # runs the MCP over stdio
# or python -m flappy_mcp
```

Use `python -m flappy_mcp --describe` to inspect metadata without starting the server.

### FastAPI (REST)

```bash
uv run uvicorn flappy_mcp.fastapi_app:create_app --factory --port 8004
```

Invoke via the auto-generated docs at `http://127.0.0.1:8004/docs`.

### python-sdk tool (STDIO / MCP)

```python
from mcp.server.fastmcp import FastMCP
from flappy_mcp.tool import build_tool

mcp = FastMCP("flappy-mcp", "Flapping dynamics simulator")
build_tool(mcp)

if __name__ == "__main__":
    mcp.run()
```

Launch with `uv run mcp dev examples/flappy_tool.py` and wire in your agent.

## Agent playbook

- **Policy tuning** - sweep control inputs and feed trajectories into reinforcement-learning pipelines.
- **Sensor synthesis** - generate inertial traces for testing perception/estimation stacks.
- **Energy studies** - log `response.metrics` to correlate control patterns with consumption.

## Stretch ideas

1. Couple with `diffsph` gradients to evaluate loads alongside motion.
2. Feed trajectories into `ctrltest-mcp` for closed-loop evaluation.
3. Build deck.gl overlays of position data for mission rehearsal.

## Accessibility & upkeep

- Concise badges keep the hero block scannable while including descriptive alt text, following current README best practices.
- Tests mock the CLI: run `uv run pytest` before pushing changes.
- Keep `FLAPPY_BIN` aligned with upstream releases for consistent physics.

## Contributing

1. `uv pip install --system -e .[dev]`
2. Run `uv run ruff check .` and `uv run pytest`
3. Submit sample trajectories or metrics with your PR so reviewers can validate quickly.

MIT license - see [LICENSE](LICENSE).
