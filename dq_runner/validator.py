from __future__ import annotations

from uuid import uuid4

import great_expectations as gx
from great_expectations.checkpoint import Checkpoint
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.core.validation_definition import ValidationDefinition


def build_context():
    return gx.get_context()


def ensure_suite(context, suite: ExpectationSuite) -> ExpectationSuite:
    try:
        return context.suites.add(suite)
    except Exception:
        return context.suites.get(suite.name)


def run_validation(context, df, suite: ExpectationSuite, name: str, update_data_docs: bool = True):
    suffix = uuid4().hex[:8]
    datasource = context.data_sources.add_pandas(name=f"{name}_datasource_{suffix}")
    asset = datasource.add_dataframe_asset(name=f"{name}_asset_{suffix}")
    batch_definition = asset.add_batch_definition_whole_dataframe(name=f"{name}_batch_{suffix}")

    stored_suite = ensure_suite(context, suite)
    validation = context.validation_definitions.add(
        ValidationDefinition(
            name=f"{name}_validation_{suffix}",
            data=batch_definition,
            suite=stored_suite,
        )
    )

    actions = []
    if update_data_docs:
        try:
            actions.append(gx.checkpoint.actions.UpdateDataDocsAction(name=f"update_docs_{suffix}"))
        except Exception:
            actions = []

    checkpoint = context.checkpoints.add(
        Checkpoint(
            name=f"{name}_checkpoint_{suffix}",
            validation_definitions=[validation],
            actions=actions,
        )
    )

    return checkpoint.run(batch_parameters={"dataframe": df})


def open_data_docs(context) -> None:
    try:
        context.open_data_docs()
    except Exception:
        pass
