# hemispheres/right/alpha/sensory_nlp.py
from transformers import pipeline
from ontology.fusion_hub import OntologyHub
import argparse

class RightAlpha:
    def __init__(self):
        self.hub = OntologyHub()
        self.pipe = pipeline(
            "text-generation",
            model="microsoft/Phi-3-mini-4k-instruct",
            torch_dtype="auto",
            device_map="auto"
        )

    def dream(self, prompt: str) -> str:
        template = f"""You are a poetic, intuitive healer. 
Speak to this pain as if it were a dream symbol asking to be integrated:

{prompt}

Use imagery, metaphor, and warmth."""
        
        out = self.pipe(template, max_new_tokens=200, do_sample=True, temperature=0.9)[0]["generated_text"]
        return out.split("Use imagery")[0].strip()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--pain", type=str, default="I feel broken and alone")
    args = p.parse_args()
    
    brain = RightAlpha()
    result = brain.dream(args.pain)
    print("\nRight (Intuitive) Dream:\n")
    print(result)
