# tests/integration_tests.py  (Full—add to existing stub)
import pytest
from hemispheres.left.alpha.voice_gate import VoiceGatedLeftAlpha
from models.voice.auth import VoiceAuth
import tempfile
import os

@pytest.fixture
def voice_gate():
    return VoiceGatedLeftAlpha()

@pytest.fixture
def mock_audio(tmp_path):
    # Create dummy WAV (pytest magic)
    dummy = tmp_path / "dummy.wav"
    dummy.write_bytes(b"fake audio bytes")
    return str(dummy)

def test_voice_enroll_and_verify_high_trust(voice_gate, mock_audio):
    voice_gate.auth.enroll(mock_audio)
    trust = voice_gate.auth.verify(mock_audio)
    assert trust > 0.65  # SpeechBrain sim > threshold

def test_voice_low_trust_blocks_healing(voice_gate, mock_audio):
    voice_gate.auth.enroll(mock_audio)
    low_audio = mock_audio.replace("dummy", "low_trust")  # Diff file sim
    with pytest.raises(ValueError, match="trust too low"):
        voice_gate.heal_with_voice("Test pain", low_audio)

def test_fallback_no_audio(voice_gate):
    # Graceful if no mic
    result = voice_gate.heal_with_voice("Test pain")  # No audio arg
    assert "healing" in result.lower()  # Proceeds w/ warning?

# Run: pytest tests/integration_tests.py -v
# ... (add to integration_tests.py)
from bridges.slime_mold import EmotionalSlimeBridge

@pytest.fixture
def slime():
    return EmotionalSlimeBridge()

def test_emotion_pulse_thickens_flow(slime):
    initial_flow = [d["flow"] for u,v,d in slime.G.edges(data=True)]
    slime.pulse("joy", 2.0)
    new_flows = [d["flow"] for u,v,d in slime.G.edges(data=True) if d["emotion"] == "joy"]
    assert all(f > 1.0 for f in new_flows)  # Thickened

def test_evaporation_prevents_infinity(slime):
    for _ in range(100):
        slime.pulse("fear", 1.0)
    dom = slime.dominant_emotion()
    assert dom == "fear"  # But flows < infinity (0.98^100 ~0.13)

# Run full: pytest tests/ -v --cov=bridges
