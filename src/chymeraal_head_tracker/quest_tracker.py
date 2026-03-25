"""Head tracking logic for Meta Quest 3 - axes adaptés à la convention réelle Quest 3 / OpenXR."""

import math
import socket
import threading
from .orientation import Quaternion, Orientation


def quaternion_to_euler(q: Quaternion) -> Orientation:
    """Convertit quaternion Quest 3 → Euler (pitch, yaw, roll).
    Axes remappés selon tes tests UDP :
      - q.x → Yaw
      - q.y → Pitch
      - q.z → Roll
    """
    norm = math.sqrt(q.x**2 + q.y**2 + q.z**2 + q.w**2)
    if norm < 1e-6:
        return Orientation(pitch=0.0, yaw=0.0, roll=0.0)

    # Remapping pour matcher la réalité Quest 3
    x = q.y  # original y devient pitch
    y = q.x  # original x devient yaw
    z = q.z
    w = q.w

    # Roll (autour de l'axe X)
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll = math.degrees(math.atan2(t0, t1))

    # Pitch (autour de l'axe Y)
    t2 = +2.0 * (w * y - z * x)
    t2 = max(min(t2, +1.0), -1.0)
    pitch = -math.degrees(math.asin(t2))  # signe inversé pour Quest

    # Yaw (autour de l'axe Z)
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw = math.degrees(math.atan2(t3, t4))

    return Orientation(pitch=pitch, yaw=yaw, roll=roll)


class QuestTracker:
    """Main class - UDP listener + simulate."""

    def __init__(self, udp_port: int = 5005):
        self._current_orientation: Orientation | None = None
        self._connected = False
        self.udp_port = udp_port
        self._udp_thread: threading.Thread | None = None
        self._stop_udp = False

    def is_connected(self) -> bool:
        return self._connected

    def update_orientation(self, q: Quaternion) -> None:
        self._current_orientation = quaternion_to_euler(q)
        self._connected = True

    def start_udp_listener(self, host: str = "0.0.0.0") -> None:
        if self._udp_thread and self._udp_thread.is_alive():
            return
        self._stop_udp = False
        self._udp_thread = threading.Thread(target=self._udp_listener, args=(host,), daemon=True)
        self._udp_thread.start()
        print(f"✅ UDP listener démarré sur {host}:{self.udp_port}")

    def _udp_listener(self, host: str):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, self.udp_port))
        sock.settimeout(1.0)

        while not self._stop_udp:
            try:
                data, _ = sock.recvfrom(1024)
                values = list(map(float, data.decode().strip().split(",")))
                if len(values) == 4:
                    q = Quaternion(x=values[0], y=values[1], z=values[2], w=values[3])
                    self.update_orientation(q)
            except socket.timeout:
                continue
            except Exception:
                pass

    def stop_udp_listener(self):
        self._stop_udp = True
        if self._udp_thread:
            self._udp_thread.join(timeout=1.0)

    def get_orientation(self) -> Orientation | None:
        return self._current_orientation
