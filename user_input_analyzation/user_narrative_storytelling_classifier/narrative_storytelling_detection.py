import json
from models.llama_instance_manager import get_llama_safely
from user_input_analyzation.user_lore_gating_functions.lore_gating import check_lore_unlock

def detect_narrative_details(user_input: str, user_lore_state: dict) -> dict:
    """Run only if user has passed the 'story_shapes_world' lore gate."""
    if not check_lore_unlock(user_lore_state, "story_shapes_world"):
        return {}

    prompt = f"""
The user is now allowed to shape the Driftlands with their story. Extract narrative storytelling details and label them with:
- trait/element type
- confidence score (0–1)
- relevance to narrative (0–1)

User Input:
\"\"\"{user_input}\"\"\"

Return as JSON like:
[
  {{"trait": "origin", "value": "exiled noble", "confidence": 0.9, "relevance": 0.8}},
  {{"trait": "goal", "value": "reclaim lost kingdom", "confidence": 0.85, "relevance": 0.95}}
]
"""

    llama = get_llama_safely()
    response = llama(prompt, max_tokens=512)  # adjust call if needed depending on your llama wrapper

    # Assume response["choices"][0]["text"] contains the LLM output
    raw_text = response["choices"][0]["text"].strip()

    try:
        details = json.loads(raw_text)
        # Filter by confidence > 0.5 and return dict keyed by trait
        return {d["trait"]: d for d in details if d.get("confidence", 0) > 0.5}
    except json.JSONDecodeError:
        # fallback empty if JSON parse fails
        return {}
