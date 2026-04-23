from __future__ import annotations

import hashlib

import pandas as pd

from dq_runner.fixers.base import BaseFixer


class DeduplicateHashFixer(BaseFixer):
    @classmethod
    def action_type(cls) -> str:
        return "deduplicate_hash"

    def apply(self, df: pd.DataFrame, column: str | None, action: dict) -> pd.DataFrame:
        key_column = action["key_column"]
        new_column = action["new_column"]
        columns = action.get("columns", [key_column])

        updated_df = df.copy()
        updated_df["is_duplicate"] = updated_df.duplicated(subset=[key_column], keep=False).astype(int)

        def generate_value(row):
            if row["is_duplicate"] == 1:
                raw_value = "||".join(str(row[col]) for col in columns)
                return hashlib.sha256(raw_value.encode("utf-8")).hexdigest()
            return row[key_column]

        updated_df[new_column] = updated_df.apply(generate_value, axis=1)
        return updated_df
