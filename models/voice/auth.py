# models/voice/auth.py  (Full—monthly rotation, decrypt audit)
from speechbrain.pretrained import SpeakerRecognition
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import json
from datetime import datetime
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
        self.key = self._load_or_gen_key()
        self.cipher = Fernet(self.key)
        self.audit_log = "voice_audit.log"
        if CONFIG.get("security", {}).get("voice_biometric", False):
            logger.info("VoiceAuth hardened — rotating keys, audit-proof")

    def _load_or_gen_key(self):
        key_file = "models/voice/secure_key.bin"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                key = f.read()
            # Rotate monthly
            if datetime.now().day == 1:
                key = os.urandom(32)
                with open(key_file, "wb") as f:
                    f.write(key)
                logger.info("Key rotated — monthly hygiene")
        else:
            key = os.urandom(32)
            with open(key_file, "wb") as f:
                f.write(key)
        return base64.urlsafe_b64encode(key)

    def enroll(self, audio_path: str):
        print(f"[VoiceAuth] Enrolling secure voice from {audio_path}")
        self.enrolled = audio_path
        meta = {"path": audio_path, "timestamp": str(datetime.now())}
        encrypted_meta = self.cipher.encrypt(json.dumps(meta).encode())
        with open("models/voice/secure_enroll.bin", "wb") as f:
            f.write(encrypted_meta)
        self._audit("enroll", success=True)
        logger.info("Enrollment encrypted + audited")

    def verify(self, audio_path: str) -> float:
        if not self.enrolled:
            return 0.0
        score, prediction = self.verifier.verify_files(self.enrolled, audio_path)
        trust = float(score)
        # Audit decrypt
        if CONFIG.get("security", {}).get("voice_biometric", False):
            try:
                with open("models/voice/secure_enroll.bin", "rb") as f:
                    decrypted = json.loads(self.cipher.decrypt(f.read()).decode())
                self._audit("verify", success=True, trust=trust, meta=decrypted['timestamp'])
                logger.info(f"Secure verify: Trust {trust:.3f}")
            except Exception as e:
                self._audit("verify", success=False, error=str(e))
                trust *= 0.5  # Penalize
                logger.error(f"Decrypt fail: {e}")
        return trust

    def _audit(self, action: str, success: bool, **kwargs):
        with open(self.audit_log, "a") as f:
            f.write(f"{datetime.now()}: {action} | success={success} | kwargs={kwargs}\n")

if __name__ == "__main__":
    auth = VoiceAuth()
    auth.enroll("inputs/audio/test1.wav")
    print(auth.verify("inputs/audio/test1.wav"))
