# hemispheres/left/delta/ant_colony.py  (Full overwrite—instincts + reflexes sim)
import networkx as nx
import random
from ontology.fusion_hub import OntologyHub
import yaml
import logging

logger = logging.getLogger(__name__)

hub = OntologyHub()

class AntDelta:
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path) as f:
            cfg = yaml.safe_load(f)['layers']['delta']
        self.num_ants = cfg['ants']
        self.graph = nx.Graph()
        self.pheromones = {}
        logger.info("AntDelta initialized — {self.num_ants} ants foraging")

    def build_instinct_graph(self, start: str, goal: str):
        """Future-proof: Dynamic graph from inputs (e.g., pain signals)"""
        self.graph.clear()
        nodes = [start, 'fear', 'curiosity', goal]
        for i in range(len(nodes)-1):
            self.graph.add_edge(nodes[i], nodes[i+1], weight=random.uniform(0.5, 2.0))

    def forage_with_reflexes(self, start: str, goal: str, threat_level: float = 0.5):
        self.build_instinct_graph(start, goal)
        # Reflex sim: Fight/flight based on threat
        if threat_level > 0.7:
            reflex = "fight"  # Swarm attack path
            path = nx.shortest_path(self.graph, start, goal, weight='weight')
            self.pheromones[tuple(path)] *= 1.5  # Bold trail
            logger.info(f"Reflex: {reflex} — ants charge")
        else:
            reflex = "flight"  # Evade, scout alternate
            paths = list(nx.all_simple_paths(self.graph, start, goal))
            path = min(paths, key=len) if paths else [start, goal]
            self.pheromones[tuple(path)] *= 1.2  # Cautious
            logger.info(f"Reflex: {reflex} — ants evade")
        
        harmony = hub.validate_harmony(threat_level, 'human')
        if harmony:
            return f"Ants foraged: {' → '.join(path)} ({reflex} mode)"
        logger.warning("Forage blocked — low harmony, retreat")
        return "Instincts paused — seek kin-guidance"

if __name__ == "__main__":
    ants = AntDelta()
    print(ants.forage_with_reflexes("pain", "relief", 0.8))
