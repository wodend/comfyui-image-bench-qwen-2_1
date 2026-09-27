# Benchmark process

Read this file when creating or completing benchmark sections. The goal is a growing visual comparison of local Qwen Image 2.1 and ChatGPT as a control, using the same submitted prompt for each task. The reader should see what was asked and inspect both original outputs before digging into settings.

## Current state

- `t2i-realistic-character` is published in `site/bench/index.md`, with one original PNG from each system.
- The operator’s ChatGPT label is “ChatGPT Images 2.0 Sol (light)”; the PNG has no generation metadata. Do not replace that label with an inferred model version.
- The exact Qwen workflow, API graph and submitted JSON string were extracted from its PNG. Preserve that submitted string, including its wrapper. Its output is 1184 × 1776, seed 593103825222985, 25 steps, CFG 1, Euler/simple and INT8 ConvRot weights.
- Timings and peak VRAM for this pair were not recorded. The dated setup snapshot is current host context rather than contemporaneous run evidence.
- I2I comparisons await input images, prompt, outputs and run records. Earlier informal I2I timing is not a published comparison.

## Iterative workflow

1. Agree on a narrow task and assign a stable ID such as `t2i-realistic-character`. Explain which capability it probes and how outputs will be compared. Prepare the shared prompt without changing already submitted prompts.
2. Create a pending task under `site/bench/index.md` and a record under `benchmarks/<test-id>.md` using `benchmarks/record-template.md`. Include the prompt and intended settings. Keep missing outputs labeled as awaiting runs; do not link nonexistent images. The new task heading automatically appears in the sidebar.
3. Give the operator the prompt and intended workflow/configuration. The operator runs Qwen and ChatGPT, then copies the original output PNGs and any I2I inputs into the repository. Do not assume a run occurred because a section was prepared.
4. Import the supplied images using the naming convention below. Preserve file bytes and metadata. Extract actual workflow and API settings from Qwen PNG metadata when present; retain explicitly supplied exports too. Prefer actual run evidence to template defaults.
5. Gather dated host and Python reports using HARDWARE.md and METHODS.md. Capture the real ComfyUI revision, launch command, resolved package set, requirements/launcher/model/input hashes and exact workflow. Label records collected later as snapshots rather than run-time evidence.
6. Render the exact prompt above equal-width image panels. Each panel has its actual model label, dimensions, meaningful alt text and a full-resolution link. Use `benchmarks/comparison-template.md`. Store settings and reproduction artifacts in an expandable section.
7. Generate a manifest with paths relative to `site/`, SHA-256 hashes and byte sizes. Mark unknown values explicitly. Do not infer ChatGPT seeds/settings from Qwen or assign a winner without reviewing the outputs.
8. Build and validate using SITE.md. Review desktop and mobile layouts, navigation and original-image links. Publish only when requested.

## Task selection and rationale

The first portrait prompt uses a simple subject and restrained studio composition. It provides observable checks for clothing structure, seams, matte fabric, lighting, pose and background without requiring a complex narrative. This is a starting point, not a comprehensive score.

Future task categories should cover distinct capabilities. These are planning directions, not completed tests or newly generated prompts:

| Category | What a basic task can reveal |
| --- | --- |
| Realistic subjects | Anatomy, materials, clothing detail and lighting |
| Objects and spatial relationships | Counts, arrangement and adherence to positional instructions |
| Typography and layouts | Exact text, hierarchy and placement |
| Illustration and styles | Ability to follow a specified visual treatment |
| I2I local edits | Changing a requested region while retaining the rest |
| I2I identity and composition | Retaining supplied subject details through an edit |
| I2I multiple references | Combining specified inputs and respecting their roles |

Choose prompts that make the requested result easy for a human to assess. Start with one clear objective and fixed inputs. Keep challenging combinations as separate tasks so it remains clear which capability is being tested. Discuss additions with the user rather than silently broadening the suite.

## Files and naming

```text
site/bench/index.md
site/assets/images/<test-id>/
  inputs/input-001.png             # I2I only
  qwen-image-2-1/output-001.png
  chatgpt/output-001.png
site/data/<test-id>/
  prompt.json
  workflow.json
  workflow-api.json
  manifest.json
benchmarks/<test-id>.md
```

Use three-digit sample numbers to retain repeats without overwriting earlier outputs. Use separate model/configuration IDs when a configuration changes; document exact model and configuration labels in the record. `chatgpt` is a service directory, not a claim about a version independently verified from its image.

## Manifest format

`path_base` is `site/`. Each `files` key is a site-relative path, such as `assets/images/t2i-realistic-character/qwen-image-2-1/output-001.png`; its value contains `sha256` and `bytes`. Do not include the manifest itself in its hash list. Historical setup manifests use a `date`, `scope`, `comfyui_commit` and filename-to-hash map; retain their format and provenance.
