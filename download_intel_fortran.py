import argparse
from pathlib import Path
from urllib.request import urlretrieve

WINDOWS_URL = (
    "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/"
    "33676fcf-14a3-4e96-a9b9-72976b1145d9/"
    "intel-fortran-essentials-2025.3.1.25_offline.exe"
)
LINUX_URL = (
    "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/"
    "ce0f9b00-4780-483f-bc09-96d6fb4467ca/"
    "intel-fortran-essentials-2025.3.1.26_offline.sh"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download Intel Fortran Essentials offline installer."
    )
    parser.add_argument(
        "--os",
        choices=["windows", "linux"],
        required=True,
        help="Target OS installer to download.",
    )
    parser.add_argument(
        "--out-dir",
        default=".",
        help="Directory to save the installer.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.os == "windows":
        url = WINDOWS_URL
        filename = Path(WINDOWS_URL).name
    else:
        url = LINUX_URL
        filename = Path(LINUX_URL).name

    out_path = out_dir / filename

    print(f"Downloading Intel Fortran installer for {args.os}...")
    print(f"Source: {url}")
    print(f"Output: {out_path}")

    urlretrieve(url, out_path)

    print("Download complete.")


if __name__ == "__main__":
    main()
