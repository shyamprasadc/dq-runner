from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class BaseFixer(ABC):
    @classmethod
    @abstractmethod
    def action_type(cls) -> str:
        raise NotImplementedError

    @abstractmethod
    def apply(self, df: pd.DataFrame, column: str | None, action: dict) -> pd.DataFrame:
        raise NotImplementedError
