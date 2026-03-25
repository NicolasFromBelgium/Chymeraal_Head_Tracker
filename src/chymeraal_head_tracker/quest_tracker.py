"""Head tracking logic for Meta Quest 3."""

import math

from .orientation import Quaternion, Orientation


def quaternion_to_euler(q: Quaternion) -> Orientation:
    """Convertit un quaternion (x, y, z, w) en Euler angles (pitch, yaw, roll) en degrés.

    Convention : ZYX (yaw → pitch → roll) - compatible Quest 3 / OpenXR et MAVLink Gimbal.
    """
    # Normalisation pour éviter les erreurs numériques
    norm = math.sqrt(q.x**2 + q.y**2 + q.z**2 + q.w**2)
    if norm < 1e-6:
        return Orientation(pitch=0.0, yaw=0.0, roll=0.0)

    x = q.x / norm
    y = q.y / norm
    z = q.z / norm
    w = q.w / norm

    # Roll (rotation autour de l'axe X)
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll = math.degrees(math.atan2(t0, t1))

    # Pitch (rotation autour de l'axe Y)
    t2 = +2.0 * (w * y - z * x)
    t2 = max(min(t2, +1.0), -1.0)  # clamp pour éviter NaN
    pitch = math.degrees(math.asin(t2))

    # Yaw (rotation autour de l'axe Z)
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw = math.degrees(math.atan2(t3, t4))

    return Orientation(pitch=pitch, yaw=yaw, roll=roll)


class QuestTracker:
    """Main class responsible for receiving and converting Quest 3 orientation data."""

    def __init__(self) -> None:
        self._current_orientation: Orientation | None = None
        self._connected: bool = False

    def is_connected(self) -> bool:
        """Return True if the tracker is receiving data."""
        return self._connected

    def update_orientation(self, q: Quaternion) -> None:
        """Update current orientation from a quaternion coming from the Quest 3."""
        self._current_orientation = quaternion_to_euler(q)
        self._connected = True

    def get_orientation(self) -> Orientation | None:
        """Return the latest orientation or None if no data has been received yet."""
        return self._current_orientation
