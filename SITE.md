# Site maintenance

Agent/operator instructions for the website. These instructions are not public page content. Benchmark operation belongs in METHODS.md; task preparation belongs in BENCH.md.

## Sources and routes

| Source | Public route |
| --- | --- |
| `README.md` | `/` |
| Public block in `HARDWARE.md` | `/hardware/` |
| Public block in `METHODS.md` | `/methods/` |
| `site/bench/index.md` plus `benchmarks/records/*.json` | `/bench/` |

Public blocks are delimited by `<!-- public:start -->` and `<!-- public:end -->`. Keep operational instructions outside these blocks. The builder renders only the listed sources, orders comparison records by `group` and `order`, then copies `site/assets/` and `site/data/`.

The benchmark task sidebar appears only on `/bench/`. Hardware and Methods have indexes of their own headings; Home has no sidebar. Individual benchmark sections begin with the prompt and aspect ratio after the heading (and I2I input images when applicable), followed by original output panels. Run details stay in the expandable section.

Links in public Markdown use paths relative to the generated site root, such as `bench/`, `hardware/`, `methods/`, `assets/images/...` and `data/...`. The builder rebases them for each route, preserving GitHub project-path and custom-domain compatibility. Do not hard-code a host into navigation. Use `/bench/#<test-id>` for direct task links.

## Build and preview

```bash
python3 -m venv .venv-site
.venv-site/bin/python -m pip install -r requirements-site.txt
.venv-site/bin/python scripts/build_site.py
.venv-site/bin/python -m http.server 8000 --directory _site
```

Reuse an existing `.venv-site` rather than recreating it. Open `http://localhost:8000/bench/`. Check the home/header links, sidebar heading jumps, prompt placement, full-size downloads, expandable run details, and mobile layout. The build removes stale generated files and validates all local links, fragment targets and file manifests. `_site/` and `.venv-site/` are ignored by Git.

## Deployment

`.github/workflows/pages.yml` builds and validates pull requests. Pushes to `main` and manual runs on `main` also deploy `_site/` using `actions/deploy-pages`. GitHub repository Settings → Pages → Source must be GitHub Actions.

The deployment environment link is `${{ steps.deployment.outputs.page_url }}`: GitHub supplies the actual host. The conventional project address is `https://wodend.github.io/comfyui-image-bench-qwen-2_1/`, but the user reported GitHub displaying `http://estoff.cc/comfyui-image-bench-qwen-2_1/`. This repository has no custom domain configuration. A custom domain on the account’s main Pages site can be inherited by project sites; that account setting has not been independently verified. Use the successful deployment’s assigned URL when testing.

Commit and push release changes only when requested. Do not add generated output to Git or alter domain settings merely to publish site changes.
