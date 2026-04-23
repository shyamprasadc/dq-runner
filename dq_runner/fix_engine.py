from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from dq_runner.fixers import get_fixer


@dataclass(frozen=True)
class ValidationFailure:
    expectation: str
    column: str | None
    kwargs: dict[str, Any]


def extract_failures(validation_result: Any) -> list[ValidationFailure]:
    failures: list[ValidationFailure] = []

    for run in validation_result.run_results.values():
        for result in run.results:
            if result.success:
                continue
            kwargs = dict(result.expectation_config.kwargs)
            failures.append(
                ValidationFailure(
                    expectation=result.expectation_config.type,
                    column=kwargs.get("column"),
                    kwargs=kwargs,
                )
            )

    return failures


def rule_matches(rule: dict[str, Any], failure: ValidationFailure) -> bool:
    condition = rule.get("condition", {})
    if condition.get("expectation") != failure.expectation:
        return False

    condition_column = condition.get("column")
    if condition_column is not None and condition_column != failure.column:
        return False

    condition_columns = condition.get("columns")
    if condition_columns is not None:
        failure_columns = failure.kwargs.get("column_list")
        if condition_columns != failure_columns:
            return False

    return True


def apply_fixes(
    df: pd.DataFrame,
    validation_result: Any,
    rules: list[dict[str, Any]],
) -> tuple[pd.DataFrame, list[str]]:
    working_df = df.copy()
    applied_actions: list[str] = []

    for failure in extract_failures(validation_result):
        for rule in rules:
            if not rule_matches(rule, failure):
                continue

            action = rule.get("action", {})
            fixer = get_fixer(action["type"])
            working_df = fixer.apply(working_df, failure.column, action)
            applied_actions.append(
                f"{action['type']} for {failure.expectation}"
                + (f" on {failure.column}" if failure.column else "")
            )

    return working_df, applied_actions
