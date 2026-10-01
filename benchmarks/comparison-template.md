# Comparison page pattern

Public comparison sections are generated from `benchmarks/records/<test-id>.json`. Start with [`record-template.json`](record-template.json) and read [`records/README.md`](records/README.md) for required fields. Keep the detailed run handoff and raw observations in `benchmarks/<test-id>.md`.

The site builder places sections by `group` and `order`. It renders the readable prompt first, then equal-width panels for the available original PNGs. A missing output appears as a labeled pending panel. Exact submitted prompts, run settings and reproducibility artifacts appear in expandable details below the images. Do not edit `site/bench/index.md` to insert a task; that file is the comparison-page introduction only.

Use `site/assets/images/<test-id>/<model-id>/output-001.png` for originals and `site/data/<test-id>/` for prompt, workflow and manifest artifacts. Preserve original bytes and mark unavailable settings rather than inferring them.
