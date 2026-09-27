# Hardware context

Read this file for the benchmark host and its inventory scripts. The public block below is the hardware page’s source of truth. Change this dated snapshot only after gathering a new report; retain earlier run records.

<!-- public:start -->
# Benchmark hardware

Local Qwen Image 2.1 runs use an NVIDIA RTX 3070 with 8 GiB of VRAM. The system below was checked on **2026-09-26**.

## Host specifications

| Component | Detail |
| --- | --- |
| CPU | AMD Ryzen 9 5900X 12-Core Processor |
| CPU cores | 12 physical, 24 logical |
| System RAM | 46 GiB |
| GPU | NVIDIA GeForce RTX 3070 |
| GPU VRAM | 8 GiB |
| NVIDIA driver | 615.71.09 |
| Operating system | CachyOS |
| Kernel | Linux 7.2.6-1-cachyos |
| System Python | 3.14.7 |

## What this snapshot describes

These specifications describe the local benchmark host. They are not minimum requirements, and the snapshot is not a contemporaneous inventory for every image shown. The [methods page](methods/) describes the model files and software used.
<!-- public:end -->

## Capture host information

The ComfyUI checkout is separate from this repository. The previously inspected checkout was `/mnt/ssd/Repos/ComfyUI`; verify its location rather than assuming it remains unchanged.

From this repository:

```bash
bash src/hardware_details.sh /path/to/ComfyUI/.venv/bin/python
bash src/python_venv_details.sh /path/to/ComfyUI/.venv
```

`src/hardware_details.sh` reports CPU model/core counts, total RAM, GPU model/VRAM, driver, OS, kernel, Python, PyTorch and CUDA. `src/python_venv_details.sh` is described in METHODS.md. These scripts omit host/user names, process lists, utilization and bus addresses. Run with actual GPU access: the sandbox previously reported CUDA unavailable although the host supported it. Do not publish that false result as a hardware change.

Keep a dated report under `site/data/<test-id>/` with each measured run. Current setup artifacts are under `site/data/setup-2026-09-26/`; keep the distinction between current snapshots and run-time evidence.

## Earlier observations

On 2026-09-22 the operator reported approximate averages of 20 seconds for T2I and 50 seconds for I2I with two inputs, with kernel `7.2.4-3-cachyos`. Run counts, timing boundaries, prompts and exact settings were not recorded. These are historical informal observations, not timing results for the published comparison.
