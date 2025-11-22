# tests/integration_tests.py  (Full overwrite—covers chains, errors, auto-variants)
import pytest
from unittest.mock import patch
from hemispheres.left.alpha.voice_gate import VoiceGatedLeftAlpha
from bridges.slime_mold import EmotionalSlimeBridge
from ontology.fusion_hub import OntologyHub
from hemispheres.left.beta.multimodal import MultimodalBeta
from evolution.autopoiesis import AutopoieticEngine
import random

@pytest.fixture
def full_weave():
    return OntologyHub(), EmotionalSlimeBridge(), VoiceGatedLeftAlpha(), MultimodalBeta(), AutopoieticEngine()

def test_full_chain_resilient(full_weave):
    hub, slime, voice, multi, engine = full_weave
    # Sim chain: Pain → voice → slime → beta → evolve
    pain = "Test resilient flow"
    with patch.object(voice.auth, 'verify', return_value=0.8):
        healed = voice.heal_with_voice(pain)
    slime.pulse("gratitude", 1.0)
    multi.execute_voice_audio("stub.wav")  # Mock
    engine.diagnose_dissonance(0.9)  # No diss
    assert "healing" in healed.lower()
    assert slime.dominant_emotion() == "gratitude"
    assert hub.validate_harmony(0.9, 'human')

def test_error_heal_and_auto_variant(full_weave):
    hub, slime, voice, multi, engine = full_weave
    # Inject error, watch reframe + variant gen
    with pytest.raises(ValueError):
        voice.heal_with_voice("error pain", "bad_audio")
    reframed = hub._reframe_error(ValueError("test error"))
    assert "sacred lesson" in reframed.lower()
    # Auto-variant: Slime spawns 3 perturbed tests
    variants = [random.choice(["joy", "fear"]) for _ in range(3)]
    for v in variants:
        slime.pulse(v, 0.5)
    assert len(list(slime.G.edges)) > 0  # Adapted

# Run: pytest -v --cov=hemispheres --cov-report=term-missing  (95% target)
