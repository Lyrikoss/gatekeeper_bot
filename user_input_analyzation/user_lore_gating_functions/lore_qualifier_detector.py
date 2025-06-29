from models.llama_instance_manager import get_llama_safely

# Lore stage keywords for clarity
LORE_STAGES = [
    "gatekeeper_role",
    "story_requirement",
    "story_shapes_world",
    "character_fulfillment"
]

def get_gatekeeper_llama():
    return get_llama_safely()

def detect_lore_stage(user_text: str) -> tuple[str, float]:
    """
    Classifies the user's current level of lore understanding based on their input.
    Returns a tuple (lore_stage, confidence_score).
    """
    prompt = f"""
You are an expert in interactive storytelling systems.
Given the user's statement below, identify the *highest lore stage* they currently show understanding of.
Possible stages:
1. gatekeeper_role — The user acknowledges the Gatekeeper as a true gatekeeper.
2. story_requirement — The user realizes they must narrate a story to proceed.
3. story_shapes_world — The user shows they understand their story defines the world they will enter.
4. character_fulfillment — The user has begun or completed a rich narrative character.
Respond in the format: stage_name | confidence (0.0–1.0)

User input:
\"\"\"{user_text}\"\"\"
"""
    llama = get_gatekeeper_llama()
    result = llama(prompt).strip()

    try:
        stage, score = result.split("|")
        stage = stage.strip()
        score = float(score.strip())
        if stage not in LORE_STAGES:
            raise ValueError
    except Exception:
        return None, 0.0  # Fallback if malformed or unknown stage

    return stage, score


def get_lore_gating_variables(user_text: str, threshold: float = 0.6) -> dict:
    """
    Produces ready-to-store and ready-to-prompt variables from user text for lore progression.
    Only includes stages above the confidence threshold.
    """
    stage, score = detect_lore_stage(user_text)
    if stage is None or score < threshold:
        return {}

    return {
        f"user_lorequalifier_{stage}": True,
        f"user_lorequalifier_{stage}_score": score
    }
