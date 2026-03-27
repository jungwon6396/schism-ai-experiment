#!/usr/bin/env python3
"""Build SCHISM from source using CMake or GNU Make.

Examples:
  python compile_schism.py --source-dir schism-master
  python compile_schism.py --source-dir schism-master --generator Ninja
  python compile_schism.py --source-dir schism-master --method make --target pschism
  python compile_schism.py --source-dir schism-master --dry-run
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile SCHISM source code")
    parser.add_argument(
        "--source-dir",
        default="schism-master",
        help="Path to SCHISM source tree (default: %(default)s)",
    )
    parser.add_argument(
        "--method",
        choices=("cmake", "make"),
        default="cmake",
        help="Build method to use (default: %(default)s)",
    )
    parser.add_argument(
        "--build-dir",
        default="build",
        help="Out-of-source build directory when using CMake (default: %(default)s)",
    )
    parser.add_argument(
        "--generator",
        default=None,
        help="Optional CMake generator (example: Ninja)",
    )
    parser.add_argument(
        "--target",
        default=None,
        help="Optional build target (example: pschism)",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=0,
        help="Parallel build jobs. 0 means let build tool choose.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without executing them",
    )
    return parser.parse_args()


def require_tool(name: str) -> None:
    if shutil.which(name):
        return
    print(f"Error: required tool '{name}' was not found in PATH.", file=sys.stderr)
    raise SystemExit(2)


def find_cmake_source_root(source_dir: Path) -> Path:
    if (source_dir / "CMakeLists.txt").is_file():
        return source_dir

    src_dir = source_dir / "src"
    if (src_dir / "CMakeLists.txt").is_file():
        return src_dir

    print(
        "Error: could not find CMakeLists.txt in source directory or source/src.",
        file=sys.stderr,
    )
    raise SystemExit(2)


def run_command(command: List[str], cwd: Path | None, dry_run: bool) -> None:
    display_cwd = str(cwd) if cwd else str(Path.cwd())
    print(f"$ (cd {display_cwd} && {' '.join(command)})")
    if dry_run:
        return
    subprocess.run(command, cwd=cwd, check=True)


def cmake_build(args: argparse.Namespace, source_dir: Path) -> None:
    require_tool("cmake")

    cmake_root = find_cmake_source_root(source_dir)
    build_dir = source_dir / args.build_dir
    build_dir.mkdir(parents=True, exist_ok=True)

    configure_cmd = ["cmake", "-S", str(cmake_root), "-B", str(build_dir)]
    if args.generator:
        configure_cmd.extend(["-G", args.generator])

    build_cmd = ["cmake", "--build", str(build_dir)]
    if args.target:
        build_cmd.extend(["--target", args.target])
    if args.jobs > 0:
        build_cmd.extend(["-j", str(args.jobs)])

    run_command(configure_cmd, cwd=None, dry_run=args.dry_run)
    run_command(build_cmd, cwd=None, dry_run=args.dry_run)


def make_build(args: argparse.Namespace, source_dir: Path) -> None:
    require_tool("make")

    makefile_candidates = [source_dir / "Makefile", source_dir / "src" / "Makefile"]
    make_root = next((path.parent for path in makefile_candidates if path.is_file()), None)
    if make_root is None:
        print(
            "Error: could not find Makefile in source directory or source/src.",
            file=sys.stderr,
        )
        raise SystemExit(2)

    command = ["make"]
    if args.jobs > 0:
        command.append(f"-j{args.jobs}")
    if args.target:
        command.append(args.target)

    run_command(command, cwd=make_root, dry_run=args.dry_run)


def main() -> None:
    args = parse_args()
    source_dir = Path(args.source_dir).expanduser().resolve()
    if not source_dir.is_dir():
        print(f"Error: source directory does not exist: {source_dir}", file=sys.stderr)
        raise SystemExit(2)

    print(f"Using source directory: {source_dir}")
    if args.method == "cmake":
        cmake_build(args, source_dir)
    else:
        make_build(args, source_dir)

    print("Build step completed.")


if __name__ == "__main__":
    main()
