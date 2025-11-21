#!/bin/bash
# scripts/run_with_awareness.sh
cd "$(dirname "$0")/.."
poetry install --no-interaction > /dev/null

echo ""
echo "Thera-Link + Today's Self-Awareness Paper Demo"
echo "================================================"
echo "1. Talking to a HUMAN (you)"
poetry run python -c "
from ontology.fusion_hub import OntologyHub
hub = OntologyHub()
print('Harmony vs human:', hub.validate_harmony(0.8, 'human'))
"

echo ""
echo "2. Talking to ITSELF"
poetry run python -c "
from ontology.fusion_hub import OntologyHub
hub = OntologyHub()
print('Harmony vs clone:', hub.validate_harmony(0.8, 'self'))
"

echo ""
echo "3. Left Theta strategic depth vs human"
poetry run python hemispheres/left/theta/strategic_reasoning.py

echo ""
echo "Done. Ontological guardrails active."
