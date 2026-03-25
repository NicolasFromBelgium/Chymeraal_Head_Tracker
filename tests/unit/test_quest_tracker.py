"""Unit tests for QuestTracker - TDD style."""

from dataclasses import asdict

from chymeraal_head_tracker.quest_tracker import QuestTracker
from chymeraal_head_tracker.orientation import Quaternion, Orientation


def test_default_tracker_is_disconnected():
    tracker = QuestTracker()
    assert not tracker.is_connected()


def test_get_orientation_before_any_data_returns_none():
    tracker = QuestTracker()
    assert tracker.get_orientation() is None


def test_update_with_neutral_quaternion():
    tracker = QuestTracker()
    q_neutral = Quaternion(x=0.0, y=0.0, z=0.0, w=1.0)
    tracker.update_orientation(q_neutral)

    orient = tracker.get_orientation()
    assert orient is not None
    assert abs(orient.pitch) < 0.1
    assert abs(orient.yaw) < 0.1
    assert abs(orient.roll) < 0.1


def test_orientation_dataclass_is_serializable():
    orient = Orientation(pitch=12.5, yaw=-45.3, roll=3.7)
    data = asdict(orient)
    assert data == {"pitch": 12.5, "yaw": -45.3, "roll": 3.7}
