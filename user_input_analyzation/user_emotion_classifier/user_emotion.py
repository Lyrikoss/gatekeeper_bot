from models.llama_instance_manager import get_llama_safely

import re

def get_gatekeeper_llama():
    global _llama_instance
    if _llama_instance is None:
        _llama_instance = get_llama_instance()
    return _llama_instance


def classify_emotion(user_text: str) -> tuple[str, float]:
    prompt = (
        "Classify the primary emotion expressed in the following text. "
        "Respond ONLY in this format:\n\n"
        "<tag>/<subtag>, <confidence score from 0 to 1>\n\n"
        f"Text: \"{user_text}\""
    )

    result = llama.generate_text(prompt).strip()

    # Example expected: "sadness/grief, 0.82"
    match = re.match(r"([a-zA-Z\-]+)/([a-zA-Z\-]+),\s*([01](?:\.\d+)?)", result)
    if match:
        tag, subtag, confidence_str = match.groups()
        confidence = float(confidence_str)
        tag_subtag = f"{tag.lower()}/{subtag.lower()}"
        return tag_subtag, confidence

    # Fallback if parsing fails
    return "neutral/none", 0.0


def detect_user_emotion(user_text: str) -> dict:
    tag_subtag, confidence = classify_emotion(user_text)

    if confidence < 0.4:
        # Don't store weak/confused emotion detection
        return {}

    subclass = tag_subtag.split("/")[1]
    key_value = {
        f"user_emotion_{subclass}": tag_subtag,
        f"user_emotion_{subclass}_score": confidence
    }
    return key_value
