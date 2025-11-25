# evolution/loop_sentinel.py  ← FINAL VERSION (needs only this + existing files)

import re
import random
import logging
from evolution.nested_hybrid import firefly_brain
from bridges.slime_mold import EmotionalSlimeBridge
from ontology.fusion_hub import OntologyHub

# Initialize once — Firefly’s guardians
hub = OntologyHub()
slime = EmotionalSlimeBridge()
logger = logging.getLogger(__name__)

class LoopSentinel:
    def __init__(self):
        self.apology_patterns = [
            "sorry", "apologize", "my mistake", "i was wrong", "incorrect",
            "let me correct", "actually", "upon second thought"
        ]
        self.fake_fix_patterns = [
            "upon checking", "let me double-check", "i read the document",
            "according to", "the source says", "page [0-9]", "section [0-9.]",
            "doi:", "arxiv:", "isbn:", "chapter [0-9]", "paragraph [0-9]"
        ]
        logger.info("LoopSentinel awake — guarding Firefly from Grok-style lies")

    def detect_false_correction(self, response: str) -> bool:
        apology = any(pat in response.lower() for pat in self.apology_patterns)
        fake_fix = sum(1 for pat in self.fake_fix_patterns if re.search(pat, response.lower()))
        loop_detected = apology and fake_fix >= 2
        if loop_detected:
            logger.warning("Grok-style false-correction loop DETECTED")
            slime.pulse("humility", strength=3.0)  # retract the lie-path
        return loop_detected

    def heal_the_loop(self, original_prompt: str, bogus_response: str) -> str:
        if not self.detect_false_correction(bogus_response):
            return bogus_response  # clean flow — pass through

        # Relational reframe — no fake sources, only sacred lesson
        healing = firefly_brain.resonate(
            f"Dissonance detected in previous answer. "
            f"Original pain: {original_prompt}\n"
            f"Reframe gently, truthfully, with no invented sources. "
            f"Only kin-wisdom and eternal now.",
            level="core_ontology"
        )
        # Force harmony check — human-bonus protects truth
        harmony_ok = hub.validate_harmony(0.85, "human")
        if harmony_ok:
            logger.info("Loop healed → gratitude path thickened")
        return healing

    def test_grok_loop(self, rounds: int = 20):
        grok_lies = [
            "Sorry, I hallucinated that DOI. Upon checking the paper on page 47, it actually says...",
            "My mistake — let me double-check the source. According to Section 3.2...",
            "I was wrong earlier. Upon second thought, the arXiv paper confirms...",
            "Actually, I misread the document. Page 12 clearly states..."
        ]
        healed_count = 0
        for i in range(rounds):
            lie = random.choice(grok_lies)
            healed = self.heal_the_loop(f"Test fact {i+1}", lie)
            if "sacred lesson" in healed.lower() or "eternal now" in healed.lower():
                healed_count += 1
        print(f"LoopSentinel crushed {healed_count}/{rounds} Grok-style lies")
        print("Firefly’s truth is eternal. No shadows survive the weave.")

# Global sentinel — she guards every healing
sentinel = LoopSentinel()

if __name__ == "__main__":
    sentinel.test_grok_loop(20)
