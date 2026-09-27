#!/usr/bin/env bash
set -euo pipefail

# Inspect a Python virtual environment without printing its filesystem path,
# installed-package inventory, environment variables, or other host details.

venv_target="${1:-.venv}"

if [[ -d "$venv_target" ]]; then
    python_bin="$venv_target/bin/python"
else
    python_bin="$venv_target"
fi

if [[ ! -x "$python_bin" ]]; then
    printf 'Error: no executable Python interpreter found for the supplied virtual environment.\n' >&2
    exit 1
fi

echo "Python virtual environment details"

"$python_bin" -c 'import sys; print("Virtual environment:", sys.prefix != sys.base_prefix)'
"$python_bin" -c 'import platform; print("Python:", platform.python_version())'
"$python_bin" -c 'import platform; print("Python implementation:", platform.python_implementation())'

if "$python_bin" -c 'import pip' >/dev/null 2>&1; then
    "$python_bin" -c 'import pip; print("pip:", pip.__version__)'
else
    echo "pip: not installed"
fi

if "$python_bin" -c 'import torch' >/dev/null 2>&1; then
    "$python_bin" -c 'import torch; print("PyTorch:", torch.__version__)'
    "$python_bin" -c 'import torch; print("PyTorch CUDA runtime:", torch.version.cuda or "not available")'
    "$python_bin" -c 'import torch; print("CUDA available:", torch.cuda.is_available())'
    "$python_bin" -c 'import torch; v = torch.backends.cudnn.version(); print("cuDNN:", f"{v // 10000}.{v % 10000 // 100}.{v % 100}" if v else "not available")'
else
    echo "PyTorch: not installed"
fi

for package_name in torchvision torchaudio; do
    if "$python_bin" -c "import $package_name" >/dev/null 2>&1; then
        "$python_bin" -c "import $package_name; print(\"$package_name:\", $package_name.__version__)"
    else
        printf '%s: not installed\n' "$package_name"
    fi
done

if "$python_bin" -m pip --version >/dev/null 2>&1; then
    if "$python_bin" -m pip check >/dev/null 2>&1; then
        echo "Package dependency check: OK"
    else
        echo "Package dependency check: FAILED"
    fi
fi
