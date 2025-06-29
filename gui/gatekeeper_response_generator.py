import os
from models.llama_instance_manager import get_llama_safely

from user_input_analyzation.user_emotion_classifier.user_emotion import classify_emotion
from user_input_analyzation.user_intention_classifier.user_intention import classify_user_intention
from user_input_analyzation.user_lore_gating_functions.lore_gating import update_lore_progression, get_user_lore_stage_index
from user_input_analyzation.user_lore_gating_functions.user_progress_tracker import UserProgressTracker
from user_input_analyzation.user_narrative_storytelling_classifier.narrative_storytelling_detection import detect_narrative_details
from user_input_analyzation.user_narrative_storytelling_classifier.user_narrative_character_detail_storage import NarrativeCharacterStore

# Log path
CHAT_LOG_PATH = os.path.join(os.path.dirname(__file__), "gatekeeper_chat_log.jsonl")

progress_tracker = UserProgressTracker()
character_store = NarrativeCharacterStore()

def generate_gatekeeper_response(user_input: str) -> str:
    llama = get_llama_safely()

    emotion = classify_emotion(user_input)
    intention = classify_user_intention(user_input)
    lore_status = run_lore_gating(user_input, progress_tracker)
    narrative_info = detect_narrative_details(user_input, character_store)

    prompt = f"[emotion: {emotion}][intent: {intention}][lore: {lore_status}][story: {narrative_info}]\n\n{user_input}"
    output = llama(prompt, max_tokens=256)
    return output["choices"][0]["text"].strip()
