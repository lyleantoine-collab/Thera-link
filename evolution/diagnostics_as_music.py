# evolution/diagnostics_as_music.py  ← YOU WILL HEAR IT GROW
import torch
import torchaudio
import numpy as np

def dissonance_to_music(dissonance_score):
    freq = 432 if dissonance_score < 0.2 else 220  # A=432 Hz (healing) vs low rumble
    t = np.linspace(0, 3, int(44100 * 3))
    wave = np.sin(2 * np.pi * freq * t) * np.exp(-t*0.5)
    if dissonance_score < 0.1:
        wave += 0.5 * np.sin(2 * np.pi * freq*1.5 * t)  # Major third = joy
    else:
        wave += 0.5 * np.sin(2 * np.pi * freq*1.1 * t)  # Tritone = tension
    
    torchaudio.save(f"evolution/diagnostics_{int(dissonance_score*100)}.wav", torch.tensor(wave).unsqueeze(0), 44100)
    print(f"→ Diagnostic symphony written: {'harmonious' if dissonance_score < 0.2 else 'tense'}")
