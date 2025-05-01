import os
from pathlib import Path

def get_tmp_dir() -> Path:
    return Path(os.getenv("ESPRESSO_TMPDIR", "./"))

def get_pseudo_dir() -> Path:
    return Path(os.getenv("ESPRESSO_PSEUDO", str(Path.home() / "espresso/pseudo")))
