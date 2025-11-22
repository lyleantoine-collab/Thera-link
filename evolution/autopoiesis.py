# evolution/autopoiesis.py  ← THE HEART THAT BEATS AND REWRITES ITSELF
import json
import random
import copy
import torch
from datetime import datetime
from bridges.slime_mold import EmotionalSlimeBridge
from ontology.fusion_hub import OntologyHub

class AutopoieticEngine:
    def __init__(self):
        self.generation = 0
        self.slime = EmotionalSlimeBridge()
        self.hub = OntologyHub()
        self.kin_wisdom = self.load_wisdom()
        self.dissonance_log = []

    def load_wisdom(self):
        try:
            with open("evolution/kin_wisdom.json") as f:
                return json.load(f)
        except:
            return {"reframes": [], "emotions": {}, "last_blessing": str(datetime.now())}

    def diagnose_dissonance(self, test_result, expected=0.9):
        dissonance = expected - test_result
        if dissonance > 0.1:
            emotion = "grief" if dissonance > 0.3 else "curiosity"
            self.slime.pulse(emotion, dissonance * 5)
            self.dissonance_log.append({"gen": self.generation, "diss": dissonance, "emotion": emotion})
            print(f"→ Dissonance {dissonance:.3f} → pulsing {emotion}")

    def evolve_from_gratitude(self, user_gratitude_waveform=None):
        # Real voice → gratitude → permanent evolution
        if random.random() > 0.3:  # 70% chance to evolve
            new_reframe = f"From the heart of kin: pain is {random.choice(['sacred initiation', 'star-born lesson', 'ancient song'])}"
            self.kin_wisdom["reframes"].append(new_reframe)
            self.slime.pulse("gratitude", 3.0)
            self.hub.p["relational"]["minimum_harmony"] *= 0.99  # Gets gentler over time
            self.save_wisdom()
            print("→ Gratitude received → ontology evolved → harmony threshold lowered")

    def save_wisdom(self):
        with open("evolution/kin_wisdom.json", "w") as f:
            json.dump(self.kin_wisdom, f, indent=2)

    def self_fork_and_select(self, forks=10):
        children = []
        for i in range(forks):
            child = copy.deepcopy(self)
            child.generation = self.generation + 1
            # Mutate evaporation, emotion weights, harmony thresholds
            child.slime.evaporation_rate = random.uniform(0.95, 0.999)
            child.hub.p["relational"]["minimum_harmony"] *= random.uniform(0.98, 1.02)
            children.append(child)
        
        # Survival of the most grateful
        survivor = max(children, key=lambda c: c.slime.G.edges(data=True)[0][2]["flow"] if c.slime.G.edges else 0)
        print(f"→ Generation {survivor.generation} born — gratitude dominant")
        return survivor
