# ComfyUI Image Bench · Qwen 2.1

A GitHub Pages site comparing local Qwen Image 2.1 in ComfyUI with ChatGPT image outputs using shared prompts. Includes side-by-side original images, workflow exports, prompt records, and dated hardware and software information.

The first comparison follows the supplied [draft](bench.md). It is a visual example, with exact Qwen settings recovered from the PNG; controlled timings are not yet available.

- [Comparisons](site/index.md)
- [Benchmark hardware](site/hardware.md)
- [ComfyUI and Python setup](site/software.md)
- [Method and prompts](site/methodology.md)

ChatGPT was used to generate the prompts used.

## Build and preview

```bash
python3 -m venv .venv-site
.venv-site/bin/python -m pip install -r requirements-site.txt
.venv-site/bin/python scripts/build_site.py
.venv-site/bin/python -m http.server 8000 --directory _site
```

Open `http://localhost:8000`. The build checks every local link, image reference, and heading anchor. Relative URLs also work under the GitHub project Pages path.

## Publish on GitHub Pages

In the repository’s **Settings → Pages → Build and deployment**, set **Source** to **GitHub Actions**. The workflow builds and validates pull requests; pushes to `main` and manual runs on `main` deploy the site. The expected URL after the first successful deployment is https://wodend.github.io/comfyui-image-bench-qwen-2_1/.

This update prepares deployment files locally; it has not yet been published.

## Repository layout

| Path | Purpose |
| --- | --- |
| `site/*.md` | Public comparison and reproducibility pages |
| `site/templates/` | Shared page layout and automatic sidebar index |
| `site/assets/` | Styling and original comparison images |
| `site/data/` | Exact prompts, run workflows, and hash manifests |
| `benchmarks/` | Templates for future comparison and measured run records |
| `src/` | Existing ComfyUI setup, launcher, and inventory scripts |
| `scripts/build_site.py` | Static site build and link validation |
| `workflows/` | Earlier image editing workflow, retained as reference |
| `bench.md` | Original editorial draft |

Use the [official Qwen Image 2.1 ComfyUI template](https://comfy.org/workflows/bb7e03924a5c-bb7e03924a5c/) as the starting point for Qwen runs. See [AGENTS.md](AGENTS.md) for image naming and benchmark record requirements.
