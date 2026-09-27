# Benchmark repository instructions

- The public site lives in `site/`; build it with `python scripts/build_site.py` after installing `requirements-site.txt`. `_site/` is generated and must not be committed.
- The public prompt-process explanation is: "ChatGPT was used to generate the prompts used." Keep the comparison images as the site's focus. Preserve existing submitted prompts verbatim and use the same submitted prompt for both models.
- Store outputs at `site/assets/images/<test-id>/<model-id>/output-001.png` and I2I inputs at `site/assets/images/<test-id>/inputs/input-001.png`. Use lowercase hyphenated identifiers, three-digit sample numbers, and the same test ID under `site/data/` and `benchmarks/`. Record exact model labels and configuration details in the comparison record.
- Retain original images without re-encoding, exact workflow exports, input images for I2I, and SHA-256 manifests under `site/assets/` and `site/data/`.
- Record dated host and environment information with each measured run. Distinguish current host snapshots from per-run evidence. Do not infer missing timings, seeds, model identities, or results.
