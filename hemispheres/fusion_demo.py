# hemispheres/fusion_demo.py
from left.alpha.nlp_art import LeftAlpha
from right.alpha.sensory_nlp import RightAlpha
from ontology.fusion_hub import OntologyHub

hub = OntologyHub()
left  = LeftAlpha()
right = RightAlpha()

pain = input("\nWhat hurts? → ")

left_out  = left.heal(pain)
right_out = right.dream(pain)

final = hub.resonate(left_out, right_out)

print("\nFUSED WHOLE-BRAIN RESPONSE\n" + "="*50)
print(final)
print("\nHarmony check:", hub.validate_harmony(0.92))
