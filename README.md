# flappy-mcp - Bio-inspired flapping dynamics for MCP agents

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB.svg" alt="Python 3.10 or newer"></a>
  <a href="https://github.com/Three-Little-Birds/flappy-mcp/actions/workflows/ci.yml"><img src="https://github.com/Three-Little-Birds/flappy-mcp/actions/workflows/ci.yml/badge.svg" alt="CI status"></a>
  <img src="https://img.shields.io/badge/MCP-tooling-blueviolet.svg" alt="MCP tooling badge">
</p>

> **TL;DR**: Control the Purdue BioRobotics "Flappy" simulator through MCP so agents can explore flapping-wing dynamics and log trajectories without headless GUIs.

<a href="https://glama.ai/mcp/servers/@yevheniikravchuk/flappy-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@yevheniikravchuk/flappy-mcp/badge" alt="Flappy Server MCP server" />
</a>

## Table of contents

1. [What it provides](#what-it-provides)
2. [Quickstart](#quickstart)
3. [Run as a service](#run-as-a-service)
4. [Agent playbook](#agent-playbook)
5. [Stretch ideas](#stretch-ideas)
6. [Install & maintenance](#install--maintenance)
7. [Contributing](#contributing)

## What it provides

| Scenario | Value |
|----------|-------|
| Flappy CLI automation | Drive the Purdue BioRobotics [Flappy simulator](https://engineering.purdue.edu/SMARTLab/research/flappingflight) from Python or MCP without bespoke shell scripts. |
| Trajectory logging | Collect pose, velocity, and energy histories as JSON for reinforcement learning or system-identification studies. |
| MCP transport | Expose the CLI via STDIO/HTTP so ToolHive and other clients can batch missions or plug results into `ctrltest-mcp`.

## Quickstart

### 1. Install the wrapper

```bash
uv pip install "git+https://github.com/Three-Little-Birds/flappy-mcp.git"
```

Build the CLI from the Purdue SMARTLab Flappy sources (partners receive access on request—see the [research page](https://engineering.purdue.edu/SMARTLab/research/flappingflight) for contact details) and point this wrapper to the resulting `flappy_cli` binary:

```bash
export FLAPPY_BIN=/path/to/flappy_cli
```

### 2. Simulate a trajectory

```python
from flappy_mcp import FlappyRequest, execute_flappy

request = FlappyRequest(
    scenario=None,
    fallback={"duration_s": 5.0, "timestep_s": 0.01},
)
response = execute_flappy(request)
print("Trajectory points:", len(response.trajectory))
print("Source:", response.source)              # "generated" or path to CLI JSON
print("First sample:", response.trajectory[0].model_dump())
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

### ToolHive smoke test

Requires the Flappy CLI executable:

```bash
export FLAPPY_BIN=/path/to/flappy_cli
uvx --with 'mcp==1.20.0' python scripts/integration/run_flappy.py
```

## Agent playbook

- **Policy tuning** - sweep control inputs and feed trajectories into reinforcement-learning pipelines.
- **Sensor synthesis** - generate inertial traces for testing perception/estimation stacks.
- **Energy studies** - derive energy usage from the returned stroke kinematics or augment the scenario before launching the CLI.

## Stretch ideas

1. Couple with `diffsph` gradients to evaluate loads alongside motion.
2. Feed trajectories into `ctrltest-mcp` for closed-loop evaluation.
3. Build deck.gl overlays of position data for mission rehearsal.

## Install & maintenance

- **Runtime install:** follow the [Quickstart](#quickstart) `uv pip install "git+https://github.com/Three-Little-Birds/flappy-mcp.git"` step on machines that need the MCP wrapper.
- **Validate dependencies:** set `FLAPPY_BIN` to the compiled `flappy_cli` path, run `$FLAPPY_BIN --help`, and confirm the simulator launches without interactive prompts.
- **Runtime expectations:** CLI runs block until completion and may take several minutes for long scenarios; the built-in sinusoidal fallback returns instantly. All trajectories are returned as lists of `{t, angle}` samples in SI units so downstream controllers can replay them verbatim.
- **Keep fixtures in sync:** document any generated trajectories or fixture updates so downstream services can replay them reliably.

## Contributing

1. `uv pip install --system -e .[dev]`
2. Run `uv run ruff check .` and `uv run pytest`
3. Submit sample trajectories or metrics with your PR so reviewers can validate quickly.

MIT license - see [LICENSE](LICENSE).