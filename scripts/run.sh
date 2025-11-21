#!/bin/bash
# scripts/run.sh
cd "$(dirname "$0")/.."
echo "Installing deps..."
poetry install --no-interaction
echo ""
echo "Starting Thera-Link fusion demo..."
poetry run python hemispheres/fusion_demo.py
