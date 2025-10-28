from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest import mock

from fastapi.testclient import TestClient

import flappy_mcp.core as core
from flappy_mcp.core import execute_flappy
from flappy_mcp.fastapi_app import create_app
from flappy_mcp.models import FlappyFallback, FlappyRequest


def _fake_run(
    args: list[str],
    *,
    check: bool,
    capture_output: bool,
) -> subprocess.CompletedProcess[bytes]:
    output = {"trajectory": [{"t": 0.0, "angle": 0.1}]}
    Path(args[4]).write_text(json.dumps(output), encoding="utf-8")
    return subprocess.CompletedProcess(args, 0, b"ok", b"")


def test_execute_flappy_stub(monkeypatch) -> None:
    monkeypatch.setattr(core, "FLAPPY_BIN", "flappy_cli_missing", raising=False)
    monkeypatch.setattr(core, "_binary_exists", lambda: False)
    request = FlappyRequest(
        scenario=None,
        fallback=FlappyFallback(
            duration_s=0.1, timestep_s=0.05, stroke_amplitude_rad=0.2, stroke_frequency_hz=1.0
        ),
    )

    response = execute_flappy(request)
    assert response.source == "generated"
    assert len(response.trajectory) == 3


def test_execute_flappy_cli(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(core, "FLAPPY_BIN", "flappy_cli", raising=False)
    monkeypatch.setattr(core, "_binary_exists", lambda: True)
    monkeypatch.setattr(core.subprocess, "run", _fake_run)
    monkeypatch.setattr(
        core.tempfile,
        "TemporaryDirectory",
        mock.MagicMock(
            return_value=mock.MagicMock(
                __enter__=lambda self: str(tmp_path), __exit__=lambda *args: False
            )
        ),
    )

    request = FlappyRequest(scenario={"simulation": {"duration_s": 0.1, "timestep_s": 0.05}})
    response = execute_flappy(request)
    assert response.source.endswith("trajectory.json")
    assert response.trajectory[0].angle == 0.1


def test_fastapi_endpoint(monkeypatch) -> None:
    monkeypatch.setattr(core, "FLAPPY_BIN", "flappy_cli_missing", raising=False)
    app = create_app()
    client = TestClient(app)
    payload = {
        "scenario": {
            "simulation": {"duration_s": 0.1, "timestep_s": 0.05},
            "control": {"stroke_amplitude_rad": 0.2, "stroke_frequency_hz": 1.0},
        }
    }

    response = client.post("/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "generated"
