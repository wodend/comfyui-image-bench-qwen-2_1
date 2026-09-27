# Method and prompts

## Comparison method

Each comparison records a task, the same submitted prompt for both systems, the input images for I2I, and the original outputs. Display outputs side by side at equal width, preserve their aspect ratios, and make the full PNGs available. Describe differences only after reviewing the images; keep informal timing observations separate from measured runs.

For measured runs, record warm-up policy, run count, timing boundaries, peak VRAM measurement, seeds, resolution, sampler, steps, CFG, model hashes, and the exact workflow. Retain a dated hardware report, ComfyUI revision, launcher hash, and resolved Python environment lock with each run. Use the [benchmark record template](https://github.com/wodend/comfyui-image-bench-qwen-2_1/blob/main/benchmarks/record-template.md).

## Prompts

ChatGPT was used to generate the prompts used.

## Official workflows

Start Qwen T2I runs from the [official ComfyUI template](https://comfy.org/workflows/bb7e03924a5c-bb7e03924a5c/). Record every change to the template and retain the exact run graph. The repository also preserves an earlier image editing workflow under `workflows/`; it is not the source of the first T2I result.

## Adding a comparison

1. Prepare a shared prompt and save the exact submitted text.
2. Run both systems and retain the original outputs and I2I input images.
3. Use `site/assets/images/<test-id>/<model-id>/output-001.png` for outputs and `site/assets/images/<test-id>/inputs/input-001.png` for I2I inputs. Save workflow, prompt, lock file, and hash manifest under `site/data/<test-id>/`.
4. Copy the comparison markup from the home page or `benchmarks/comparison-template.md`, including meaningful image descriptions and model captions.
5. Add a heading in `site/index.md`; its sidebar index is generated from headings automatically.
6. Complete a record under `benchmarks/` and link its reproducibility artifacts. Mark unavailable information explicitly.
7. Build and validate the site before publishing.

## Image naming convention

Use lowercase identifiers with hyphens. Keep the test identifier stable across its images, records, and artifacts. The model directory identifies the generating model; use `chatgpt` when only the service is known, and record the operator’s model label in the comparison caption. Number outputs with three digits (`output-001.png`, `output-002.png`) so repeated samples sort consistently. Store distinct model versions or configurations in separate model directories and document what changed.

```text
site/
├── assets/images/
│   ├── t2i-realistic-character/
│   │   ├── qwen-image-2-1/output-001.png
│   │   └── chatgpt/output-001.png
│   └── i2i-example/
│       ├── inputs/input-001.png
│       ├── qwen-image-2-1/output-001.png
│       └── chatgpt/output-001.png
└── data/
    └── t2i-realistic-character/
        ├── prompt.json
        ├── workflow.json
        ├── workflow-api.json
        └── manifest.json
```

The I2I paths illustrate the convention; no I2I comparison has been added yet. Preserve original file bytes and metadata when renaming. Each manifest lists paths relative to `site/`, file sizes, and SHA-256 hashes. Use the same test identifier for its record under `benchmarks/`.
