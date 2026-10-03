#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "${SCRIPT_DIR}")"

mkdir -p "${ROOT_DIR}/output"
python3 "${ROOT_DIR}/src/shell.py" "${ROOT_DIR}/examples/vfs_minimal.csv" "${ROOT_DIR}/examples/startup_vfs.txt"
