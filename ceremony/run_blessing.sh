#!/bin/bash
cd "$(dirname "$0")/.."
poetry run python ceremony/blessing.py
echo "Mesh officially blessed. It is now a living relative."
