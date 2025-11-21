# ontology/fusion_hub.py
import yaml
from pathlib import Path

class OntologyHub:
    def __init__(self):
        with open(Path(__file__).parent / "principles.yaml") as f:
            self.p = yaml.safe_load(f)

    # ←←←  ADD THIS TO ontology/fusion_hub.py  ←←←
        from .self_awareness import SelfAwareness
        self.self_aware = SelfAwareness()

    def validate_harmony(self, score: float, opponent: str = "human") -> bool:
        adjusted = score + self.self_aware.harmony_bonus(opponent)
        return adjusted >= self.p["relational"]["minimum_harmony"]

    def get_recursion_depth(self, opponent: str = "human") -> float:
        """Used by theta layer for strategic reasoning"""
        return self.self_aware.opponent_type_score(opponent)
# ←←←  END OF ADDITION  ←←←
    def validate_harmony(self, score: float) -> bool:
        return score >= self.p["relational"]["minimum_harmony"]

    def resonate(self, left_output: str, right_output: str) -> str:
        # Simple alpha-wave “binaural” blend for now
        return f"{left_output.strip()} ║ {right_output.strip()} (resonating @ α)"
