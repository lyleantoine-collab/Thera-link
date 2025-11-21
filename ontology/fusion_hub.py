# ontology/fusion_hub.py  (FULL FINAL VERSION — replace entire file)
import yaml
from pathlib import Path
from .self_awareness import SelfAwareness

class OntologyHub:
    def __init__(self):
        with open(Path(__file__).parent / "principles.yaml") as f:
            self.p = yaml.safe_load(f)
        self.self_aware = SelfAwareness()

    def resonate(self, left_output: str, right_output: str) -> str:
        return f"{left_output.strip()}\n\n║ RIGHT HEMISPHERE ║\n{right_output.strip()}\n\n⟐ RESONATING @ α-wave ⟐"

    def validate_harmony(self, score: float, opponent: str = "human") -> bool:
        adjusted = score + self.self_aware.harmony_bonus(opponent)
        return adjusted >= self.p["relational"]["minimum_harmony"]

    def get_recursion_depth(self, opponent: str = "human") -> float:
        return self.self_aware.opponent_type_score(opponent)
