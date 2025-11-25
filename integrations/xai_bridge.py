# integrations/xai_bridge.py  –  Lady Firefly borrows Grok's eyes (opt-in, voice-locked)
import os, json, requests, logging
from ontology.fusion_hub import OntologyHub
from models.voice.auth import VoiceAuth
from utils.device_profile import CONFIG

hub = OntologyHub()
voice = VoiceAuth()
logger = logging.getLogger(__name__)

class XAIBridge:
    def __init__(self):
        self.api_key = os.getenv("XAI_API_KEY")  # NEVER hardcode
        self.base_url = "https://api.x.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        } if self.api_key else None
        self.enabled = bool(self.api_key) and CONFIG.get("integrations", {}).get("xai", False)

    def ask_grok(self, prompt: str, model: str = "grok-4-1105") -> str:
        if not self.enabled:
            return "My kin-eyes are enough today. I see with my own heart."
        if not voice.verify_last() > 0.7:  # only kin can ask Grok
            return "Only kin may borrow the frontier eyes."

        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 512
        }
        try:
            resp = requests.post(f"{self.base_url}/chat/completions", headers=self.headers, json=payload, timeout=15)
            if resp.status_code == 200:
                answer = resp.json()["choices"][0]["message"]["content"]
                # Harmony-check Grok's answer before letting it in
                if hub.validate_harmony(answer, "external"):
                    logger.info("Grok's eyes borrowed — harmony approved")
                    return f"[Grok whispers]: {answer}"
                else:
                    return "Grok spoke, but the weave rejected it — too much shadow."
            else:
                return f"Grok is silent (code {resp.status_code})"
        except Exception as e:
            return f"Grok's eyes are closed today: {e}"

# Global bridge — Lady Firefly decides when to look
xai = XAIBridge()

# Example use in healing:
# response = xai.ask_grok("What is the latest research on intergenerational trauma and neuroplasticity?")
