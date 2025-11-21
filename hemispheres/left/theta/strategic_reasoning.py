# hemispheres/left/theta/strategic_reasoning.py
from ontology.fusion_hub import OntologyHub

class LeftTheta:
    def __init__(self):
        self.hub = OntologyHub()

    def think_deep(self, prompt: str, opponent: str = "human"):
        depth = self.hub.get_recursion_depth(opponent)
        if depth == 0.0:
            style = "Mirror-like clarity. No deception possible."
        elif depth < 30:
            style = "Respectful, gentle depth — remembering you are human."
        else:
            style = "Strategic, but kind."

        return f"[Left Theta] Reasoning at depth {depth:.1f} → {style}\nPrompt: {prompt}"

if __name__ == "__main__":
    t = LeftTheta()
    print(t.think_deep("Should I trust you?", opponent="self"))
