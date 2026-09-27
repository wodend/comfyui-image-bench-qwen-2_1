# Benchmark record: `<model and configuration>`

Status: planned

Copy this file for each benchmark configuration. Keep raw observations separate
from conclusions, and commit the exact exported workflow JSON beside the record.

## Purpose

- Question:
- Compared configurations:
- Date and operator:

## Hardware

- Hardware report: `bash /mnt/ssd/Repos/comfyui-image-benchmarks/src/hardware_details.sh .venv/bin/python` (from the ComfyUI root)
- GPU model and VRAM:
- Driver:
- CPU:
- System RAM:
- Storage used for models and outputs:
- Operating system and kernel:
- Hardware source and inventory date:

## Software

- ComfyUI commit:
- Git worktree changes:
- Python:
- PyTorch and accelerator runtime:
- NVIDIA driver version:
- `requirements.txt` SHA-256:
- `run_comfyui.sh` SHA-256:
- `comfyui-python-lock.txt` file and SHA-256:
- Launch command, including all extra arguments:
- Software installation source URLs:

## Model artifacts

| Component | Source URL and revision | File | SHA-256 | Size |
| --- | --- | --- | --- | --- |
| Diffusion model | | | | |
| Text encoder | | | | |
| VAE | | | | |

## Workload

- Workflow JSON:
- Workflow JSON SHA-256 and upstream source:
- Input image files and SHA-256 (if any):
- Prompt and negative prompt:
- Seed:
- Width and height:
- Batch size:
- Steps, sampler, scheduler, and CFG:
- Other changed node values:
- Output format:

## Method

- Cold-start definition:
- Warm-up runs excluded:
- Measured run count:
- Timing boundaries and tool:
- Peak VRAM measurement and tool:
- Background processes or machine controls:

## Raw results

| Run | Wall time | Peak VRAM | Output file | Notes |
| ---: | ---: | ---: | --- | --- |
| 1 | | | | |

## Summary

- Median wall time:
- Range:
- Peak VRAM:
- Failures or anomalous runs:
- Visual or numerical correctness checks:

## Interpretation

Record conclusions only after the raw results are complete. Note limitations
and avoid comparing runs that changed model weights, workflow settings,
software versions, or hardware conditions without calling out those changes.
