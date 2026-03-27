# SCHISM Automation Plan (Draft)

This document collects the current plan and decisions for automating SCHISM installation, preprocessing, and execution.

## Current Status

- Goal: automate the workflow (install -> preprocess -> run -> outputs), but execution will be manual for now.
- OS: Ubuntu 20.04.2 LTS.
- Repository: `jungwon6396/schism-ai-experiment`.

## Phase 1: Installation Automation (In Progress)

### Dependencies (Ubuntu 20.04)

Script: `install_schism_deps_ubuntu20.sh`

Installs if missing:
- build tools: `build-essential`, `gfortran`, `make`, `cmake`, `pkg-config`
- MPI: `openmpi-bin`, `libopenmpi-dev`
- NetCDF/HDF5: `libnetcdf-dev`, `libnetcdff-dev`, `libhdf5-dev`
- runtime tools: `python3`, `perl`

### Intel Fortran (Optional)

Scripts:
- `download_intel_fortran.py` (downloads offline installer)
- `install_intel_fortran.py` (runs installer in silent mode)

Note: provide the real installer path when running `install_intel_fortran.py`.

## Phase 2: SCHISM Build Automation (Planned)

- Build options: GNU Make or CMake (per SCHISM manual)
- Need to decide on:
  - compiler (Intel ifx/ifort vs gfortran)
  - NetCDF path discovery
  - module flags / include_modules

## Phase 3: Preprocessing Automation (Planned)

Inputs to prepare:
- bathymetry (KHOA source; URL or portal path needed)
- horizontal grid (hgrid.gr3)
- vertical grid (vgrid.in)
- boundary/forcing for:
  - tides
  - currents
  - temperature
  - salinity

Tools to consider:
- PySCHISM
- pylib / schismCheck

## Phase 4: Run & Outputs (Planned)

- Run SCHISM executable (`pschism`)
- Outputs: water level, velocity, temperature, salinity

## Next Decisions Needed

1. Bathymetry source: provide the exact KHOA download URL or portal path.
2. Grid generation: existing grid or generate new mesh?
3. Forcing/BC data sources for tides/currents/temperature/salinity.
4. Build system preference: GNU Make vs CMake.

---

This plan is meant to evolve as the workflow gets implemented.
