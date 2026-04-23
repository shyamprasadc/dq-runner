from __future__ import annotations

from pathlib import Path

import click

from dq_runner.fixers import list_fixers
from dq_runner.runner import run_pipeline


@click.group()
def cli() -> None:
    """Command line interface for dq-runner."""


@cli.command("run")
@click.option("--source", "source_dir", default="./source", show_default=True, type=click.Path(path_type=Path))
@click.option("--output", "output_dir", default="./output", show_default=True, type=click.Path(path_type=Path))
@click.option("--pre-suite", "pre_suite_path", default="./configs/pre_suite.yaml", show_default=True, type=click.Path(path_type=Path))
@click.option("--post-suite", "post_suite_path", default="./configs/post_suite.yaml", show_default=True, type=click.Path(path_type=Path))
@click.option("--fix-rules", "fix_rules_path", default="./configs/fix_rules.yaml", show_default=True, type=click.Path(path_type=Path))
@click.option("--output-file", default="final_output.csv", show_default=True)
@click.option("--open-docs", is_flag=True, default=False, help="Open Great Expectations data docs after the run.")
def run_command(
    source_dir: Path,
    output_dir: Path,
    pre_suite_path: Path,
    post_suite_path: Path,
    fix_rules_path: Path,
    output_file: str,
    open_docs: bool,
) -> None:
    """Run pre-validation, fixes, post-validation, and write the output CSV."""
    result = run_pipeline(
        source_dir=source_dir,
        output_dir=output_dir,
        pre_suite_path=pre_suite_path,
        post_suite_path=post_suite_path,
        fix_rules_path=fix_rules_path,
        output_file=output_file,
        open_docs=open_docs,
    )

    click.echo(f"Rows processed: {result['record_count']}")
    click.echo(f"Applied actions: {len(result['applied_actions'])}")
    for action in result["applied_actions"]:
        click.echo(f"  - {action}")
    click.echo(f"Output written to: {result['output_path']}")
    click.echo(f"Post-validation passed: {result['post_passed']}")

    raise SystemExit(0 if result["post_passed"] else 1)


@cli.command("list-fixers")
def list_fixers_command() -> None:
    """List all registered fixer types."""
    for fixer_type in list_fixers():
        click.echo(fixer_type)
