from __future__ import annotations

import pandas as pd

from dq_runner.fixers.base import BaseFixer


class FillDefaultFixer(BaseFixer):
    @classmethod
    def action_type(cls) -> str:
        return "fill_default"

    def apply(self, df: pd.DataFrame, column: str | None, action: dict) -> pd.DataFrame:
        if not column:
            return df

        updated_df = df.copy()
        updated_df[column] = updated_df[column].fillna(action["value"])
        return updated_df
