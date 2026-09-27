#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
output_dir="${COMFYUI_OUTPUT_DIR:-/mnt/hdd/ComfyUIOutput}"
if [[ "$output_dir" != /* || ! -d "$output_dir" || ! -w "$output_dir" ]]; then
    echo 'Error: COMFYUI_OUTPUT_DIR must be an existing, writable absolute directory.' >&2
    exit 1
fi
exec "$repo_dir/.venv/bin/python" "$repo_dir/main.py" \
    --lowvram \
    --output-directory "$output_dir" \
    "$@"
