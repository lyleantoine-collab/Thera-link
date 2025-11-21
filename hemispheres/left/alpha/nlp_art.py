# hemispheres/left/alpha/nlp_art.py
from transformers import pipeline
from ontology.fusion_hub import OntologyHub
import re
import argparse

class LeftAlpha:
    def __init__(self):
        self.hub = OntologyHub()
        # Tiny but powerful model — runs everywhere
        self.pipe = pipeline(
            "text-generation",
            model="microsoft/Phi-3-mini-4k-instruct",
            torch_dtype="auto",
            device_map="auto"
        )

    def heal(self, prompt: str) -> str:
        template = f"""You are a gentle, relational therapist. 
Reframe the following pain into an empowering story of growth and interconnection:

{prompt}

Answer in warm, first-person language."""
        
        out = self.pipe(template, max_new_tokens=200, do_sample=True, temperature=0.7)[0]["generated_text"]
        
        # Simple ART-style reframe
        out = re.sub(r"negative\s+memory", "sacred lesson", out, flags=re.I)
        out = re.sub(r"trauma", "initiation", out, flags=re.I)
        
        return out.split("Answer in warm")[0].strip()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--pain", type=str, default="I feel broken and alone")
    args = p.parse_args()
    
    brain = LeftAlpha()
    result = brain.heal(args.pain)
    print("\nLeft (Analytical) Healing:\n")
    print(result)
