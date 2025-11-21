# bridges/slime_mold.py  (replace old version)
import networkx as nx
import random

class EmotionalSlimeBridge:
    def __init__(self):
        self.G = nx.DiGraph()
        layers = ["delta", "theta", "alpha", "beta"]
        emotions = ["joy", "sadness", "anger", "love", "fear", "gratitude"]
        for i in range(len(layers)):
            for j in range(i + 1, len(layers)):
                self.G.add_edge(layers[i], layers[j], flow=1.0, emotion=random.choice(emotions))

    def pulse(self, emotion: str, strength: float = 2.0):
        for u, v, d in self.G.edges(data=True):
            if d["emotion"] == emotion:
                d["flow"] += strength
        # gentle evaporation
        for u, v, d in self.G.edges(data=True):
            d["flow"] *= 0.98

    def dominant_emotion(self):
        flows = [d["flow"] * (1 + random.random()) for u,v,d in self.G.edges(data=True)]
        return max(set([d["emotion"] for u,v,d in self.G.edges(data=True)]), key=flows.count)
