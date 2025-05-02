"""Pydantic models for Quantum ESPRESSO inputs."""

from pathlib import Path

versions = sorted(
    [p.name for p in Path(__file__).parent.iterdir() if p.is_dir() and p.name != "__pycache__"]
)

directory = Path(__file__).parent
