# schism-ai-experiment

SCHISM modeling and SST prediction experiments with AI integration.

## Files

- `hello.py`: prints `hellow wold`
- `download_schism.py`: downloads the official SCHISM source ZIP from GitHub and extracts it into the current directory
- `download_intel_fortran.py`: downloads Intel Fortran Essentials offline installer for Windows or Linux
- `install_intel_fortran.py`: runs the Intel Fortran Essentials offline installer in silent mode
- `check_schism_prereqs.sh`: checks whether SCHISM build prerequisites are installed
- `install_schism_deps_ubuntu20.sh`: installs SCHISM build dependencies on Ubuntu 20.04 if missing
- `compile_schism.py`: compiles SCHISM from local source using CMake (default) or Make

## Check Linux distribution

```bash
cat /etc/os-release
```

Or a more concise command:

```bash
. /etc/os-release && echo "$PRETTY_NAME"
```

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

## Run install_intel_fortran.py

```bash
python install_intel_fortran.py --os windows --installer C:\path\to\intel-fortran-essentials-2025.x.x_offline.exe --execute
```

Or for Linux:

```bash
python install_intel_fortran.py --os linux --installer /path/to/intel-fortran-essentials-2025.x.x_offline.sh --execute
```

Linux with sudo:

```bash
python install_intel_fortran.py --os linux --installer /path/to/intel-fortran-essentials-2025.x.x_offline.sh --execute --sudo
```

Dry run (prints the command without installing):

```bash
python install_intel_fortran.py --os windows --installer C:\path\to\intel-fortran-essentials-2025.x.x_offline.exe
```

## Run install_schism_deps_ubuntu20.sh

```bash
chmod +x install_schism_deps_ubuntu20.sh
./install_schism_deps_ubuntu20.sh
```

This will install missing packages for Ubuntu 20.04:

- `build-essential`, `gfortran`, `make`, `cmake`, `pkg-config`
- `openmpi-bin`, `libopenmpi-dev`
- `libnetcdf-dev`, `libnetcdff-dev`, `libhdf5-dev`
- `python3`, `perl`


## Run compile_schism.py

```bash
python compile_schism.py --source-dir schism-master
```

Optional flags:

```bash
# Use GNU Make instead of CMake
python compile_schism.py --source-dir schism-master --method make

# Build a specific target
python compile_schism.py --source-dir schism-master --target pschism

# Use parallel jobs
python compile_schism.py --source-dir schism-master --jobs 8

# Pass extra arguments to CMake configure (repeatable)
python compile_schism.py --source-dir schism-master \
  --cmake-arg=-DCMAKE_Fortran_FLAGS=-I/usr/include

# Preview commands without running compilation
python compile_schism.py --source-dir schism-master --dry-run
```

What it does:

- Validates the source directory exists
- Detects build files (`CMakeLists.txt` or `Makefile`)
- Runs configure/build commands and prints each command before execution
- Supports passing additional configure flags to CMake via repeatable `--cmake-arg`

## SCHISM build requirements (besides Intel Fortran)

According to the SCHISM compilation guide, these are typically required in addition to a Fortran compiler:

- C compiler and MPI wrappers (`mpif90`, `mpicc`)
- NetCDF library (NetCDF-4 recommended)
- Python and Perl
- Build system: GNU Make or CMake

## Run check_schism_prereqs.sh

```bash
chmod +x check_schism_prereqs.sh
./check_schism_prereqs.sh
```

This will report whether the following are installed:

- Fortran compiler (ifx/ifort/gfortran)
- `mpif90` and `mpicc`
- NetCDF (via `nc-config`, `nf-config`, or `pkg-config netcdf`)
- `python3` and `perl`
- `make` and `cmake`

## Notes

- The SCHISM script downloads source code, not a prebuilt installer
- Building and running SCHISM may require additional compilers and dependencies depending on your environment
- The Intel Fortran installer URLs may change with new releases
