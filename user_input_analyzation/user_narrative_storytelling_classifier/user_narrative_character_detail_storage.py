import json
import os

CHARACTER_PROFILE_PATH = os.path.join(os.path.dirname(__file__), "user_character_profile.json")


class NarrativeCharacterStore:
    def __init__(self):
        self.profile = {}
        self.load_profile()

    def load_profile(self):
        if os.path.exists(CHARACTER_PROFILE_PATH):
            with open(CHARACTER_PROFILE_PATH, "r", encoding="utf-8") as f:
                self.profile = json.load(f)
        else:
            self.profile = {}

    def save_profile(self):
        with open(CHARACTER_PROFILE_PATH, "w", encoding="utf-8") as f:
            json.dump(self.profile, f, indent=4)

    def update_from_detected(self, detected_traits: dict):
        """Merge new narrative data if confidence/relevance are high enough."""
        for trait, data in detected_traits.items():
            stored = self.profile.get(trait)
            if (
                not stored
                or data["confidence"] > stored.get("confidence", 0.5)
                or data["relevance"] > stored.get("relevance", 0.5)
            ):
                self.profile[trait] = data
        self.save_profile()

    def get_full_profile(self):
        return self.profile.copy()

    def is_complete(self, required_traits: list[str]) -> bool:
        return all(trait in self.profile for trait in required_traits)
