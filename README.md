# schism-ai-experiment

SCHISM modeling and SST prediction experiments with AI integration.

## Files

- `hello.py`: prints `hellow wold`
- `download_schism.py`: downloads the official SCHISM source ZIP from GitHub and extracts it into the current directory
- `download_intel_fortran.py`: downloads Intel Fortran Essentials offline installer for Windows or Linux

## Run hello.py

```bash
python hello.py
```

Expected output:

```text
hellow wold
```

## Run download_schism.py

```bash
python download_schism.py
```

What it does:

- Downloads SCHISM source code from the official `schism-dev/schism` repository
- Saves the ZIP file as `schism-master.zip`
- Extracts the source into `schism-master`

## Run download_intel_fortran.py

```bash
python download_intel_fortran.py --os windows
```

Or for Linux:

```bash
python download_intel_fortran.py --os linux
```

Optional output directory:

```bash
python download_intel_fortran.py --os windows --out-dir downloads
```

## Notes

- The SCHISM script downloads source code, not a prebuilt installer
- Building and running SCHISM may require additional compilers and dependencies depending on your environment
- The Intel Fortran installer URLs may change with new releases
