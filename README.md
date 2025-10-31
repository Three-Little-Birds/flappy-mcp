# flappy-mcp · Learn Biobotics Simulation the Friendly Way

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](pyproject.toml)
[![CI](https://github.com/Three-Little-Birds/flappy-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/Three-Little-Birds/flappy-mcp/actions/workflows/ci.yml)

This project wraps the [Flappy](https://github.com/purdue-biorobotics/flappy) flapping-wing simulator so that newcomers—and MCP agents—can generate motion traces with a few lines of code. It also ships with a deterministic surrogate so laptop demos never block on the full simulator.

## What you will practice

- Installing `flappy_cli` and verifying a basic take-off simulation.
- Calling the MCP helper to run Flappy (or the surrogate) and inspect the resulting wing trajectories.
- Registering a python-sdk tool so an AI assistant can answer questions like “what is the wingtip amplitude at 7 Hz?”

## Set-up checklist

| Requirement | How to get it |
|-------------|---------------|
| `flappy_cli` binary | Build from source (instructions in the upstream README) or download a prebuilt release. |
| Python 3.10+ with `uv` | Used for installation and examples. |
| `numpy`/`matplotlib` (optional) | Helpful for plotting trajectories. |

Expose the binary if it lives outside `PATH`:

```bash
export FLAPPY_BIN=/path/to/flappy_cli
```

## Step 1 – Install the MCP wrapper

```bash
uv pip install "git+https://github.com/Three-Little-Birds/flappy-mcp.git"
```

## Step 2 – Run a simulation in pure Python

```python
from flappy_mcp import SimulationRequest, run_flappy

request = SimulationRequest(
    frequency_hz=6.5,
    stroke_amplitude_deg=35.0,
    duration_s=2.0,
    payload_mass_kg=0.15,
)

response = run_flappy(request)
print("Samples:", len(response.trajectory.samples))
print("Energy used (approx):", response.trajectory.energy_j)
```

If `flappy_cli` is installed the helper writes a temporary JSON config, invokes the binary, and parses the output back into typed data. If not, the surrogate generates a sinusoidal trajectory so you can continue experimenting.

## Step 3 – Visualise the motion

```python
import matplotlib.pyplot as plt

samples = response.trajectory.samples
angles = [sample.joint_angle_deg for sample in samples]
times = [sample.time_s for sample in samples]

plt.plot(times, angles)
plt.xlabel("Time [s]")
plt.ylabel("Wing joint angle [deg]")
plt.show()
```

## Step 4 – Bring the simulator to an MCP agent

### FastAPI quickstart

```python
from flappy_mcp.fastapi_app import create_app

app = create_app()
```

Run locally:

```bash
uv run uvicorn flappy_mcp.fastapi_app:create_app --factory --port 8004
```

Try `/simulate` in the automatically generated docs.

### python-sdk tool

```python
from mcp.server.fastmcp import FastMCP
from flappy_mcp.tool import build_tool

mcp = FastMCP("flappy-mcp", "Flappy dynamics simulator")
build_tool(mcp)

if __name__ == "__main__":
    mcp.run()
```

Launch the tool (`uv run mcp dev examples/flappy_tool.py`) and let your MCP-aware IDE or assistant send `flappy-mcp.run` requests.

## Stretch goals

- **Controller tuning:** sweep `frequency_hz` and log `energy_j` to find efficient operating points.
- **Surrogate verification:** compare the surrogate output with the real simulator in a notebook and quantify the error.
- **Mission scripting:** chain this tool with ctrltest-mcp to evaluate closed-loop behaviour.

## Contribute & test

```bash
uv pip install --system -e .[dev]
uv run ruff check .
uv run pytest
```

Unit tests stub out the binary so you can see exactly what request payloads look like and how they’re parsed.

## License

MIT — see [LICENSE](LICENSE).
