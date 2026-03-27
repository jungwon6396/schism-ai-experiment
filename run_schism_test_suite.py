#!/usr/bin/env python3
"""Download and run SCHISM verification tests.

The official SCHISM manual documents that the verification tests are
distributed via SVN:
https://schism-dev.github.io/schism/master/getting-started/test_suite.html
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_TEST_SUITE_URL = "https://columbia.vims.edu/schism/schism_verification_tests"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Checkout/update and run SCHISM verification tests"
    )
    parser.add_argument(
        "--tests-url",
        default=DEFAULT_TEST_SUITE_URL,
        help="SVN URL for SCHISM verification tests (default: %(default)s)",
    )
    parser.add_argument(
        "--tests-dir",
        default="schism_verification_tests",
        help="Local directory for the test suite checkout (default: %(default)s)",
    )
    parser.add_argument(
        "--case",
        default="Test_QuarterAnnulus",
        help=(
            "Case name to run. The script searches recursively for a folder with this "
            "exact name (default: %(default)s)."
        ),
    )
    parser.add_argument(
        "--run-script",
        default="run_test",
        help=(
            "Runner script basename to execute inside the case directory. "
            "The script tries '<name>' then '<name>.sh' (default: %(default)s)."
        ),
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="If tests-dir exists, run 'svn update' instead of skipping checkout",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without executing them",
    )
    return parser.parse_args()


def run_command(command: list[str], cwd: Path | None, dry_run: bool) -> None:
    display_cwd = str(cwd) if cwd else str(Path.cwd())
    print(f"$ (cd {display_cwd} && {' '.join(command)})")
    if dry_run:
        return
    subprocess.run(command, cwd=cwd, check=True)


def require_tool(name: str) -> None:
    if shutil.which(name):
        return
    print(
        f"Error: required tool '{name}' was not found in PATH. Install it and retry.",
        file=sys.stderr,
    )
    raise SystemExit(2)


def checkout_or_update_tests(
    tests_url: str, tests_dir: Path, update: bool, dry_run: bool
) -> None:
    if not dry_run:
        require_tool("svn")

    if tests_dir.exists():
        if update:
            run_command(["svn", "update"], cwd=tests_dir, dry_run=dry_run)
        else:
            print(f"Using existing tests directory: {tests_dir}")
        return

    run_command(["svn", "co", tests_url, str(tests_dir)], cwd=None, dry_run=dry_run)


def find_case_dir(tests_dir: Path, case_name: str) -> Path:
    candidates = sorted(path for path in tests_dir.rglob(case_name) if path.is_dir())
    if not candidates:
        print(
            f"Error: could not find case directory named '{case_name}' under {tests_dir}",
            file=sys.stderr,
        )
        raise SystemExit(2)
    if len(candidates) > 1:
        print(
            "Info: multiple matches found; using the first one:\n"
            + "\n".join(f"  - {path}" for path in candidates[:10])
        )
    return candidates[0]


def resolve_runner_script(case_dir: Path, run_script: str) -> Path:
    candidates = [case_dir / run_script, case_dir / f"{run_script}.sh"]
    for path in candidates:
        if path.is_file():
            return path
    print(
        f"Error: could not find runner script '{run_script}' or '{run_script}.sh' in {case_dir}",
        file=sys.stderr,
    )
    raise SystemExit(2)


def main() -> None:
    args = parse_args()
    tests_dir = Path(args.tests_dir).expanduser().resolve()

    checkout_or_update_tests(
        tests_url=args.tests_url,
        tests_dir=tests_dir,
        update=args.update,
        dry_run=args.dry_run,
    )
    if args.dry_run and not tests_dir.exists():
        print(
            "Dry run note: test suite directory does not exist yet, so case discovery is skipped."
        )
        print("Test run step completed.")
        return

    case_dir = find_case_dir(tests_dir, args.case)
    print(f"Selected case directory: {case_dir}")

    runner_script = resolve_runner_script(case_dir, args.run_script)
    run_command(["sh", runner_script.name], cwd=case_dir, dry_run=args.dry_run)
    print("Test run step completed.")


if __name__ == "__main__":
    main()
