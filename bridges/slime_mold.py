# bridges/slime_mold.py
import networkx as nx
import random

class SlimeBridge:
    def __init__(self):
        self.G = nx.DiGraph()
        layers = ["delta", "theta", "alpha", "beta"]
        for i in range(len(layers)):
            for j in range(i + 1, len(layers)):
                self.G.add_edge(layers[i], layers[j], flow=1.0)

    def pulse(self, from_layer: str, to_layer: str, strength: float = 1.0):
        if self.G.has_edge(from_layer, to_layer):
            self.G[from_layer][to_layer]["flow"] += strength
        # evaporate a little everywhere
        for u, v in self.G.edges():
            self.G[u][v]["flow"] *= 0.99

    def best_path(self, start: str, end: str):
        try:
            path = nx.shortest_path(self.G, start, end, weight=lambda u,v,e: 1/e["flow"])
            return path
        except nx.NetworkXNoPath:
            return [start, end]  # fallback
