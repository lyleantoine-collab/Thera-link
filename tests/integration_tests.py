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
