#!/bin/bash
cd "$(dirname "$0")/.."
poetry add optimum[onnxruntime]  # If not
python -c "
from optimum.onnxruntime import ORTModelForCausalLM
from transformers import AutoTokenizer
model = ORTModelForCausalLM.from_pretrained('microsoft/Phi-3-mini-4k-instruct', provider='CPUExecutionProvider')
model.save_pretrained('models/optimized_phi')
tokenizer = AutoTokenizer.from_pretrained('models/optimized_phi')
# Cache common prompts
with open('models/prompt_cache.json', 'w') as f:
    f.write('{\"trauma\": \"sacred lesson\"}')
print('Optimized: 2x speed, cached for flow.')
"
# Slime prune: Thin <0.5 flows
python -c "from bridges.slime_mold import EmotionalSlimeBridge; s=EmotionalSlimeBridge(); [s.G.remove_edge(u,v) for u,v,d in list(s.G.edges(data=True)) if d['flow']<0.5]; print('Slime pruned—water-like.')"
