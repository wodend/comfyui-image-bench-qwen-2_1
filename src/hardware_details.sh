#!/usr/bin/env bash
set -euo pipefail

# Print stable system specifications without process lists, utilization, device
# addresses, host names, user names, mount paths, or other machine identifiers.

python_bin="${1:-python3}"

echo "Hardware and runtime details"

if command -v lscpu >/dev/null 2>&1; then
    lscpu | awk -F: '
        /^Model name:/ { gsub(/^[ \t]+/, "", $2); print "CPU: " $2 }
        /^Socket\(s\):/ { gsub(/^[ \t]+/, "", $2); sockets=$2 }
        /^Core\(s\) per socket:/ { gsub(/^[ \t]+/, "", $2); cores=$2 }
        /^CPU\(s\):/ && !threads { gsub(/^[ \t]+/, "", $2); threads=$2 }
        END {
            if (sockets && cores) print "CPU physical cores: " sockets * cores
            if (threads) print "CPU logical cores: " threads
        }
    '
fi

free -h | awk '/^Mem:/ { print "System RAM: " $2 }'

if command -v nvidia-smi >/dev/null 2>&1; then
    if gpu_rows="$(nvidia-smi \
        --query-gpu=name,memory.total,driver_version \
        --format=csv,noheader,nounits 2>/dev/null)" && [[ -n "$gpu_rows" ]]; then
        awk -F', *' '{
        gib = $2 / 1024
        printf "GPU: %s\nGPU VRAM: %g GiB\nNVIDIA driver: %s\n", $1, gib, $3
        }' <<<"$gpu_rows"
    else
        echo "GPU: nvidia-smi found, but the NVIDIA driver is unavailable"
    fi
else
    echo "GPU: nvidia-smi not available"
fi

if [[ -r /etc/os-release ]]; then
    os_name="$({ . /etc/os-release; printf '%s' "${PRETTY_NAME:-unknown}"; })"
    printf 'Operating system: %s\n' "$os_name"
fi
printf 'Kernel: %s\n' "$(uname -sr)"

if command -v "$python_bin" >/dev/null 2>&1; then
    "$python_bin" -c 'import platform; print("Python:", platform.python_version())'
    if "$python_bin" -c 'import torch' >/dev/null 2>&1; then
        "$python_bin" -c 'import torch; print("PyTorch:", torch.__version__)'
        "$python_bin" -c 'import torch; print("PyTorch CUDA runtime:", torch.version.cuda or "not available")'
        "$python_bin" -c 'import torch; print("CUDA available:", torch.cuda.is_available())'
    else
        echo "PyTorch: not installed for $python_bin"
    fi
else
    echo "Python: $python_bin not available"
fi
