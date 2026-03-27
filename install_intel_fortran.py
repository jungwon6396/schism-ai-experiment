import argparse
import shlex
import subprocess
from pathlib import Path


WINDOWS_FLAGS = ["-s", "-a", "--silent", "--eula", "accept"]
LINUX_FLAGS = ["-a", "--silent", "--eula", "accept"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Intel Fortran Essentials offline installer."
    )
    parser.add_argument(
        "--os",
        choices=["windows", "linux"],
        required=True,
        help="Target OS installer type.",
    )
    parser.add_argument(
        "--installer",
        required=True,
        help="Path to the downloaded offline installer (.exe or .sh).",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually run the installer (otherwise prints the command).",
    )
    parser.add_argument(
        "--sudo",
        action="store_true",
        help="Use sudo on Linux.",
    )
    return parser.parse_args()


def build_command(os_name: str, installer: Path, use_sudo: bool) -> list[str]:
    if os_name == "windows":
        return [str(installer)] + WINDOWS_FLAGS

    cmd = ["sh", str(installer)] + LINUX_FLAGS
    if use_sudo:
        cmd = ["sudo"] + cmd
    return cmd


def main() -> None:
    args = parse_args()
    installer = Path(args.installer).expanduser().resolve()

    if not installer.exists():
        raise FileNotFoundError(f"Installer not found: {installer}")

    command = build_command(args.os, installer, args.sudo)

    printable = " ".join(shlex.quote(part) for part in command)
    print("Installer command:")
    print(printable)

    if not args.execute:
        print("Dry run only. Re-run with --execute to start installation.")
        return

    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
