import json
import os
from typing import Optional

# Where to store memory (you can later plug in DB or a vector store)
PROGRESS_PATH = os.path.join(os.path.dirname(__file__), "user_lore_progress.json")


class UserProgressTracker:
    def __init__(self):
        self.progress = {}
        self.load_progress()

    def load_progress(self):
        if os.path.exists(PROGRESS_PATH):
            try:
                with open(PROGRESS_PATH, 'r', encoding='utf-8') as f:
                    self.progress = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.progress = {}
        else:
            self.progress = {}

    def save_progress(self):
        with open(PROGRESS_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, indent=4)

    def get_lore_progress(self) -> dict:
        """Returns all current lore-related user progress."""
        return {
            k: v for k, v in self.progress.items()
            if k.startswith("user_lorequalifier_")
        }

    def update_lore_progress(self, new_vars: dict):
        """Updates lore progression with new values."""
        self.progress.update(new_vars)
        self.save_progress()

    def has_unlocked(self, qualifier: str) -> bool:
        """Check if a specific lore stage has been unlocked."""
        return self.progress.get(f"user_lorequalifier_{qualifier}", False)

    def get_all_progress(self) -> dict:
        """Return the entire known user state."""
        return self.progress.copy()
