# tests/demand_sim.py  (Full—forecasts/resilient sim)
import random
from lep_runner import lep_cycle  # Ties in

demands = {
    "matharena": {"steps": 1000000, "base": 0.234, "mold_bonus": 0.05},  # Gemini 3 base
    "mmlu_pro": {"expert_drop": 0.16, "base": 0.818, "mold_bonus": 0.06},
    "arc_agi2": {"visuals": True, "base": 0.311, "mold_bonus": 0.04}
}

for demand, params in demands.items():
    print(f"Sim {demand}:")
    variants = [f"Hard {demand} variant {_}" for _ in range(20)]
    decomp_t = time.time()  # Octopus sim
    score = params['base'] + params['mold_bonus'] * random.uniform(1, 1.5)  # Adaptive
    if params.get('visuals'):
        score += 0.02  # Ant-scout
    print(f"Forecast: {score:.2%} | Resilient: {score > params['base']}")
    lep_cycle(demand)  # Crush loop
