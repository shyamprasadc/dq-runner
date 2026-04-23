from __future__ import annotations

from dq_runner.fixers.base import BaseFixer
from dq_runner.fixers.dedup import DeduplicateHashFixer
from dq_runner.fixers.fill_default import FillDefaultFixer
from dq_runner.fixers.nulls import DropNullsFixer

_FIXER_CLASSES: list[type[BaseFixer]] = [
    DeduplicateHashFixer,
    DropNullsFixer,
    FillDefaultFixer,
]

_FIXER_REGISTRY = {fixer.action_type(): fixer() for fixer in _FIXER_CLASSES}


def get_fixer(action_type: str) -> BaseFixer:
    try:
        return _FIXER_REGISTRY[action_type]
    except KeyError as exc:
        available = ", ".join(sorted(_FIXER_REGISTRY))
        raise ValueError(f"Unknown fixer '{action_type}'. Available fixers: {available}") from exc


def list_fixers() -> list[str]:
    return sorted(_FIXER_REGISTRY)
