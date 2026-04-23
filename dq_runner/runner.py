from __future__ import annotations

from pathlib import Path

import pandas as pd

from dq_runner.fix_engine import apply_fixes
from dq_runner.loader import load_fix_rules, load_suite_from_file
from dq_runner.validator import build_context, open_data_docs, run_validation


def load_source_data(source_dir: str | Path) -> pd.DataFrame:
    source_path = Path(source_dir)
    csv_files = sorted(source_path.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {source_path}")

    dataframes = []
    for csv_file in csv_files:
        frame = pd.read_csv(csv_file)
        frame["source"] = csv_file.stem
        dataframes.append(frame)

    return pd.concat(dataframes, ignore_index=True)


def write_output(df: pd.DataFrame, output_dir: str | Path, output_file: str) -> Path:
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    output_path = target_dir / output_file
    df.to_csv(output_path, index=False)
    return output_path


def run_pipeline(
    source_dir: str | Path = "./source",
    output_dir: str | Path = "./output",
    pre_suite_path: str | Path = "./configs/pre_suite.yaml",
    post_suite_path: str | Path = "./configs/post_suite.yaml",
    fix_rules_path: str | Path = "./configs/fix_rules.yaml",
    output_file: str = "final_output.csv",
    open_docs: bool = False,
):
    context = build_context()
    pre_suite = load_suite_from_file(pre_suite_path)
    post_suite = load_suite_from_file(post_suite_path)
    rules = load_fix_rules(fix_rules_path)
    df = load_source_data(source_dir)

    pre_result = run_validation(context, df, pre_suite, name="pre")
    df_fixed, applied_actions = apply_fixes(df, pre_result, rules)
    post_result = run_validation(context, df_fixed, post_suite, name="post")

    output_path = write_output(df_fixed, output_dir, output_file)
    post_passed = bool(getattr(post_result, "success", False))

    if open_docs:
        open_data_docs(context)

    return {
        "dataframe": df_fixed,
        "output_path": output_path,
        "pre_result": pre_result,
        "post_result": post_result,
        "post_passed": post_passed,
        "applied_actions": applied_actions,
        "record_count": len(df_fixed),
    }


def run(
    source_dir: str | Path = "./source",
    output_dir: str | Path = "./output",
    pre_suite_path: str | Path = "./configs/pre_suite.yaml",
    post_suite_path: str | Path = "./configs/post_suite.yaml",
    fix_rules_path: str | Path = "./configs/fix_rules.yaml",
    output_file: str = "final_output.csv",
    open_docs: bool = False,
):
    result = run_pipeline(
        source_dir=source_dir,
        output_dir=output_dir,
        pre_suite_path=pre_suite_path,
        post_suite_path=post_suite_path,
        fix_rules_path=fix_rules_path,
        output_file=output_file,
        open_docs=open_docs,
    )
    return result["dataframe"], result["post_passed"]
