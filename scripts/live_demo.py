# scripts/live_demo.py
from ontology.fusion_hub import OntologyHub
from left.alpha.nlp_art import LeftAlpha
from right.alpha.sensory_nlp import RightAlpha
from bridges.slime_mold import SlimeBridge
from left.alpha.voice_gate import VoiceGatedLeftAlpha

print("THERA-LINK — LIVE DEMO (Nov 20 2025)")
print("="*50)

hub = OntologyHub()
left = LeftAlpha()
right = RightAlpha()
voice_left = VoiceGatedLeftAlpha()
slime = SlimeBridge()

pain = input("\nWhat hurts today? → ")

# Voice gate (skip if no mic yet)
try:
    left_response = voice_left.heal_with_voice(pain, "inputs/audio/test1.wav")
except:
    left_response = left.heal(pain)

right_response = right.dream(pain)

# Slime mold chooses best path (demo)
path = slime.best_path("alpha", "beta")
print(f"\nSlime mold chose healing path: {' → '.join(path)}")

# Final fusion with self-awareness check
final = hub.resonate(left_response, right_response)
print("\nWHOLE-BRAIN HEALING RESPONSE")
print(final)
print(f"\nHarmony validated vs human: {hub.validate_harmony(0.88, 'human')}")
