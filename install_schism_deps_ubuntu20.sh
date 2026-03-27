#!/usr/bin/env sh
set -eu

if [ "$(id -u)" -ne 0 ]; then
  if command -v sudo >/dev/null 2>&1; then
    exec sudo -E sh "$0" "$@"
  fi
  echo "This script needs root privileges (sudo)." >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive

PACKAGES="\
  build-essential \
  gfortran \
  make \
  cmake \
  pkg-config \
  openmpi-bin \
  libopenmpi-dev \
  libnetcdf-dev \
  libnetcdff-dev \
  libhdf5-dev \
  python3 \
  perl\
"

missing=""
for pkg in $PACKAGES; do
  if ! dpkg -s "$pkg" >/dev/null 2>&1; then
    missing="$missing $pkg"
  fi
done

if [ -z "$missing" ]; then
  echo "All required packages are already installed."
  exit 0
fi

echo "Installing missing packages:$missing"
apt-get update -y
apt-get install -y $missing

echo "Done."
