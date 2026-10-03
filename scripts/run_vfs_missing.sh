#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "${SCRIPT_DIR}")"

echo exit | python3 "${ROOT_DIR}/src/shell.py" "${ROOT_DIR}/examples/does_not_exist.csv"
