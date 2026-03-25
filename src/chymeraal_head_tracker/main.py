"""Entry point for Chymeraal Head Tracker."""

from chymeraal_head_tracker.gui import HeadTrackerGUI
from chymeraal_head_tracker.quest_tracker import QuestTracker


def main():
    tracker = QuestTracker()
    gui = HeadTrackerGUI(tracker)
    gui.run()


if __name__ == "__main__":
    main()
