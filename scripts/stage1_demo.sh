#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "${SCRIPT_DIR}")"

printf 'ls -la /home/user\ncd projects\nfoobar\nexit\n' | python3 "${ROOT_DIR}/src/shell.py"
