# Proposal: T2I Goat

Status: ready for review — both outputs imported

Test ID: `t2i-goat` · Roadmap stage 3

The intervening roadmap stage, `i2i-change-outfit`, is not yet prepared or run. This is the next T2I task; its output directories are ready and its public section is marked pending.

## Purpose

Generate a realistic, full-body goat portrait. The task tests recognizable goat anatomy, coat markings, pose and basic scene adherence. A visible torso, legs and head also make one of these AI-generated outputs usable as the shared subject image for the later `i2i-change-goat-outfit` task.

A goat has distinctive horns, a beard and cloven hooves that a viewer can assess without relying on text or a busy environment. The neutral studio composition gives the later edit room to add clothing while checking whether the goat's identity and pose remain intact.

## Recommended shared prompt

Submit this exact JSON string to **both systems**. Do not add a model-specific preface or rewrite. Select the output aspect ratio separately where supported.

```json
{"rewritten_prompt":"A realistic full-body studio photograph of a single adult domestic goat standing naturally in a three-quarter view, facing slightly toward the camera. The goat has a short cream-colored coat with light brown patches on its shoulders, two small backward-curving horns, a short beard, upright ears, and clearly visible cloven hooves. Its head, torso, all four legs and hooves, and entire tail are visible, with clear space around the body. The goat has a calm, alert expression. Soft, even studio lighting shows the coat texture and body shape against a plain warm gray background. No collar, harness, clothing, accessories, people, other animals, text, or logos. The composition is centered and vertical.","wh_ratio":"2:3"}
```

Requested aspect ratio: **2:3**. Keep the exact submitted JSON in the run artifacts even if a model's interface displays only the `rewritten_prompt` field.

## Proposed run handoff

Generate **one initial image per system**. Start Qwen from the [official ComfyUI Qwen Image 2.1 T2I template](https://comfy.org/workflows/bb7e03924a5c-bb7e03924a5c/), using the existing INT8 ConvRot diffusion and text encoder, BF16 VAE, 25 steps, CFG 1, Euler/simple, 2:3 at 2 megapixels, and batch size 1. Leave the negative prompt empty. Record the **actual** seed and all actual workflow values from the PNG; do not assume a proposed seed was used. For ChatGPT, request 2:3 where supported and record its actual model label and output dimensions.

Queue one Qwen image at a time with the ComfyUI INFO log enabled as described in `METHODS.md`. Pair the output filename with the matching `Prompt executed in` entry; mark cold versus warm runs. Keep retries as `output-002.png`, etc., without replacing the first samples. Timing is an observation unless a measured-run policy and run count are documented.

## Review checks and reference rule

- One recognizable goat, with plausible proportions, four distinct legs with cloven hooves, a coherent head and tail.
- Requested small horns, short beard, upright ears, cream coat and light brown shoulder patches appear coherently.
- The full animal is visible, including enough empty space around the torso for a later outfit edit.
- The image has no collar, harness, clothing, other animals or people.
- Background and lighting are simple enough to distinguish animal anatomy from artifacts.

Keep both outputs in the T2I comparison even if one fails a check. For the later outfit edit, use Qwen's first sample if it satisfies all reference criteria; otherwise use ChatGPT's first sample if it does. Record that selection and give both I2I systems the **same original goat PNG**, alongside the same AI-generated outfit reference. If neither output is usable, discuss a recorded retry before moving to the edit.

## Output locations

```text
site/assets/images/t2i-goat/
  qwen-image-2-1/output-001.png
  chatgpt/output-001.png
site/data/t2i-goat/
  prompt.json
  workflow.json
  workflow-api.json
  manifest.json
benchmarks/records/t2i-goat.json
```

Both original PNGs were supplied. The post-generation script imported their metadata and hashes, matched the Qwen timing, updated the structured record and rebuilt the site. Visual review and selection of a goat reference for the later edit remain pending.

<!-- postgen:start -->
## Post-generation capture

- Qwen original: `site/assets/images/t2i-goat/qwen-image-2-1/output-001.png`; SHA-256 `bde4b2079671101fff02d2b00941e94d1b85a85fd3be75e08ab834092032d31f`.
- ChatGPT original: `site/assets/images/t2i-goat/chatgpt/output-001.png`; SHA-256 `c5806f805163e9100a595f99fc1cc0d422a5981d4dc1bccaa63311ed12b2ecf5`.
- Qwen actual seed: `593103825222985`; steps: `25`; CFG: `1.0`; sampler/scheduler: `euler/simple`.
- Timing: ComfyUI log: [2026-10-01 00:04:39,206] [INFO] Prompt executed in 63.78 seconds. Matched to the original Qwen PNG by SHA-256 and its save time.
- Captured artifacts: `site/data/t2i-goat/`. Visual review and reference selection remain pending.
<!-- postgen:end -->
