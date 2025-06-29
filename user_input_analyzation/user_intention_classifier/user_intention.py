import re
from models.llama_instance_manager import get_llama_safely

def classify_user_intention(user_text: str) -> tuple[str, float]:
    llama = get_llama_safely()
    prompt = (
        "Based on the following input, classify the user's primary intention in one or two words "
        "(e.g., 'seek guidance', 'test boundaries', 'share story', 'issue challenge', 'request entry'). "
        "Return only the intention label and a confidence score between 0 and 1.\n\n"
        "Format: <intention>, <confidence>\n\n"
        f"Text: \"{user_text}\""
    )

    result = llama(prompt, max_tokens=64)["choices"][0]["text"].strip()

    # Example expected: "seek guidance, 0.92"
    match = re.match(r"([a-zA-Z\-_\s]+),\s*([01](?:\.\d+)?)", result)
    if match:
        intention = match.group(1).strip().lower().replace(" ", "_")
        confidence = float(match.group(2))
        return intention, confidence

    return "unknown", 0.0


def detect_user_intention(user_text: str) -> dict:
    intention, confidence = classify_intention(user_text)

    if confidence < 0.4 or intention == "unknown":
        return {}

    return {
        f"user_interactiontype_{intention}": intention,
        f"user_interactiontype_{intention}_score": confidence
    }
