# Benchmark process

Read this file when creating or completing benchmark sections. The goal is a growing visual comparison of local Qwen Image 2.1 and ChatGPT as a control, using the same submitted prompt for each task. The reader should see what was asked and inspect both original outputs before digging into settings.

## Current state

- `t2i-realistic-character` is published in `site/bench/index.md`, with one original PNG from each system.
- The operator’s ChatGPT label is “ChatGPT Images 2.0 Sol (light)”; the PNG has no generation metadata. Do not replace that label with an inferred model version.
- The exact Qwen workflow, API graph and submitted JSON string were extracted from its PNG. Preserve that submitted string, including its wrapper. Its output is 1184 × 1776, seed 593103825222985, 25 steps, CFG 1, Euler/simple and INT8 ConvRot weights.
- Timings and peak VRAM for this pair were not recorded. The dated setup snapshot is current host context rather than contemporaneous run evidence.
- The first I2I outfit edit has two portrait cases, each with a Qwen and ChatGPT output. Qwen prompts, workflows and timings were recovered from the original PNGs and recent log. ChatGPT's output-to-portrait pairing follows the supplied file numbers and visual inspection because its PNGs have no embedded workflow metadata. Earlier informal I2I timing is not a published comparison.
- `benchmarks/t2i-outfit-reference.md` has both original outputs and one 89.43-second Qwen cold-start observation. The Qwen dress was selected as the shared reference for both outfit-edit cases. The operator confirmed identical submitted prompt text for both T2I systems; the ChatGPT PNG itself has no generation metadata.
- `benchmarks/t2i-goat.md` has both original outputs and a 63.78-second Qwen log observation matched to its original PNG. The pair is ready for review; the reference for the later goat-outfit edit has not been selected.
- `benchmarks/i2i-change-outfit.md` has four edited originals organized into two portrait cases. The three input copies match their T2I originals by hash, and the site shows the input lineage, prompt and both side-by-side pairs.

## Iterative workflow

1. Propose one narrow roadmap task in `benchmarks/<test-id>.md`, including the recommended shared prompt, rationale, intended settings, review criteria and planned file paths. Mark it `planned` and awaiting approval. Preserve already submitted prompts. Do not create its image/artifact directories or public section until the user approves the proposal.
2. After approval, create the task's model output directories and artifact directory, then create `benchmarks/records/<test-id>.json` from `benchmarks/record-template.json`. Expand the Markdown handoff using `benchmarks/record-template.md` as needed and mark it `awaiting outputs`. Keep missing outputs labeled as awaiting runs. The site builder renders the structured record and its task heading automatically appears in the sidebar; do not edit `site/bench/index.md` to add an individual task.
3. Give the operator the prompt and intended workflow/configuration. The operator runs Qwen and ChatGPT, then copies the original output PNGs and any I2I inputs into the repository. Do not assume a run occurred because a section was prepared.
4. Import the supplied images using the naming convention below. For an approved one-sample T2I pair, copy both original PNGs into their standardized paths and run `.venv-site/bin/python scripts/post_generation.py --test-id <test-id>`. First use `--check` if the prompt or timing needs inspection. The script reads only the recent log tail, archives Qwen PNG workflow metadata, records hashes and settings, and rebuilds the site. It does not re-encode images or invent an unmatched timing. Preserve explicitly supplied exports too. For I2I or multi-sample runs, follow the manual record procedure until the script supports them.
5. Gather dated host and Python reports using HARDWARE.md and METHODS.md. Capture the real ComfyUI revision, launch command, resolved package set, requirements/launcher/model/input hashes and exact workflow. Label records collected later as snapshots rather than run-time evidence.
   When timing is requested, run ComfyUI with the INFO log described in METHODS.md. Queue one image at a time, and pair each output filename with its corresponding `Prompt executed in` line. Inspect only a short log tail. The importer matches the original Qwen PNG by hash, then uses its save time to identify a unique recent log entry; it leaves timing blank if the match is ambiguous. Mark cold starts, retries and missing durations explicitly; do not infer duration from filenames or file modification times alone.
6. Update the structured record's outputs, exact prompt links, settings and artifacts. The site builder renders the prompt above equal-width image panels, each with its actual model label, dimensions, meaningful alt text and full-resolution link. It places settings and reproduction artifacts in an expandable section.
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

## Roadmap with generated prerequisites

All benchmark images, including editing inputs and reference assets, come from recorded T2I runs. The ten comparison goals now require fourteen new stages, plus the existing `t2i-realistic-character` baseline. Each new stage is its own benchmark task with the same iterative workflow and its own `benchmarks/<test-id>.md` record. These are proposed tasks, not completed runs or final prompts.

| Stage | Task | Test ID | Inputs or dependency | Main checks |
| --- | --- | --- | --- | --- |
| 1 | T2I Outfit reference | `t2i-outfit-reference` | Text only; generate a clearly visible replacement outfit on a mannequin or as a flat lay. | Garment structure, materials, color and visibility of the outfit. |
| 2 | I2I Change outfit | `i2i-change-outfit` | Existing generated portrait + outfit reference from stage 1. | Transfer the reference outfit while retaining face, hair, pose, framing and background. |
| 3 | T2I Goat | `t2i-goat` | Text only; generate one clearly specified goat. | Anatomy, coat, horns, hooves and pose. |
| 4 | T2I Goat outfit reference | `t2i-goat-outfit-reference` | Text only; generate clothing appropriate to the goat from stage 3, with visible garment details. | Clear garment design and suitability for a goat. |
| 5 | I2I Change goat outfit | `i2i-change-goat-outfit` | Goat from stage 3 + goat outfit reference from stage 4. | Transfer the reference clothing while retaining goat identity, anatomy, pose and background. |
| 6 | T2I Second character | `t2i-second-character` | Text only; generate a distinct second person with compatible framing for a group portrait. | Anatomy, visible face and distinguishing appearance. |
| 7 | I2I Group picture | `i2i-group-picture` | Existing generated portrait + second character from stage 6. | Combine both subjects into one portrait; inspect identities, count, placement and consistent lighting. |
| 8 | T2I Object counting and placement | `t2i-counting-placement` | Text only; generate a small fixed number of distinct objects, including one isolated removal target. | Count, specified left/right relationships and correct attribute assignment. |
| 9 | T2I Text on a sign | `t2i-text-sign` | Text only. | Exact short phrase, spelling, legibility and integration with the scene. |
| 10 | T2I Materials and lighting | `t2i-materials-lighting` | Text only; generate a simple glass, metal and fabric still life. | Material differences, reflections and shadow consistency. |
| 11 | T2I Illustration style | `t2i-illustration-style` | Text only; generate a simple subject in one specified medium. | Subject adherence and consistent visual treatment. |
| 12 | T2I Background reference | `t2i-background-reference` | Text only; generate an empty target setting with space for the portrait subject. | Scene instructions, perspective and coherent lighting. |
| 13 | I2I Change background | `i2i-change-background` | Existing generated portrait + background reference from stage 12. | Transfer the subject into the reference setting while retaining identity, clothing and pose; inspect framing, edges and lighting compatibility. |
| 14 | I2I Remove an object | `i2i-remove-object` | Generated scene from stage 8; identify the fixed removal target in text. | Remove only that object, retain the remaining count/placement, and reconstruct a plausible background without fragments. |

The original ten goals remain; four T2I reference tasks have been added for clothing, goat clothing, a second person and a target background. Object removal reuses the counting scene, so it needs no separate source-image task. The existing portrait is already AI-generated and need not be regenerated unless its framing is unsuitable for a specific edit. If a replacement is necessary, add and record that T2I prerequisite before proceeding.

The outfit tasks use two inputs: a subject image and a generated garment reference. The group task uses two generated subject references. The background task uses a subject image and a generated setting reference. Record the role and order of each image in the actual I2I workflow. Confirm the intended subjects and group arrangement when preparing stage 7.

## Generated input selection and lineage

Run each prerequisite T2I task through both systems with the same prompt and retain both outputs as a comparison. Choose and record a fixed reference set before running its dependent I2I task. Give both editors the **same original input files in the same roles and order**, rather than automatically feeding each system its own T2I outputs. This compares editing on shared inputs; a separate model-specific end-to-end chain can be added later if requested.

Before each T2I prerequisite, define what makes its outputs usable as references: for example, visible garment details or enough empty space in a background. Record the selection rule, selected model/sample and any failed attempts or retries. Retain all requested samples; selecting a reference does not remove the other model's result from the T2I comparison. If no sample is usable, record the prerequisite failure and wait for a usable generated source instead of importing an external photograph.

For every I2I input, record its originating T2I test ID, generating model/sample, original output path and SHA-256 hash. Copy the selected original into `site/assets/images/<i2i-test-id>/inputs/input-001.png` (and `input-002.png` as needed) without re-encoding. The input copy and originating output must have identical hashes. Keep the original generation prompt and workflow with the T2I task and link them from the dependent edit record. The site's edit section should show its input references before the edit prompt and the side-by-side output panels.

These stages add counting, text, materials, style, subject preservation and scene reconstruction to the user's four starting proposals. Keep each initial task small enough that a viewer can judge the intended result directly.

## Reusable task procedure

The iterative workflow is the common procedure; each task record supplies its specific inputs and checks. There is no need for ten separate skills that duplicate the same instructions.

Before handing a task to the operator, fill in these fields in its individual record:

- Task ID and the single capability being tested.
- Shared prompt and output aspect ratio; preserve the exact final submitted text.
- Fixed input files, hashes, originating T2I test/model/sample and reference order for I2I, including a subject-to-reference mapping for group composition.
- T2I prerequisite dependencies, usable-reference criteria and the recorded input selection rule.
- Requested changes and properties that must remain unchanged for edits.
- A short list of observable checks from the roadmap, with task-specific details.
- Intended Qwen workflow/settings and the operator's ChatGPT model label. Record actual settings separately after the runs.

Use the same inputs and prompt for both systems. Agree on the sample count before running; retain every requested sample with consecutive numbers rather than selecting only the most favorable output. Record failed runs and retries. Different systems need not expose equivalent seeds or sampler controls; mark unavailable settings explicitly.

For Qwen Image 2.1 I2I prompts, refer to the numbered workflow inputs with the literal tags `<image1>`, `<image2>`, and so on, as shown in `workflows/image_qwen_image_2_1_image_edit.json`. The first image is the edit target and later images are references. Preserve those tags in the shared prompt sent to both systems; document which original file occupies each slot.

Advance each record through `planned` → `awaiting outputs` → `ready for review` → `published`. In preparation, create the section and run handoff; wait for the user to run it and supply files. On import, verify the originals, collect artifacts and show both outputs. During review, describe adherence and unintended changes using the predefined checks, then build the site. Publishing is a separate user-authorized step. Do not mark a task published merely because its files exist locally.

## Files and naming

```text
site/bench/index.md
benchmarks/records/<test-id>.json
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

The structured JSON is the site display source. Its `group` (`t2i` or `i2i`) and numeric `order` determine task position and sidebar order. `outputs` lists only verified, imported originals; `pending_models` names missing outputs. The Markdown file remains the operator handoff and detailed run log. See `benchmarks/record-template.json` for the format and `benchmarks/records/README.md` for field rules. Keep those sources consistent when changing a result.

## Manifest format

`path_base` is `site/`. Each `files` key is a site-relative path, such as `assets/images/t2i-realistic-character/qwen-image-2-1/output-001.png`; its value contains `sha256` and `bytes`. Do not include the manifest itself in its hash list. Historical setup manifests use a `date`, `scope`, `comfyui_commit` and filename-to-hash map; retain their format and provenance.
