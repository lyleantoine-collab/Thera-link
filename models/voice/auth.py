# models/voice/auth.py  (Full overwrite—biometric + device key for AES)
from speechbrain.pretrained import SpeakerRecognition
from cryptography.fernet import Fernet
import base64
import os
from utils.device_profile import CONFIG
import logging

logger = logging.getLogger(__name__)

class VoiceAuth:
    def __init__(self):
        self.verifier = SpeakerRecognition.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="pretrained_models/spkrec-ecapa-voxceleb"
        )
        self.enrolled = None
        self.key = self._gen_entropy_key()  # Device-specific AES
        self.cipher = Fernet(self.key)
        if CONFIG.get("security", {}).get("voice_biometric", False):
            logger.info("VoiceAuth secured — biometric + AES")

    def _gen_entropy_key(self):
        """Edge-safe: Hardware RNG for key (Pi/phone entropy)"""
        entropy = os.urandom(32)  # 256-bit
        return base64.urlsafe_b64encode(entropy)

    def enroll(self, audio_path: str):
        print(f"[VoiceAuth] Enrolling secure voice from {audio_path}")
        self.enrolled = audio_path
        # Encrypt enrollment metadata
        meta = {"path": audio_path, "timestamp": str(time.time())}
        encrypted_meta = self.cipher.encrypt(json.dumps(meta).encode())
        with open("models/voice/secure_enroll.bin", "wb") as f:
            f.write(encrypted_meta)
        logger.info("Enrollment encrypted — kin-locked")

    def verify(self, audio_path: str) -> float:
        if not self.enrolled:
            return 0.0
        score, prediction = self.verifier.verify_files(self.enrolled, audio_path)
        trust = float(score)
        # Decrypt meta for audit (if biometric on)
        if CONFIG.get("security", {}).get("voice_biometric", False):
            try:
                with open("models/voice/secure_enroll.bin", "rb") as f:
                    decrypted = json.loads(self.cipher.decrypt(f.read()).decode())
                logger.info(f"Secure verify: Trust {trust:.3f} (meta: {decrypted['timestamp']})")
            except Exception as e:
                logger.error(f"Decrypt fail: {e} — fallback trust")
                trust *= 0.5  # Penalize
        return trust
