# utils/device_profile.py   ← create this file
import yaml
import os
from pathlib import Path

def load_config() -> dict:
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    profile = os.getenv("THERA_PROFILE", cfg.get("profile", "desktop")).lower()

    if profile == "edge" and "edge_overrides" in cfg:
        print("Edge device profile activated — going feather-light")
        overrides = cfg["edge_overrides"]
        if overrides.get("when") == "edge":
            # Deep-merge overrides
            for section, values in overrides.items():
                if section == "when":
                    continue
                if section not in cfg:
                    cfg[section] = {}
                cfg[section].update(values)

    return cfg

CONFIG = load_config()   # Imported everywhere
