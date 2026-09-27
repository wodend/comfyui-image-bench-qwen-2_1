#!/usr/bin/env bash
set -euo pipefail

# Run from a clean ComfyUI checkout. This script does not replace an existing
# environment or launcher.
if [[ ! -f main.py || ! -f requirements.txt || ! -d models ]]; then
    echo 'Error: run this script from the root of a ComfyUI checkout.' >&2
    exit 1
fi
if [[ -e .venv || -L .venv ]]; then
    echo 'Error: .venv already exists; use a fresh checkout.' >&2
    exit 1
fi
if [[ -e run_comfyui.sh || -L run_comfyui.sh ]]; then
    echo 'Error: run_comfyui.sh already exists; refusing to replace it.' >&2
    exit 1
fi
if [[ -e comfyui-python-lock.txt || -L comfyui-python-lock.txt ]]; then
    echo 'Error: comfyui-python-lock.txt already exists; refusing to replace it.' >&2
    exit 1
fi

python_bin="${COMFYUI_PYTHON:-python3.14}"
if ! command -v "$python_bin" >/dev/null 2>&1; then
    printf 'Error: %s is unavailable. Set COMFYUI_PYTHON to a Python 3.14 interpreter.\n' "$python_bin" >&2
    exit 1
fi
if ! "$python_bin" -c 'import sys; assert sys.version_info[:2] == (3, 14)' 2>/dev/null; then
    echo 'Error: this benchmark setup requires Python 3.14.' >&2
    exit 1
fi
if ! command -v nvidia-smi >/dev/null 2>&1 || ! nvidia-smi -L >/dev/null 2>&1; then
    echo 'Error: an available NVIDIA GPU and driver are required.' >&2
    exit 1
fi

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
output_dir="${COMFYUI_OUTPUT_DIR:-/mnt/hdd/ComfyUIOutput}"
if [[ "$output_dir" != /* ]]; then
    echo 'Error: COMFYUI_OUTPUT_DIR must be an absolute path.' >&2
    exit 1
fi
if [[ "$output_dir" == /mnt/hdd/ComfyUIOutput ]] && ! mountpoint -q /mnt/hdd; then
    echo 'Error: /mnt/hdd is not mounted; set COMFYUI_OUTPUT_DIR to another location.' >&2
    exit 1
fi
mkdir -p -- "$output_dir"
if [[ ! -w "$output_dir" ]]; then
    printf 'Error: output directory is not writable: %s\n' "$output_dir" >&2
    exit 1
fi

"$python_bin" -m venv .venv
venv_python=.venv/bin/python
"$venv_python" -m pip install --upgrade 'pip==26.2.1'
"$venv_python" -m pip install --index-url https://download.pytorch.org/whl/cu130 \
    'torch==2.14.0+cu130' 'torchvision==0.29.0+cu130' 'torchaudio==2.11.0+cu130'
"$venv_python" -m pip install -r requirements.txt
"$venv_python" -m pip check
"$venv_python" -c 'import torch; assert torch.cuda.is_available(), "CUDA is unavailable"; print("PyTorch:", torch.__version__); print("GPU:", torch.cuda.get_device_name(0))'

install -m 755 "$script_dir/run_comfyui.sh" ./run_comfyui.sh
"$venv_python" -m pip freeze --all > comfyui-python-lock.txt
printf '\nSetup complete. Start ComfyUI with:\n  COMFYUI_OUTPUT_DIR=%q ./run_comfyui.sh\n' "$output_dir"
echo 'Resolved package versions were saved to comfyui-python-lock.txt.'
