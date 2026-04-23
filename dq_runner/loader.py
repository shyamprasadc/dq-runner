from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import great_expectations as gx
import yaml
from great_expectations.core.expectation_suite import ExpectationSuite


def load_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as handle:
        if config_path.suffix.lower() == ".json":
            return json.load(handle)
        return yaml.safe_load(handle)


def expectation_class_name(expectation_type: str) -> str:
    return "".join(part.capitalize() for part in expectation_type.split("_"))


def load_suite_from_file(path: str | Path) -> ExpectationSuite:
    config = load_config(path)
    expectations = []

    for expectation in config.get("expectations", []):
        class_name = expectation_class_name(expectation["expectation_type"])
        try:
            expectation_class = getattr(gx.expectations, class_name)
        except AttributeError as exc:
            raise ValueError(
                f"Unsupported expectation type '{expectation['expectation_type']}' in {path}"
            ) from exc
        expectations.append(expectation_class(**expectation.get("kwargs", {})))

    return ExpectationSuite(
        name=config["name"],
        expectations=expectations,
    )


def load_fix_rules(path: str | Path) -> list[dict[str, Any]]:
    config = load_config(path)
    rules = config.get("rules", [])
    if not isinstance(rules, list):
        raise ValueError(f"'rules' must be a list in {path}")
    return rules
