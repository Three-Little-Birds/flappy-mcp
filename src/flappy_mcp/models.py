"""Typed models used by the Flappy MCP helpers."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class FlappyFallback(BaseModel):
    """Fallback parameters used when the Flappy binary is unavailable."""

    duration_s: float = Field(2.0, gt=0.0)
    timestep_s: float = Field(0.02, gt=0.0)
    stroke_amplitude_rad: float = Field(0.3, ge=0.0)
    stroke_frequency_hz: float = Field(4.0, ge=0.0)


class FlappyRequest(BaseModel):
    """Request payload for a Flappy simulation."""

    scenario: dict[str, Any] | None = Field(
        default=None,
        description="Full scenario dictionary passed directly to flappy_cli.",
    )
    fallback: FlappyFallback = Field(
        default_factory=FlappyFallback,
        description="Parameters used if the binary is unavailable or when generating a stub trajectory.",
    )


class TrajectoryPoint(BaseModel):
    t: float
    angle: float


class FlappyResponse(BaseModel):
    """Response returned by `execute_flappy`."""

    trajectory: list[TrajectoryPoint]
    source: str
    scenario: dict[str, Any] | None = None
