# dq-runner

A plug-and-play data quality framework built on Great Expectations and Pandas, driven by YAML or JSON configs.

## Quick Start

```bash
uv sync
uv run dq-runner run
```

Full example:

```bash
uv run dq-runner run \
  --source ./source \
  --output ./output \
  --pre-suite ./configs/pre_suite.yaml \
  --post-suite ./configs/post_suite.yaml \
  --fix-rules ./configs/fix_rules.yaml \
  --output-file final_output.csv \
  --open-docs
```

List built-in fixers:

```bash
uv run dq-runner list-fixers
```

Programmatic usage:

```python
from dq_runner import run

df_fixed, post_passed = run(
    source_dir="./source",
    output_dir="./output",
    pre_suite_path="./configs/pre_suite.yaml",
    post_suite_path="./configs/post_suite.yaml",
    fix_rules_path="./configs/fix_rules.yaml",
)
```

## Project Structure

```text
dq-runner/
├── pyproject.toml
├── README.md
├── configs/
│   ├── fix_rules.yaml
│   ├── post_suite.yaml
│   └── pre_suite.yaml
├── output/
├── source/
└── dq_runner/
    ├── __init__.py
    ├── cli.py
    ├── fix_engine.py
    ├── loader.py
    ├── runner.py
    ├── validator.py
    └── fixers/
        ├── __init__.py
        ├── base.py
        ├── dedup.py
        ├── fill_default.py
        └── nulls.py
```

## Config Reference

`pre_suite.yaml` and `post_suite.yaml` define Great Expectations suites:

```yaml
name: my_suite
expectations:
  - expectation_type: expect_column_values_to_not_be_null
    kwargs:
      column: MyColumn
```

`fix_rules.yaml` maps failed expectations to fixer actions:

```yaml
rules:
  - condition:
      expectation: expect_column_values_to_be_unique
      column: MyColumn
    action:
      type: deduplicate_hash
      key_column: MyColumn
      new_column: MyColumn_New
      columns: ["MyColumn", "source"]
```

## Extending

Create a new fixer under `dq_runner/fixers/`, register it in `dq_runner/fixers/__init__.py`, and reference its `type` from your rule config.
