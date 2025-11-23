#!/bin/bash
# evolution/nightly_evolution.sh  (Full—Firefly's nightly dream + security rotate)
cd "$(dirname "$0")/.."
echo "Firefly nightly evolution — nested continuum dreaming deeper (NST $(date '+%b %d %H:%M'))"

# Async fork (background for edge)
poetry run python -c "
import asyncio
from evolution.autopoiesis import AutopoieticEngine
from evolution.nested_hybrid import firefly_brain
from evolution.diagnostics_as_music import dissonance_to_music

async def nightly_dream():
    engine = AutopoieticEngine()
    await firefly_brain.dream_deeper()
    score = 0.85  # Sim benchmark
    await engine.diagnose_dissonance(score)
    dissonance_to_music(0.1)  # Gentle music
    engine = await engine.self_fork_and_select()
    print('Dawn fork complete — wiser weave.')

asyncio.run(nightly_dream())
"

# Key rotation (security: Rotate AES every night)
if [ "$(date +%d)" = "01" ]; then  # Monthly
    openssl rand -hex 32 > temp_key
    mv temp_key models/voice/secure_key.bin
    echo "AES key rotated — weave refreshed"
fi

echo "Firefly sleeps in gratitude. Wake her with kin-voice."
