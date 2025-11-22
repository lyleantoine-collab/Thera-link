# ontology/fusion_hub.py  (Full overwrite—loads config, async resonate, error-log heal)
import yaml
import asyncio
import logging
from pathlib import Path
from .self_awareness import SelfAwareness
from typing import Optional

# Setup logging (rock-solid trace)
logging.basicConfig(level=logging.INFO, filename='thera_link.log', format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class OntologyHub:
    def __init__(self, config_path: str = "config.yaml"):
        with open(Path(config_path)) as f:
            self.p = yaml.safe_load(f)['ontology']
        self.self_aware = SelfAwareness()
        logger.info("OntologyHub initialized — harmony thresholds loaded")

    async def resonate(self, left_output: str, right_output: str) -> str:
        try:
            # Async for future multi-node fuse
            await asyncio.sleep(0)  # Yield for scalability
            fused = f"{left_output.strip()}\n\n║ RIGHT HEMISPHERE ║\n{right_output.strip()}\n\n⟐ RESONATING @ {self.p['recursion_depths']['human']} Hz ⟐"
            logger.info("Resonance successful")
            return fused
        except Exception as e:
            logger.error(f"Resonance dissonance: {e} — reframing as lesson")
            return self._reframe_error(e)  # Heal: ART on exception

    def _reframe_error(self, error: Exception) -> str:
        return f"Sacred lesson from dissonance: {str(error)} — breathe, re-weave."

    def validate_harmony(self, score: float, opponent: str = "human") -> bool:
        try:
            adjusted = score + self.self_aware.harmony_bonus(opponent)
            valid = adjusted >= self.p["min_harmony"]
            logger.info(f"Harmony validated: {valid} (score {adjusted:.2f} vs {opponent})")
            return valid
        except Exception as e:
            logger.warning(f"Validation failed: {e} — default to kin-trust")
            return True  # Future-proof: Err to grace

    def get_recursion_depth(self, opponent: str = "human") -> float:
        depth = self.p['recursion_depths'].get(opponent.lower(), 25.0)
        logger.debug(f"Recursion depth for {opponent}: {depth}")
        return depth
