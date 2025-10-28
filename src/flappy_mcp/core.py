"""Core helpers for launching the Flappy simulator."""

from __future__ import annotations

import json
import math
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .models import FlappyFallback, FlappyRequest, FlappyResponse, TrajectoryPoint

FLAPPY_BIN = os.environ.get("FLAPPY_BIN", "flappy_cli")


def execute_flappy(request: FlappyRequest) -> FlappyResponse:
    """Execute Flappy using the request payload.

    If the configured binary exists, the helper writes a temporary configuration file containing
    the scenario dictionary and launches the CLI. Otherwise a deterministic sinusoidal trajectory is
    generated using the fallback parameters.
    """

    scenario_dict = request.scenario or _build_fallback_scenario(request.fallback)

    if _binary_exists():  # pragma: no cover - integration path
        return _run_cli(scenario_dict, request.fallback)

    trajectory = _generate_stub_trajectory(scenario_dict, request.fallback)
    return FlappyResponse(trajectory=trajectory, source="generated", scenario=scenario_dict)


def _binary_exists() -> bool:
    return os.path.exists(FLAPPY_BIN)


def _run_cli(scenario: dict[str, Any], fallback: FlappyFallback) -> FlappyResponse:
    with tempfile.TemporaryDirectory(prefix="flappy_mcp_") as tmpdir:
        cfg_path = Path(tmpdir) / "config.json"
        out_path = Path(tmpdir) / "trajectory.json"
        cfg_payload = {"scenario": scenario}
        cfg_path.write_text(json.dumps(cfg_payload), encoding="utf-8")

        try:
            result = subprocess.run(  # pragma: no cover - integration path
                [FLAPPY_BIN, "--config", str(cfg_path), "--output", str(out_path)],
                check=False,
                capture_output=True,
            )
        except FileNotFoundError as exc:  # pragma: no cover
            raise RuntimeError("Flappy binary not found") from exc

        if result.returncode != 0:  # pragma: no cover
            raise RuntimeError(result.stderr.decode("utf-8", errors="ignore"))

        trajectory_data = json.loads(out_path.read_text(encoding="utf-8"))
        trajectory = [TrajectoryPoint(**point) for point in trajectory_data.get("trajectory", [])]
        return FlappyResponse(trajectory=trajectory, source=str(out_path), scenario=scenario)


def _generate_stub_trajectory(
    scenario: dict[str, Any],
    fallback: FlappyFallback,
) -> list[TrajectoryPoint]:
    sim = scenario.get("simulation", {})
    control = _extract_control(scenario)

    duration = float(sim.get("duration_s", fallback.duration_s))
    timestep = float(sim.get("timestep_s", fallback.timestep_s))
    amplitude = float(control.get("stroke_amplitude_rad", fallback.stroke_amplitude_rad))
    frequency = float(control.get("stroke_frequency_hz", fallback.stroke_frequency_hz))

    steps = int(duration / timestep)
    trajectory: list[TrajectoryPoint] = []
    for i in range(steps + 1):
        t = i * timestep
        angle = amplitude * math.sin(2 * math.pi * frequency * t)
        trajectory.append(TrajectoryPoint(t=t, angle=angle))
    return trajectory


def _build_fallback_scenario(fallback: FlappyFallback) -> dict[str, Any]:
    return {
        "simulation": {
            "duration_s": fallback.duration_s,
            "timestep_s": fallback.timestep_s,
        },
        "control": {
            "stroke_amplitude_rad": fallback.stroke_amplitude_rad,
            "stroke_frequency_hz": fallback.stroke_frequency_hz,
        },
    }


def _extract_control(scenario: dict[str, Any]) -> dict[str, Any]:
    if "control" in scenario:
        return scenario["control"]  # type: ignore[return-value]

    bird = scenario.get("bird")
    if isinstance(bird, dict) and "control" in bird:
        control = bird["control"]
        if isinstance(control, dict):
            return control
    return {}


__all__ = [
    "execute_flappy",
    "FLAPPY_BIN",
]
