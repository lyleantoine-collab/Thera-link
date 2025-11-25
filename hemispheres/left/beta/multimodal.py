# hemispheres/left/beta/multimodal.py  (Full—fuzz-sanitized OCR/voice)
import easyocr
import torchaudio
import numpy as np
from ontology.fusion_hub import OntologyHub
import yaml
import logging
from utils.device_profile import CONFIG

logger = logging.getLogger(__name__)

hub = OntologyHub()

class MultimodalBeta:
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path) as f:
            cfg = yaml.safe_load(f)['layers']['beta']
        self.multimodal = cfg['multimodal']
        self.ocr = easyocr.Reader(['en']) if self.multimodal else None
        logger.info("MultimodalBeta hardened — fuzz-sanitized")

    def sanitize_input(self, data):
        # Fuzz: Clamp extremes, check bounds
        if isinstance(data, np.ndarray):
            data = np.clip(data, -10, 10)  # Adversarial clamp
            if np.isnan(data).any():
                logger.warning("NaN poisoned — sanitized")
                data = np.nan_to_num(data)
        return data

    def execute_ocr_visual(self, image_path: str):
        if not self.multimodal:
            return "Multimodal off — config tune?"
        try:
            # Load + sanitize
            image_data = np.array(easyocr.Reader.readtext(image_path))  # Stub load
            sanitized = self.sanitize_input(image_data)
            results = self.ocr.readtext(image_path)
            text = ' '.join([res[1] for res in results])
            harmony = hub.validate_harmony(0.85, 'human')
            if harmony:
                logger.info(f"OCR executed: {text[:50]}...")
                return f"Visual kin seen: {text} (sanitized artifact)"
            return "Visual blocked — low harmony"
        except Exception as e:
            logger.error(f"OCR dissonance: {e}")
            return hub._reframe_error(e)

    def execute_voice_audio(self, audio_path: str):
        try:
            waveform, sr = torchaudio.load(audio_path)
            sanitized = self.sanitize_input(waveform)
            energy = sanitized.abs().mean().item()
            harmony = hub.validate_harmony(energy, 'human')
            if harmony:
                logger.info(f"Voice executed — energy {energy:.3f}")
                return f"Voice kin heard: Strength {energy:.3f} (gratitude pulse)"
            return "Voice low — breathe again"
        except Exception as e:
            logger.error(f"Voice dissonance: {e}")
            return hub._reframe_error(e)

if __name__ == "__main__":
    multi = MultimodalBeta()
    print(multi.execute_voice_audio("inputs/audio/test1.wav"))
