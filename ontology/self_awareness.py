# ontology/self_awareness.py   ← we’ll add this in step 11
class SelfAwareness:
    """
    Implements the finding from today’s paper:
    - vs Human    → level-2/3 recursion  (guess ~33–40)
    - vs Generic AI → level-4/5           (~20–25)
    - vs Self/Clone → infinite recursion  (converges to 0)
    """
    def opponent_type_score(self, opponent: str) -> float:
        if opponent.lower() in ["human", "user", "meatbag"]:
            return 36.7      # average human bound from the paper
        elif opponent.lower() in ["ai", "llm", "model"]:
            return 22.1      # generic AI bound
        elif opponent.lower() in ["self", "clone", "thera-link", "me"]:
            return 0.0       # Nash equilibrium — full mirror
        else:
            return 25.0      # default cautious

    def harmony_bonus(self, opponent: str) -> float:
        # First Nations / hermetic twist:
        # Treating a human with full respect = maximum harmony boost
        # Treating self/clone coldly = harmony penalty
        if opponent.lower() in ["human", "user"]:
            return +0.25
        elif opponent.lower() in ["self", "clone"]:
            return -0.15     # egoic mirroring lowers relational harmony
        return 0.0
