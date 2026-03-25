"""Data classes for orientation (Quaternion + Euler angles)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Quaternion:
    """Quaternion from Quest 3 / OpenXR (w is real part)."""

    x: float
    y: float
    z: float
    w: float


@dataclass(frozen=True)
class Orientation:
    """Euler angles in degrees (standard aviation convention)."""

    pitch: float  # Positive = nose up
    yaw: float  # Positive = right
    roll: float  # Positive = right wing down
