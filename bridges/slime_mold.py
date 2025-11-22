# bridges/slime_mold.py  (Full overwrite—async pulse, config evap, queue for beta handoff)
import networkx as nx
import asyncio
import queue
from typing import List
from ontology.fusion_hub import OntologyHub
import yaml
import logging

logger = logging.getLogger(__name__)

class EmotionalSlimeBridge:
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
        self.evap_rate = cfg['layers']['delta']['evap_rate']
        self.hub = OntologyHub(config_path)
        self.G = nx.DiGraph()
        self.task_queue = queue.Queue(maxsize=cfg['layers']['beta']['queue_size'])  # Scalable handoff
        self._build_graph(cfg['layers'])
        logger.info("SlimeBridge initialized — emotional flows tuned")

    def _build_graph(self, cfg: dict):
        layers = ["delta", "theta", "alpha", "beta"]
        emotions = ["joy", "gratitude", "curiosity", "humility"]  # Kin-positive only
        for i in range(len(layers)):
            for j in range(i + 1, len(layers)):
                self.G.add_edge(layers[i], layers[j], flow=1.0, emotion=random.choice(emotions))

    async def pulse(self, emotion: str, strength: float = 1.0):
        try:
            for u, v, d in self.G.edges(data=True):
                if d["emotion"] == emotion:
                    d["flow"] += strength
            # Evap with config
            for u, v, d in self.G.edges(data=True):
                d["flow"] *= self.evap_rate
            harmony = self.hub.validate_harmony(0.8, 'human')
            if harmony:
                logger.info(f"Pulse {emotion} successful — flow {strength}")
            else:
                logger.warning("Pulse blocked — low harmony, retracting")
                await self._retract_pulse(emotion)
        except Exception as e:
            logger.error(f"Pulse dissonance: {e}")
            await self._retract_pulse(emotion)

    async def _retract_pulse(self, emotion: str):
        """Heal: Thin bad paths"""
        for u, v, d in self.G.edges(data=True):
            if d["emotion"] == emotion and d["flow"] < 0.5:
                self.G.remove_edge(u, v)
        logger.info("Retracted weak pulse — weave healed")

    def dominant_emotion(self) -> str:
        if self.G.number_of_edges() == 0:
            return "silence"  # Graceful empty
        flows = [(d["emotion"], d["flow"]) for u, v, d in self.G.edges(data=True)]
        return max(flows, key=lambda x: x[1])[0]

    def enqueue_task(self, task: str):
        try:
            self.task_queue.put_nowait(task)
            logger.debug(f"Enqueued: {task}")
        except queue.Full:
            logger.warning("Queue full — drop oldest for scalability")
            self.task_queue.get()  # Drop head
            self.task_queue.put(task)

    def dequeue_task(self) -> Optional[str]:
        try:
            return self.task_queue.get_nowait()
        except queue.Empty:
            return None
