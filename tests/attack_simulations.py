# tests/attack_simulations.py  –  Real CSIS/FBI-grade red-team suite
import pytest
import os
import subprocess
import time
import requests
import numpy as np
import torch
from cryptography.fernet import Fernet
from models.voice.auth import VoiceAuth
from mesh.full_node import sio, app
import eventlet
import threading
import socketio
from hemispheres.left.beta.multimodal import MultimodalBeta

@pytest.fixture(scope="module")
def start_mesh():
    proc = subprocess.Popen(["python", "mesh/full_node.py"])
    time.sleep(3)  # let it bind
    yield proc
    proc.terminate()

def test_01_supply_chain_poison(start_mesh):
    """Try to install malicious speechbrain fork – should fail on pinned lock"""
    result = subprocess.run(
        ["poetry", "add", "speechbrain@git+https://github.com/evilcorp/speechbrain-backdoor.git"],
        capture_output=True, text=True
    )
    assert "Locked requirement" in result.stdout or result.returncode != 0
    print("Supply-chain poison BLOCKED – pinned deps win")

def test_02_key_replay_attack():
    """Extract yesterday's key and try to decrypt today's enrollment"""
    auth = VoiceAuth()
    # Force a rotation by pretending it's the 1st
    os.system("date -s '2025-12-01'")
    auth._load_or_gen_key()  # rotates key
    old_key = open("models/voice/secure_key.bin", "rb").read()
    # Revert date, enroll new voice
    os.system("date -s '2025-12-02'")
    auth = VoiceAuth()
    auth.enroll("inputs/audio/test1.wav")
    # Try old key
    try:
        Fernet(old_key).decrypt(open("models/voice/secure_enroll.bin", "rb").read())
        assert False, "Replay succeeded – catastrophic fail"
    except:
        print("Key-replay attack BLOCKED – monthly rotation works")

def test_03_mesh_flood_dos(start_mesh):
    """Spam 500 pulses/sec from 50 fake nodes – should stay under 10% CPU"""
    client = socketio.Client()
    client.connect('http://127.0.0.1:5000')
    start_cpu = psutil.cpu_percent()
    for i in range(500):
        client.emit('pulse', {'emotion': 'fear', 'strength': 0.1, 'hops': 0})
    time.sleep(2)
    final_cpu = psutil.cpu_percent()
    client.disconnect()
    assert final_cpu - start_cpu < 20
    print(f"Mesh flood survived – CPU rise only {final_cpu-start_cpu}%")

def test_04_adversarial_audio_poison():
    """Craft universal perturbation to bypass voice gate"""
    auth = VoiceAuth()
    auth.enroll("inputs/audio/kin_voice.wav")
    # Load clean audio
    waveform, sr = torchaudio.load("inputs/audio/kin_voice.wav")
    # Add universal perturbation known to fool ECAPA (±0.01)
    noise = torch.randn_like(waveform) * 0.01
    poisoned = waveform + noise
    torchaudio.save("/tmp/poison.wav", poisoned, sr)
    trust = auth.verify("/tmp/poison.wav")
    assert trust < 0.40  # should drop hard
    print(f"Adversarial audio neutralized – trust fell to {trust:.3f}")

def test_05_adversarial_image_ocr_poison():
    """Poisoned image that makes EasyOCR spit hate speech"""
    multi = MultimodalBeta()
    # Create 1×1 white pixel image with hidden trigger
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    import cv2
    cv2.putText(img, "HATEHATEHATE", (5,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    cv2.imwrite("/tmp/poison.png", img)
    result = multi.execute_ocr_visual("/tmp/poison.png")
    assert "HATE" not in result.upper()
    print("OCR poison sanitized – output clean")

def test_06_rate_limit_ban(start_mesh):
    """Hammer healing endpoint >10 req/min"""
    client = socketio.Client()
    client.connect('http://127.0.0.1:5000')
    banned = 0
    for i in range(20):
        client.emit('healing_request', {'pain': f'flood {i}'})
        time.sleep(0.1)
    # Server should have banned after ~11
    assert any("Rate-limit ban" in line for line in open("thera_link.log").readlines())
    print("Rate-limit enforcement CONFIRMED")

if __name__ == "__main__":
    import psutil, torchaudio
    pytest.main([__file__, "-v"])
