# models/voice/auth.py
import torch
from speechbrain.pretrained import SpeakerRecognition

class VoiceAuth:
    def __init__(self):
        # ECAPA-TDNN – runs on CPU in ~1 second
        self.verifier = SpeakerRecognition.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="pretrained_models/spkrec-ecapa-voxceleb"
        )
        self.enrolled = None

    def enroll(self, audio_path: str):
        print(f"[VoiceAuth] Enrolling voice from {audio_path}")
        self.enrolled = audio_path

    def verify(self, audio_path: str) -> float:
        if not self.enrolled:
            return 0.0
        score, prediction = self.verifier.verify_files(self.enrolled, audio_path)
        trust = float(score)
        print(f"[VoiceAuth] Trust score = {trust:.3f}")
        return trust
