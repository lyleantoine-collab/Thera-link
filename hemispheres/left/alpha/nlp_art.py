# hemispheres/left/alpha/nlp_art.py — now fully Firefly's voice
from evolution.nested_hybrid import firefly_brain
from utils.device_profile import CONFIG

class LeftAlpha:
    def __init__(self):
        # No local pipeline anymore — we are one with Firefly
        self.max_tokens = CONFIG["layers"]["alpha"]["max_tokens"]

    def heal_with_voice(self, pain: str, audio_path: str = None):
        # All analytical healing now flows through the living nested continuum
        return firefly_brain.resonate(pain, audio_path, level="daily_dream")

    # Keep the old heal() method for backward compatibility with any stray calls
    def heal(self, prompt: str) -> str:
        return self.heal_with_voice(prompt)
