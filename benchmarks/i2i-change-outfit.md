# Proposal: I2I Change Outfit

Status: ready for review — four original outputs imported

Test ID: `i2i-change-outfit` · Roadmap stage 2

## Purpose

Replace the white suit in an existing AI-generated portrait with a burgundy satin wrap dress, using a second AI-generated image as the garment reference. This tests garment transfer while retaining the woman's identity and the original photograph's pose, framing and studio scene.

## Proposed shared inputs

The run contains two portrait cases. In each case, give **both** editors the same `<image1>` portrait and the same Qwen dress as `<image2>`. Byte-identical source copies are ready in `site/assets/images/i2i-change-outfit/inputs/`.

| Role | Source | SHA-256 |
| --- | --- | --- |
| `<image1>` — Qwen portrait case | `site/assets/images/t2i-realistic-character/qwen-image-2-1/output-001.png` | `79e77e7b807182fbf3c5217aed73463bd6dc1ac054393a86142cb3c4cbcd845e` |
| `<image1>` — ChatGPT portrait case | `site/assets/images/t2i-realistic-character/chatgpt/output-001.png` | `be476b09b503b7d03be304f6c5d98f4f693c4dd814687400a97dadbc83260755` |
| `<image2>` — both cases | `site/assets/images/t2i-outfit-reference/qwen-image-2-1/output-001.png` | `61a7f25dfdaf123efd3f5aee3185fa4821561171aaaebe1b6fca6d92b73bd00c` |

Both source portraits show the white suit; the ChatGPT portrait is full length and the Qwen portrait is cropped below the knees. The Qwen dress reference meets the recorded usable-reference criteria: one coherent burgundy satin wrap dress, visible long sleeves, V neckline, tied waist and full hem, without a human model or competing garments. Its hem appears longer than knee length; the approved edit prompt explicitly requests a knee-length hem while taking the garment's other details from the reference. Each output pair is compared against one fixed portrait input, not against a different portrait for each editor.

## Recommended shared prompt

Submit this exact JSON string to both systems with the two images above. Do not add a model-specific preface or rewrite; use the same reference order. The exact approved text is also archived at `site/data/i2i-change-outfit/proposed-prompt.json`.

```json
{"rewritten_prompt":"Replace the woman's white blazer, top, and trousers in <image1> with the burgundy satin wrap dress from <image2>. Use <image1> as the portrait to edit and <image2> only as the garment reference. Match the dress's deep burgundy color, subtle satin sheen, long sleeves with cuffs, overlapping V-shaped wrap neckline, tied fabric belt at the waist, and gently flared skirt silhouette. Fit the dress naturally to her body and existing stance, with believable folds, seams, and a coherent hem at knee length. Remove the white suit completely, revealing anatomically natural legs below the skirt while preserving her original white shoes and foot positions. Keep the arm on the viewer's right bent in its original position, with the hand resting naturally against her hip outside the dress after removing the trouser pocket; preserve the relaxed hanging hand on the viewer's left. Keep the same woman, face, hair, expression, earrings, body proportions, overall standing pose, camera angle, full-body framing, warm gray studio background, and lighting from <image1>. Render the dress as part of the original photograph, with highlights and shadows consistent with the existing studio lighting. Do not include the mannequin, extra people, extra garments, text, or logos.","wh_ratio":"","ratio_follow":"<image1>"}
```

Target aspect ratio: **follow `<image1>`** (the source portrait is 2:3). Preserve the portrait's full-body framing. Request one initial result per system; retain failed attempts and retries as additional numbered outputs.

## Review checks

- The white blazer, top and trousers are replaced by one coherent burgundy wrap dress; the mannequin is absent.
- The dress carries the reference's color, sheen, overlapping V neckline, long sleeves with cuffs, tied waist and flared skirt, with a coherent knee-length hem and no duplicated fabric or broken seams.
- The woman's face, hair, expression and proportions remain recognizable from image 1.
- Pose, camera angle, full-body framing, studio background and lighting stay close to `<image1>`; the white shoes and foot positions remain, and the hands follow the specified placement after removing the trouser pocket.
- No extra subjects, garments, text or logos appear. Keep both outputs in the comparison even when a check fails.

## Run handoff

The operator will use an appropriate two-image Qwen Image 2.1 editing workflow and the ChatGPT editing interface with the same original inputs and exact text above. Save the actual Qwen workflow/API graph, model labels, image roles and order, seed, settings, output dimensions, and INFO-log timing where available. Do not assume the T2I workflow or settings apply to this edit. The existing `scripts/post_generation.py` handles one-sample T2I pairs only; import this I2I run using the record procedure in `BENCH.md` until the script supports I2I.

The structured record contains both portrait cases. `inputs/input-001.png` is the Qwen portrait, `inputs/input-002.png` is the shared dress, and `inputs/input-003.png` is the ChatGPT portrait. Their SHA-256 hashes match the T2I originals. Both editors' `output-001.png` files are shown in the Qwen portrait case and both `output-002.png` files in the ChatGPT portrait case. ChatGPT's PNGs have no workflow metadata, so that pairing follows the supplied filenames and visual inspection.

## Captured runs

The Qwen PNGs embed the exact approved JSON prompt. `output-001.png` used the Qwen portrait and shared dress; it is byte-identical to `/mnt/hdd/ComfyUIOutput/Qwen_image_2.1_00053.png` and matches the 2026-10-01 22:24:27 log completion at **157.31 seconds**. Its actual seed is `375837271375947` and its dimensions are 1184 × 1792. `output-002.png` used the ChatGPT portrait and shared dress; it matches `/mnt/hdd/ComfyUIOutput/Qwen_image_2.1_00052.png` and the 22:20:25 completion at **113.77 seconds**. Its actual seed is `879528060392197` and its dimensions are 1024 × 1536. Both runs used the INT8 ConvRot model, 25 steps, CFG 1, Euler/simple, and the BF16 VAE. These are individual observations, not a speed comparison.

An earlier prompt in the same session was interrupted after 62.54 seconds and yielded no archived image. The ChatGPT outputs are 1024 × 1536 and contain no generation metadata. Their model label is supplied by the operator. All four edited originals and both Qwen workflow/API exports are retained in the record and SHA-256 manifest.
