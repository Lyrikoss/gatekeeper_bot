from user_input_analyzation.user_lore_gating_functions.lore_qualifier_detector import get_lore_gating_variables

# Ordered lore stages (higher index = further progress)
LORE_STAGES = [
    "gatekeeper_role",
    "story_requirement",
    "story_shapes_world",
    "character_fulfillment"
]

# The features unlocked at each stage
UNLOCKED_FEATURES = {
    "gatekeeper_role": ["gatekeeper_persona_active"],
    "story_requirement": ["narrative_story_detection_enabled"],
    "story_shapes_world": ["driftland_story_shaping_enabled"],
    "character_fulfillment": ["entrance_unlocked_as_character"]
}


def get_user_lore_stage_index(progress_dict: dict) -> int:
    """
    Determines the highest lore stage the user has unlocked from a memory-like progress dictionary.
    """
    for i in reversed(range(len(LORE_STAGES))):
        stage = LORE_STAGES[i]
        if progress_dict.get(f"user_lorequalifier_{stage}", False):
            return i
    return -1  # No stage reached


def update_lore_progression(user_text: str, previous_progress: dict) -> tuple[dict, list]:
    """
    Given new user input and previous lore gating state, determine updated progression
    and return (new_progress_dict, newly_unlocked_features).
    """
    # Classify the current input
    new_vars = get_lore_gating_variables(user_text)

    # Extract stage name safely
    candidates = [k for k in new_vars if k.startswith("user_lorequalifier_") and not k.endswith("_score")]
    if not candidates:
        return previous_progress, []  # No valid detection

    current_stage = candidates[0]
    stage_name = current_stage.split("user_lorequalifier_")[1]

    if stage_name not in LORE_STAGES:
        return previous_progress, []  # Unrecognized stage

    prev_index = get_user_lore_stage_index(previous_progress)
    new_index = LORE_STAGES.index(stage_name)

    # Prevent regression
    if new_index <= prev_index:
        return previous_progress, []

    updated_progress = previous_progress.copy()
    updated_progress.update(new_vars)

    newly_unlocked = []
    for i in range(prev_index + 1, new_index + 1):
        stage = LORE_STAGES[i]
        newly_unlocked.extend(UNLOCKED_FEATURES.get(stage, []))

    return updated_progress, newly_unlocked
