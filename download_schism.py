from pathlib import Path
from urllib.request import urlretrieve
import zipfile

SCHISM_ZIP_URL = "https://codeload.github.com/schism-dev/schism/zip/refs/heads/master"
ZIP_NAME = "schism-master.zip"
EXTRACT_DIR = "schism-master"


def main() -> None:
    base_dir = Path.cwd()
    zip_path = base_dir / ZIP_NAME
    extract_path = base_dir / EXTRACT_DIR

    print(f"Downloading SCHISM from: {SCHISM_ZIP_URL}")
    urlretrieve(SCHISM_ZIP_URL, zip_path)
    print(f"Saved archive to: {zip_path}")

    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(base_dir)

    print(f"Extracted SCHISM source into: {extract_path}")
    print("Download complete.")


if __name__ == "__main__":
    main()
