#!/usr/bin/env sh
set -eu

check_cmd() {
  name="$1"
  cmd="$2"
  if command -v "$cmd" >/dev/null 2>&1; then
    printf "[OK] %s -> %s\n" "$name" "$(command -v "$cmd")"
  else
    printf "[MISSING] %s\n" "$name"
  fi
}

check_info_cmd() {
  name="$1"
  cmd="$2"
  if command -v "$cmd" >/dev/null 2>&1; then
    printf "[OK] %s\n" "$name"
  else
    printf "[MISSING] %s\n" "$name"
  fi
}

printf "SCHISM prerequisites check\n"
printf "==========================\n"

# Fortran compiler (Intel or others)
if command -v ifx >/dev/null 2>&1; then
  printf "[OK] Intel Fortran (ifx) -> %s\n" "$(command -v ifx)"
elif command -v ifort >/dev/null 2>&1; then
  printf "[OK] Intel Fortran (ifort) -> %s\n" "$(command -v ifort)"
elif command -v gfortran >/dev/null 2>&1; then
  printf "[OK] GNU Fortran (gfortran) -> %s\n" "$(command -v gfortran)"
else
  printf "[MISSING] Fortran compiler (ifx/ifort/gfortran)\n"
fi

# MPI wrappers
check_cmd "MPI Fortran wrapper" "mpif90"
check_cmd "MPI C wrapper" "mpicc"

# NetCDF
if command -v nc-config >/dev/null 2>&1; then
  printf "[OK] NetCDF (nc-config) -> %s\n" "$(command -v nc-config)"
elif command -v nf-config >/dev/null 2>&1; then
  printf "[OK] NetCDF Fortran (nf-config) -> %s\n" "$(command -v nf-config)"
elif command -v pkg-config >/dev/null 2>&1 && pkg-config --exists netcdf; then
  printf "[OK] NetCDF (pkg-config)\n"
else
  printf "[MISSING] NetCDF (nc-config/nf-config or pkg-config netcdf)\n"
fi

# Python and Perl
check_cmd "Python" "python3"
check_cmd "Perl" "perl"

# Build tools
check_cmd "GNU Make" "make"
check_cmd "CMake" "cmake"

printf "==========================\n"
printf "Done.\n"
