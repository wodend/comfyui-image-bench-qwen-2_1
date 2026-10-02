# T2I Outfit reference

Status: ready for review — both outputs imported

Proposed on: 2026-09-27

Test ID: `t2i-outfit-reference` · Roadmap stage 1

## Purpose

Generate a garment reference for the next `i2i-change-outfit` task. A burgundy satin dress differs clearly from the existing portrait's white suit in color, silhouette and material. A neutral mannequin makes the garment easy to inspect and gives the later editor an outfit reference without introducing a competing human identity.

This stage compares garment generation. The later I2I stage tests whether each editor can transfer the same selected dress onto the same selected portrait while retaining the person and scene.

## Recommended shared prompt

Submit the following paragraph verbatim to both systems as plain text, without a JSON wrapper or additional instructions. Set the output aspect ratio separately where supported.

> A realistic studio product photograph of a single burgundy satin wrap dress displayed on a neutral ivory, headless dress mannequin, viewed straight from the front. The dress has long sleeves, a modest V-shaped neckline, a tied fabric belt at the waist, and a knee-length skirt. The smooth satin fabric has a gentle sheen, with clearly visible seams and natural folds. The entire dress is visible, including both sleeves and the complete hem, with a small margin around it. The mannequin stands against a plain warm gray studio background. Soft, even lighting shows the garment's shape and fabric without harsh shadows. There are no other garments, accessories, people, text, or logos in the image. The composition is centered and vertical.

Requested aspect ratio: **2:3**.

## Proposed run settings

Produce **one initial image per system**. Save both originals, including failed or unusable results. Record any retries as additional numbered outputs rather than replacing the first image.

| Setting | Qwen Image 2.1 | ChatGPT |
| --- | --- | --- |
| Workflow | Existing official ComfyUI T2I template | Text-to-image generation |
| Inputs | Text only | Identical text only |
| Aspect ratio | 2:3 | Request 2:3 through available controls |
| Resolution | ResolutionSelector: 2 megapixels, multiple of 8 | Record actual output dimensions |
| Weights | INT8 ConvRot diffusion/text encoder, BF16 VAE | Record the model label actually used |
| Steps / CFG | 25 / 1.0 | Record only exposed settings |
| Sampler / scheduler | Euler / simple | Record only exposed settings |
| Seed | Fixed at `424242` | Record if exposed; otherwise unavailable |
| Negative prompt | Empty | No additional negative instructions |
| Batch size | 1 | One requested image |

These are intended settings, not evidence of a completed run. Use the existing setup documented in `METHODS.md`; record actual workflow values and output dimensions after generation. If ComfyUI runs with the INFO log described there, record its `Prompt executed in` duration alongside the Qwen output filename. Treat the first run as cold and record retries separately. ChatGPT timing is unavailable unless measured and documented separately.

## Review and usable-reference criteria

- One dress, in burgundy, with the requested wrap shape and satin appearance.
- Both long sleeves, the V-shaped neckline, tied waist and entire hem are visible.
- Garment construction is coherent: no fused sleeves, duplicated fabric belts or disconnected panels.
- The reference is sharp enough to distinguish color, neckline, silhouette and fabric folds.
- The image contains no human subject, extra outfit, text or logo that could confuse the later transfer.

Keep the T2I comparison even if an image fails these checks. For the subsequent edit, use Qwen's first sample if it meets all usable-reference criteria; otherwise use ChatGPT's first sample if it does. Record the selected source and the reasons. If neither qualifies, review the failures with the user before planning a retry. Both editors will receive the exact same selected reference, with its original bytes preserved.

## Output locations

The directories are ready. Drop each original PNG at:

```text
site/assets/images/t2i-outfit-reference/
  qwen-image-2-1/output-001.png
  chatgpt/output-001.png
site/data/t2i-outfit-reference/
```

Both original PNGs are present in their model directories. No I2I input directory is needed for this text-only stage. If there are additional samples, use `output-002.png`, and so on.

Save the exact submitted prompt, ComfyUI workflow/API export, dated setup evidence and a hash manifest in the artifact directory after approval and generation. Extract workflow metadata from the Qwen PNG when available. Record actual ChatGPT settings as reported; do not infer them from Qwen. Later, the selected garment reference will be copied without re-encoding into the separate I2I task's inputs, alongside a fixed original portrait.

## Next action

Both originals are imported as `output-001.png` under their respective model directories. The site's section is rendered from `benchmarks/records/t2i-outfit-reference.json`. The Qwen dress original was selected as the shared reference for both I2I outfit-edit cases; its bytes are preserved in `site/assets/images/i2i-change-outfit/inputs/input-002.png`. The Qwen workflow, API graph, exact prompt and both image hashes are in `site/data/t2i-outfit-reference/`.

## First observed Qwen run — awaiting file import

The local ComfyUI log contains one completed prompt in the 2026-09-30 23:29 startup session. It received the prompt at **23:34:46** and logged **`Prompt executed in 89.43 seconds` at 23:36:15**. Model loading occurred during this run, so classify this as a **cold-start observation**, not a warm-run average or a timing comparison with ChatGPT. ComfyUI's timer covers dequeued prompt execution, including saving the image.

The single PNG saved at that time is `/mnt/hdd/ComfyUIOutput/Qwen_image_2.1_00050.png` (1184 × 1776, 2,291,120 bytes; SHA-256 `61a7f25dfdaf123efd3f5aee3185fa4821561171aaaebe1b6fca6d92b73bd00c`). It was copied without re-encoding to `site/assets/images/t2i-outfit-reference/qwen-image-2-1/output-001.png`; the hashes match.

Embedded metadata reports 25 steps, CFG 1.0, Euler/simple, a 2:3 selector at 2 megapixels and **seed `593103825222985`**. The proposed seed was `424242`; the actual seed must take precedence in the run record. The text encoder received the proposed description inside a JSON string with `rewritten_prompt` and `wh_ratio` fields, not as the plain text described in the proposal. That exact string was extracted to [`site/data/t2i-outfit-reference/prompt.json`](../site/data/t2i-outfit-reference/prompt.json). The Qwen PNG contains a workflow and API graph. The log reports ComfyUI 0.37.0, PyTorch 2.14.0+cu130 and an RTX 3070 under `LOW_VRAM`; these are observations from this session, not a complete per-run environment capture.

The ChatGPT original is `site/assets/images/t2i-outfit-reference/chatgpt/output-001.png` (1024 × 1536, 1,814,051 bytes; SHA-256 `6962e3029bb702d3d26bb01ef5900b51a88c7f7ae1aaeb6a564941a169a099e5`). It contains no generation metadata. The operator confirmed on 2026-09-30 that the exact submitted prompt text matched Qwen; the ChatGPT settings remain unrecorded.

Both images show burgundy satin, a V-shaped neckline, long sleeves and a tied waist. The Qwen image has straighter sleeves and a longer-looking skirt; the ChatGPT image has gathered shoulders and a shorter-looking skirt. Exact knee length cannot be assessed without visible legs. The Qwen image was selected as the garment reference for the I2I edit because its long sleeves, wrap neckline, tied belt and complete hem are coherent and visible.
