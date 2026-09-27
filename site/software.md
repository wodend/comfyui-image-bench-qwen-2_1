# ComfyUI and Python setup

Snapshot checked on 2026-09-26 from the separate ComfyUI checkout. The checkout is at [`b5cc8830279eae909a59de030af1e50761c36751`](https://github.com/Comfy-Org/ComfyUI/commit/b5cc8830279eae909a59de030af1e50761c36751), with untracked setup and launcher scripts. CUDA availability was verified outside the sandbox. This describes the current host; a complete environment lock for the first comparison has not yet been archived.

## Verified environment

| Component | Detail |
| --- | --- |
| Virtual environment | Confirmed |
| Python | CPython 3.14.7 |
| pip | 26.2.1 |
| PyTorch | 2.14.0+cu130 |
| PyTorch CUDA runtime | 13.0 |
| CUDA available | Yes |
| cuDNN | 9.24.0 |
| torchvision | 0.29.0+cu130 |
| torchaudio | 2.11.0+cu130 |
| Package dependency check | OK |

## Archived current setup

The [resolved Python package inventory](data/setup-2026-09-26/python-packages.txt), [ComfyUI requirements](data/setup-2026-09-26/requirements.txt), [actual launcher](data/setup-2026-09-26/run_comfyui.sh), [actual setup script](data/setup-2026-09-26/setup_comfyui.sh), and [revision and SHA-256 manifest](data/setup-2026-09-26/manifest.json) were captured from the current checkout on 2026-09-26. These are current setup artifacts, not proof of the environment at the moment the first image was generated. The actual setup script is retained separately from this repository’s maintained setup recipe.

To rebuild the captured package set in a fresh Python 3.14 environment, install `python-packages.txt` using `--extra-index-url https://download.pytorch.org/whl/cu130`, then verify dependencies and CUDA. Archive fresh reports with each future run.

## Official workflow

Benchmarks use the [official ComfyUI Qwen Image 2.1 template](https://comfy.org/workflows/bb7e03924a5c-bb7e03924a5c/). The first comparison uses the INT8 models below, a 2:3 resolution at 2 megapixels, and 25 steps. Its exact workflow and API graph are archived on the comparison page.

## Set up the existing ComfyUI checkout

This recipe targets Linux, an NVIDIA GPU, Python 3.14, and an existing ComfyUI
checkout. The reference checkout used while writing this guide was
[`b5cc8830279eae909a59de030af1e50761c36751`](https://github.com/Comfy-Org/ComfyUI/commit/b5cc8830279eae909a59de030af1e50761c36751).
Record your checkout's actual commit; a different revision may have different
requirements or behavior. The script follows the [ComfyUI manual installation sequence](https://github.com/Comfy-Org/ComfyUI#manual-install-windows-linux):
create a virtual environment, install CUDA-enabled PyTorch, then install the
checkout's `requirements.txt`. The Python environment is local to ComfyUI,
not this documentation repository. The pinned PyTorch versions match the
verified environment above. They are installed from the [official PyTorch CUDA
wheel index](https://download.pytorch.org/whl/cu130).

From your existing ComfyUI checkout root, identify its revision:

```bash
git rev-parse HEAD
git status --short
```

Install Python 3.14 and a working NVIDIA driver first; `python3.14 --version`
and `nvidia-smi` must succeed. Use your distribution's packages and record their
exact versions. The [Python `venv` documentation](https://docs.python.org/3.14/library/venv.html),
[CachyOS installation guide](https://wiki.cachyos.org/installation/installation_on_root/),
and [CachyOS hardware driver guide](https://wiki.cachyos.org/features/chwd/chwd/)
give the upstream installation background. ComfyUI notes that Python 3.14 can
cause trouble with some custom nodes; this benchmark uses no custom nodes.

From the same ComfyUI checkout root, run the setup script. These commands
assume this documentation repository is at
`/mnt/ssd/Repos/comfyui-image-bench-qwen-2_1`; adjust that path if you move it.

```bash
python3.14 --version
nvidia-smi
bash /mnt/ssd/Repos/comfyui-image-bench-qwen-2_1/src/setup_comfyui.sh
```

The script stops if `.venv`, `run_comfyui.sh`, or `comfyui-python-lock.txt`
already exists. It creates
`.venv` from Python 3.14, installs pip 26.2.1 and CUDA 13.0 PyTorch 2.14.0,
torchvision 0.29.0, and torchaudio 2.11.0, installs the checked-out
`requirements.txt`, checks dependencies and CUDA, then installs the launcher
and writes `comfyui-python-lock.txt` with all resolved package versions.
It does not download models. Set `COMFYUI_PYTHON=/absolute/path/to/python3.14`
if that interpreter has another name. Set `COMFYUI_OUTPUT_DIR=/absolute/path`
before setup if `/mnt/hdd/ComfyUIOutput` is unsuitable; use the same value
when launching. The default path requires `/mnt/hdd` to be mounted. A failed
install leaves `.venv` for diagnosis. Start again in
a fresh checkout after resolving the cause.

This script pins the direct PyTorch packages, while ComfyUI's requirements
still allow many transitive packages to change. Copy the generated lock file
into the benchmark record before running a benchmark. For a later rebuild,
create a fresh Python 3.14 virtual environment in the same ComfyUI revision
and install that lock file with the CUDA index command in section 6. Compare
`pip check`, the ComfyUI commit, and model hashes before treating runs as
equivalent.

## 2. Verify the environment

These checks do not install or modify packages:

```bash
.venv/bin/python --version
.venv/bin/python -m pip check
.venv/bin/python -c 'import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "no CUDA GPU")'
```

For an NVIDIA benchmark host, `torch.cuda.is_available()` should print `True`
and the reported device should be the intended GPU before continuing.

## 3. Prepare Qwen Image 2.1 for low VRAM

Use the smaller official INT8 ConvRot diffusion model and text encoder, plus
the BF16 VAE. If you already have these weights, keep them in place. Their
upstream source is the [Comfy-Org Qwen Image 2.1 repository](https://huggingface.co/Comfy-Org/Qwen-Image-2.1/tree/main).
Verify their locations:

```text
models/
├── diffusion_models/
│   └── qwen_image_2.1_int8_convrot.safetensors
├── text_encoders/
│   └── qwen3vl_8b_int8_convrot.safetensors
└── vae/
    └── qwen_image_2.1_vae_bf16.safetensors
```

The official file pages publish these SHA-256 values. Check your existing
files against them; no model download is part of the setup script.

| File | SHA-256 | Official source |
| --- | --- | --- |
| `qwen_image_2.1_int8_convrot.safetensors` | `cb74113cb03faecd79611b01fd7fd642f0aa60d6f0b95086abee214d75eaa57d` | [Diffusion model](https://huggingface.co/Comfy-Org/Qwen-Image-2.1/blob/main/diffusion_models/qwen_image_2.1_int8_convrot.safetensors) |
| `qwen3vl_8b_int8_convrot.safetensors` | `8bfd0f6e12abf2d2d697ecc888e5e90b0d6741d6708f05799f53afa560452e8f` | [Text encoder](https://huggingface.co/Comfy-Org/Qwen-Image-2.1/blob/main/text_encoders/qwen3vl_8b_int8_convrot.safetensors) |
| `qwen_image_2.1_vae_bf16.safetensors` | `bb21f7473051e1ac368515dd3f2e15cd44d7a11748ee8823e1ddca3e4876b7c9` | [VAE](https://huggingface.co/Comfy-Org/Qwen-Image-2.1/blob/main/vae/qwen_image_2.1_vae_bf16.safetensors) |

The official repository also provides larger BF16 variants. Do not mix their
performance results with the INT8 configuration: weight format affects disk
use, memory use, speed, and potentially output.

The files are large. Verify free space for the environment and generated
outputs before running:

```bash
df -h .
# Also check the output filesystem when /mnt/hdd is a separate mount:
df -h /mnt/hdd
```

## 4. Run ComfyUI

The setup script installs [this launcher](https://github.com/wodend/comfyui-image-bench-qwen-2_1/blob/main/src/run_comfyui.sh) in the ComfyUI
root. It can be invoked from any working directory:

```bash
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
```

- `set -euo pipefail` makes shell errors, unset variables, and failed pipeline
  stages stop the launcher.
- `repo_dir=...` resolves the directory containing the script rather than
  assuming the current directory is the repository.
- `.venv/bin/python` guarantees that ComfyUI uses this checkout's virtual
  environment.
- `exec` replaces the shell with Python, so signals and the process exit code
  reach the ComfyUI process directly.
- `--lowvram` selects ComfyUI's low-VRAM mode. In this checkout, its CLI help
  notes that the flag moves text encoders to CPU when dynamic VRAM is not in
  use.
- `COMFYUI_OUTPUT_DIR` selects an existing writable output directory; it
  defaults to `/mnt/hdd/ComfyUIOutput`, which the setup script creates.
- `"$@"` forwards caller-supplied options without losing argument boundaries.
  Because they occur last, options supplied at launch can override many earlier
  argparse options, but benchmark runs should record every extra argument.

Before the first launch, confirm the configured output location:

```bash
test -x run_comfyui.sh
test -x .venv/bin/python
test -w "${COMFYUI_OUTPUT_DIR:-/mnt/hdd/ComfyUIOutput}"
```

Start the local server with:

```bash
./run_comfyui.sh
```

The default UI is normally available at `http://127.0.0.1:8188`. To change a
runtime option while retaining the launcher's defaults, append it, for example:

```bash
./run_comfyui.sh --port 8189
```

## 5. Load the official workflow

After ComfyUI starts:

1. Open the local UI and select the Qwen Image 2.1 text-to-image workflow from
   the workflow templates. If it is not listed, download and load the
   [official workflow JSON](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_qwen_image_2_1_t2i.json).
2. Confirm that the loaders select the INT8 diffusion model and text encoder
   and the BF16 VAE listed above.
3. For the first smoke test, retain the template's 1024 by 1024 resolution,
   Euler sampler, simple scheduler, CFG 1, and 25 steps. The template notes that
   a negative prompt is unused at CFG 1.
4. Enter a prompt and queue one image. Confirm that a PNG appears under the
   configured output directory.

This smoke test proves that the environment, model placement, workflow, and
output path work together. It is not a benchmark result. Do not compare timing
until inputs, workflow JSON, software revisions, warm-up policy, and measurement
method have been fixed and recorded.

## 6. Capture the setup before benchmarking

Generate a privacy-safe hardware and runtime summary with:

```bash
bash /mnt/ssd/Repos/comfyui-image-bench-qwen-2_1/src/hardware_details.sh .venv/bin/python
bash /mnt/ssd/Repos/comfyui-image-bench-qwen-2_1/src/python_venv_details.sh .venv/bin/python
```

The script reports stable specifications only. It deliberately omits running
processes, current CPU/GPU/memory utilization, host and user names, device bus
addresses, and filesystem paths. Its NVIDIA query converts total VRAM from MiB
to GiB (for example, `8192 MiB` becomes `8 GiB`). Passing the virtual
environment's Python executable includes its PyTorch and CUDA runtime versions;
without an argument, the script checks `python3`.

Also save the following read-only inventory with the first future benchmark
record:

```bash
git rev-parse HEAD
git status --short
.venv/bin/python --version
.venv/bin/python -m pip freeze --all
.venv/bin/python -m pip check
sha256sum comfyui-python-lock.txt
sha256sum requirements.txt
sha256sum run_comfyui.sh
sha256sum models/diffusion_models/qwen_image_2.1_int8_convrot.safetensors
sha256sum models/text_encoders/qwen3vl_8b_int8_convrot.safetensors
sha256sum models/vae/qwen_image_2.1_vae_bf16.safetensors
```

Also export the exact workflow JSON from ComfyUI. Generated PNG metadata is
useful for reconstruction, but the explicit workflow and environment inventory
make comparisons easier to audit.

Copy `comfyui-python-lock.txt` beside each benchmark record. It records the
resolved versions, including indirect dependencies. To
rebuild that exact Python package set in another fresh Python 3.14 environment,
install with `python -m pip install --extra-index-url https://download.pytorch.org/whl/cu130 -r /path/to/comfyui-python-lock.txt`
and run `python -m pip check`. Exact wheels and GPU behavior still depend on
the Python patch release, OS, architecture, NVIDIA driver, and package index
availability. Record those along with model SHA-256 values and input image
hashes. The ComfyUI commit above identifies source code; the requirements hash
also catches local dependency edits.

## Sources

- [ComfyUI manual installation and running instructions](https://github.com/Comfy-Org/ComfyUI#manual-install-windows-linux)
- [Python 3.14 virtual environment documentation](https://docs.python.org/3.14/library/venv.html)
- [PyTorch installation and CUDA wheel index](https://pytorch.org/get-started/locally/)
- [CachyOS installation and hardware driver documentation](https://wiki.cachyos.org/features/chwd/chwd/)
- [Official ComfyUI Qwen Image 2.1 model files](https://huggingface.co/Comfy-Org/Qwen-Image-2.1)
- [Official Qwen Image 2.1 text-to-image workflow](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_qwen_image_2_1_t2i.json)
