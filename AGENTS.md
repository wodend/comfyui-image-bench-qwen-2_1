# Agent context

Read this file at the beginning of every conversation about this repository. Read the relevant context files before changing benchmarks or setup information:

- [HARDWARE.md](HARDWARE.md): dated host specifications, separate ComfyUI checkout, and inventory scripts.
- [METHODS.md](METHODS.md): benchmark Python environment, model setup, actual launcher and run capture instructions.
- [BENCH.md](BENCH.md): iterative benchmark preparation, image imports, task rationale and record conventions.
- [SITE.md](SITE.md): website build, preview, routing and deployment instructions.

## Sources of truth

`README.md` supplies the public home page. The marked public blocks in `HARDWARE.md` and `METHODS.md` supply the hardware and methods pages. Keep setup facts in those raw context files; do not maintain competing copies in public Markdown. The rest of those files and the agent/site instructions are not rendered into the website.

`site/bench/index.md` supplies only the comparison introduction. `benchmarks/records/<test-id>.json` supplies each task section; its `group` and `order` fields control the hierarchy. The main route is `/bench/`, with task links such as `/bench/#t2i-realistic-character`. The header links Home, Benchmarks, Hardware and Methods. The benchmark task sidebar appears only on `/bench/`; Hardware and Methods show their own page indexes, and Home has no sidebar.

## Benchmark rules

- Preserve existing submitted prompts verbatim and use the same submitted prompt for both models. Keep the site's focus on image comparisons. The one public sentence explaining prompt generation belongs in the methods page only.
- Store outputs at `site/assets/images/<test-id>/<model-id>/output-001.png`; I2I inputs at `site/assets/images/<test-id>/inputs/input-001.png`. Use lowercase hyphenated IDs and three-digit sample numbers. Use the same test ID under `site/data/` and `benchmarks/`.
- Retain original image bytes and metadata without re-encoding, exact workflow exports, input images, and SHA-256 manifests. Record actual model labels and configuration details.
- Record dated host and environment information with measured runs. Distinguish current setup snapshots from per-run evidence. Do not infer missing timings, seeds, model identities or conclusions.
- Generate all editing inputs and references through recorded T2I tasks. Track prerequisite IDs and input lineage in each record, and give both editors the same selected original files. See BENCH.md for the dependency roadmap.
- Usually the agent prepares a task and the user runs it and supplies files later. Keep pending tasks clearly labeled, and never substitute generated examples for actual benchmark outputs.

## Working on the site

Install `requirements-site.txt` and run `python scripts/build_site.py`. The build checks local links, heading anchors and archived file hashes. `_site/` is generated and must not be committed. Desktop comparisons use two equal-width panels with uncropped images at their natural aspect ratios; small screens stack panels. Keep the prompt above the images. Put long settings and artifact details in expandable sections.

The ComfyUI checkout and its virtual environment are separate from the website’s `.venv-site`. Do not run installation recipes or change the benchmark environment merely to edit documentation. Changes to dated setup facts require new evidence.
