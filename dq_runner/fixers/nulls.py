from __future__ import annotations

import pandas as pd

from dq_runner.fixers.base import BaseFixer


class DropNullsFixer(BaseFixer):
    @classmethod
    def action_type(cls) -> str:
        return "drop_nulls"

    def apply(self, df: pd.DataFrame, column: str | None, action: dict) -> pd.DataFrame:
        if not column:
            return df
        return df[df[column].notna()].reset_index(drop=True)
