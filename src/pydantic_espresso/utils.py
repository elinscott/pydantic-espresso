"""Utility functions."""

import os
from pathlib import Path


def get_tmp_dir() -> Path:
    """Get the environment variable for the temporary directory."""
    return Path(os.getenv("ESPRESSO_TMPDIR", "./"))


def get_pseudo_dir() -> Path:
    """Get the environment variable for the pseudo directory."""
    return Path(os.getenv("ESPRESSO_PSEUDO", str(Path.home() / "espresso/pseudo")))
