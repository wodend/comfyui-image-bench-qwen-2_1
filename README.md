# Qwen Image 2.1 Benchmarks in ComfyUI

[View the benchmark website](https://wodend.github.io/comfyui-image-bench-qwen-2_1/) · [![Build and deploy GitHub Pages](https://github.com/wodend/comfyui-image-bench-qwen-2_1/actions/workflows/pages.yml/badge.svg)](https://github.com/wodend/comfyui-image-bench-qwen-2_1/actions/workflows/pages.yml)

This project explores what Qwen Image 2.1 can do when run locally in ComfyUI, using ChatGPT image generation as a control. The comparisons cover basic text to image (T2I) and image to image (I2I) tasks. Hardware specifications, software versions and workflow artifacts give context for reproducing the local runs.

The focus is the images: each benchmark shows its inputs and prompt followed by the original outputs in side-by-side panels.

These visual benchmarks test local AI image generation and image editing with shared prompts and, for edits, shared reference images. Original PNGs, ComfyUI workflows, submitted prompts, and SHA-256 manifests accompany the results so readers can inspect image quality and reproduce the local setup. Individual run details distinguish recorded observations from settings that were not captured.

## Project sources

- [ComfyUI](https://github.com/Comfy-Org/ComfyUI), the local image-generation engine.
- Official Qwen Image 2.1 [text-to-image workflow](https://comfy.org/workflows/bb7e03924a5c-bb7e03924a5c/) and [image-edit workflow](https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_qwen_image_2_1_image_edit.json).
- [Comfy-Org Qwen Image 2.1 model files](https://huggingface.co/Comfy-Org/Qwen-Image-2.1), including the INT8 ConvRot weights used for local runs.

The Methods page is the source of truth for the recorded ComfyUI and Python setup. The Hardware page gives the dated host snapshot; each comparison links its own available run evidence.
