#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo exit | python3 "${SCRIPT_DIR}/../src/shell.py" "${SCRIPT_DIR}/../examples/vfs.csv"
