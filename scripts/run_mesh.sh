# scripts/run_mesh.sh
#!/bin/bash
cd "$(dirname "$0")/.."

echo "Starting Thera-Link mesh node..."
poetry run python mesh/node.py
