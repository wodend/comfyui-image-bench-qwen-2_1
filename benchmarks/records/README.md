# Structured benchmark records

Each `<test-id>.json` file renders one public comparison section. Copy `../record-template.json` for a new task; do not copy that template into this directory. Keep the human run handoff and raw observations in `../<test-id>.md`.

- `id` must match the filename and image/data directory identifier. It becomes the heading anchor.
- `group` is `t2i` or `i2i`; `order` is a unique number within that group. T2I appears before I2I. These fields determine page and sidebar position; there is no hand-maintained list of sections.
- `status` is `awaiting outputs` or `complete`. A complete record has at least one original output from each comparison model. Pending outputs belong in `pending_models`, never as broken image links or stand-in pictures.
- `prompt.display` is the readable description shown above the images. `prompt.submitted` points to exact submitted-text files under `site/data/<test-id>/` where available. Say when a model's submitted string is unverified; never silently equate a plain-text description with a JSON wrapper.
- Each `outputs` entry has a model ID, label, site-relative PNG path, dimensions, alt text, caption, and optional timing (`duration_seconds`, `timing_kind`, `logged_at`). Timings must match a documented log entry and output file. Mark cold starts separately.
- `settings` rows are `[label, Qwen value, ChatGPT value]`. `notes` hold limits or observations. `artifacts` rows are `[label, site-relative path]`; link only files that exist.
- Keep original PNGs under `site/assets/images/<test-id>/<model-id>/` and workflow/prompt/hash evidence under `site/data/<test-id>/`. Update the SHA-256 manifest whenever artifacts are added.

Run `python scripts/build_site.py` after editing. It validates identifiers, group/order uniqueness, image dimensions, local links and manifest hashes. The generated `_site/` remains ignored by Git.
