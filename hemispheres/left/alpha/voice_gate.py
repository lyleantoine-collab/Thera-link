# hemispheres/left/alpha/voice_gate.py
from models.voice.auth import VoiceAuth
from ontology.fusion_hub import OntologyHub
from left.alpha.nlp_art import LeftAlpha

class VoiceGatedLeftAlpha:
    def __init__(self):
        self.auth = VoiceAuth()
        self.brain = LeftAlpha()
        self.hub = OntologyHub()

    def heal_with_voice(self, prompt: str, audio_path: str = "inputs/audio/enroll.wav"):
        trust = self.auth.verify(audio_path)
        if trust < 0.65:
            return "Voice not recognized — relational trust too low to proceed."
        
        harmony_bonus = self.hub.self_aware.harmony_bonus("human")
        print(f"Voice verified — +{harmony_bonus} harmony for being human")
        
        return self.brain.heal(prompt)

# Quick test
if __name__ == "__main__":
    vg = VoiceGatedLeftAlpha()
    vg.auth.enroll("inputs/audio/enroll.wav")  # first time only
    print(vg.heal_with_voice("I feel lost", "inputs/audio/enroll.wav"))
