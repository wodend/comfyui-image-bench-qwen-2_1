# Benchmark hardware

Current host inventory captured on 2026-09-26. These are the system specifications used for local Qwen runs, not minimum requirements. Each future measured run should retain its own dated inventory.

## Host specifications

The initial privacy-safe hardware inventory for this benchmark host is below.
These are observations from the host, not requirements for every ComfyUI user.
The CPU and GPU models can be checked against the [AMD Ryzen 9 5900X specifications](https://www.amd.com/en/products/processors/desktops/ryzen/5000-series/amd-ryzen-9-5900x.html)
and [NVIDIA RTX 3070 specifications](https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3070-3070ti/).

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


## Capture an inventory

From the benchmark repository, run:

```bash
bash src/hardware_details.sh /path/to/ComfyUI/.venv/bin/python
bash src/python_venv_details.sh /path/to/ComfyUI/.venv
```

The scripts omit host names, user names, filesystem paths, utilization, and process lists. Run with GPU access so sandbox restrictions do not incorrectly report CUDA as unavailable. See [software setup](software.html) for environment versions and model artifacts.

## Earlier run observations

On 2026-09-22, the operator reported approximate averages of 20 seconds for T2I and 50 seconds for I2I with two inputs. Those observations used kernel `7.2.4-3-cachyos`. Run counts, timing boundaries, and workflow settings were not recorded, so these are informal observations and are not timings for the images on the comparison page.
