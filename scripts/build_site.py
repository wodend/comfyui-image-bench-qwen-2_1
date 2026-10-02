#!/usr/bin/env python3
"""Render four public pages from repository context; validate links and artifacts."""
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from shutil import copytree, rmtree
from string import Template
from urllib.parse import unquote, urlsplit
import hashlib
import json
import re
import struct
import markdown

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site"
OUTPUT = ROOT / "_site"
RECORDS = ROOT / "benchmarks/records"


def comparison_markdown():
    """Render benchmark records; group/order determine their place on the page."""
    records = [(path, json.loads(path.read_text())) for path in sorted(RECORDS.glob("*.json"))]
    seen = set()
    for record_path, record in records:
        key = (record["group"], record["order"])
        if (record["schema_version"] != 1 or record["group"] not in ("t2i", "i2i")
                or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", record["id"])
                or record_path.stem != record["id"]
                or key in seen or record["status"] not in ("complete", "awaiting outputs")):
            raise ValueError(f"Invalid or duplicate benchmark record: {record['id']}")
        seen.add(key)
        present_models = {output["model_id"] for output in record["outputs"]}
        pending_models = {pending["model_id"] for pending in record["pending_models"]}
        if (present_models & pending_models or
                (record["status"] == "complete" and (pending_models or not {"qwen-image-2-1", "chatgpt"} <= present_models))):
            raise ValueError(f"Inconsistent output status: {record['id']}")
        for output in record["outputs"]:
            path = SOURCE / output["path"]
            if not path.is_file() or not path.resolve().is_relative_to(SOURCE.resolve()):
                raise ValueError(f"Missing benchmark output: {path}")
            with path.open("rb") as image_file:
                header = image_file.read(24)
            if header[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", header[16:24]) != (output["width"], output["height"]):
                raise ValueError(f"Incorrect PNG dimensions: {path}")
        for input_image in record.get("inputs", []):
            path = SOURCE / input_image["path"]
            original = SOURCE / input_image["source_output"]
            if (not path.is_file() or not original.is_file()
                    or not path.resolve().is_relative_to(SOURCE.resolve())
                    or not original.resolve().is_relative_to(SOURCE.resolve())):
                raise ValueError(f"Missing or invalid benchmark input: {path}")
            actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual_hash != input_image["sha256"] or hashlib.sha256(original.read_bytes()).hexdigest() != actual_hash:
                raise ValueError(f"Input lineage hash mismatch: {path}")
            with path.open("rb") as image_file:
                header = image_file.read(24)
            if header[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", header[16:24]) != (input_image["width"], input_image["height"]):
                raise ValueError(f"Incorrect input PNG dimensions: {path}")
        output_paths = {output["path"] for output in record["outputs"]}
        input_paths = {input_image["path"] for input_image in record.get("inputs", [])}
        for case in record.get("cases", []):
            if (not set(case["input_paths"]) <= input_paths
                    or not set(case["output_paths"]) <= output_paths):
                raise ValueError(f"Invalid input or output path in case: {record['id']}")
        for entry in record["artifacts"]:
            if not (SOURCE / entry[1]).is_file():
                raise ValueError(f"Missing benchmark artifact: {entry[1]}")
    result = []
    for _, record in sorted(records, key=lambda item: ((0 if item[1]["group"] == "t2i" else 1), item[1]["order"])):
        prompt = record["prompt"]
        result += [f'## {record["title"]} {{#{record["id"]}}}', '']
        if record.get("inputs"):
            result += ['### Inputs', '', '<div class="comparison inputs" aria-label="Editing inputs">']
            for input_image in record["inputs"]:
                path = escape(input_image["path"])
                result += [f'<figure><a href="{path}"><img src="{path}" width="{input_image["width"]}" height="{input_image["height"]}" alt="{escape(input_image["alt"])}"></a>',
                           f'<figcaption><strong>{escape(input_image["label"])}</strong><span>{escape(input_image["role"])}</span><a href="{path}" download>Download original input PNG</a></figcaption></figure>']
            result += ['</div>', '']
        result += ['<blockquote class="prompt"><p>' + escape(prompt["display"]) + '</p></blockquote>', '',
                   f'Requested aspect ratio: **{prompt["aspect_ratio"]}**.', '']
        output_by_path = {output["path"]: output for output in record["outputs"]}
        cases = record.get("cases") or [{"title": record["title"], "output_paths": list(output_by_path)}]
        for case in cases:
            if record.get("cases"):
                result += [f'### {case["title"]}', '']
            result += [f'<div class="comparison" aria-label="{escape(case["title"])} comparison">']
            for output_path in case["output_paths"]:
                output = output_by_path[output_path]
                label, path = escape(output["label"]), escape(output["path"])
                result += [f'<figure><a href="{path}"><img src="{path}" width="{output["width"]}" height="{output["height"]}" alt="{escape(output["alt"])}"></a>',
                           f'<figcaption><strong>{label}</strong><span>{escape(output["caption"])}</span><a href="{path}" download>Download original PNG</a></figcaption></figure>']
            if not record.get("cases"):
                for pending in record["pending_models"]:
                    result += [f'<div class="pending-panel"><strong>{escape(pending["label"])}</strong><span>{escape(pending["message"])}</span></div>']
            result += ['</div>', '']
        result += ['<details markdown="1">', '<summary>Run settings and reproduction artifacts</summary>', '',
                   '### Exact submitted prompt', '', prompt["note"], '']
        shown_prompts = set()
        for model, path in prompt["submitted"].items():
            if path:
                if path in shown_prompts:
                    continue
                shown_prompts.add(path)
                exact = (SOURCE / path).read_text().strip()
                result += ['```json', exact, '```', '']
        result += ['### Recorded settings', '', '| Setting | Qwen Image 2.1 | ChatGPT |', '| --- | --- | --- |']
        for row in record["settings"]:
            result.append('| ' + ' | '.join(row) + ' |')
        result += ['', *[note + '\n' for note in record["notes"]],
                   '### Reproduction artifacts', '']
        for label, path in record["artifacts"]:
            result.append(f'- [{label}]({path})')
        result += ['', '</details>', '']
    return '\n'.join(result)


def public_block(filename):
    text = (ROOT / filename).read_text()
    return text.split("<!-- public:start -->", 1)[1].split("<!-- public:end -->", 1)[0].strip()


def render(text):
    renderer = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "md_in_html", "attr_list"],
                                 extension_configs={"toc": {"toc_depth": "2"}})
    content = renderer.convert(text)
    content = content.replace("<table>", '<div class="table-scroll" tabindex="0" role="region" aria-label="Data table"><table>').replace("</table>", "</table></div>")
    return content, renderer.toc, renderer.toc_tokens


def rebase(html, prefix):
    """Public source paths are site-root relative; fragments stay on the page."""
    def replace(match):
        target = match[2]
        url = urlsplit(target)
        if target.startswith("#") or url.scheme or url.netloc:
            return match[0]
        return f'{match[1]}="{prefix}{target}"'
    return re.sub(r'(href|src)="([^"]*)"', replace, html)


def task_headings(tokens):
    for token in tokens:
        if token["level"] == 2:
            yield token
        yield from task_headings(token["children"])


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if key in attrs:
                self.targets.append(attrs[key])


def validate():
    parsed = {}
    for page in OUTPUT.rglob("*.html"):
        parser = Links()
        parser.feed(page.read_text())
        parsed[page.resolve()] = parser
    errors = []
    for page, parser in parsed.items():
        for target in parser.targets:
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            destination = (page.parent / unquote(url.path)).resolve() if url.path else page
            if destination.is_dir():
                destination /= "index.html"
            if not destination.is_relative_to(OUTPUT.resolve()):
                errors.append(f"{page.relative_to(OUTPUT)}: link escapes site: {target}")
            elif not destination.exists():
                errors.append(f"{page.relative_to(OUTPUT)}: missing target: {target}")
            elif url.fragment and destination in parsed and unquote(url.fragment) not in parsed[destination].ids:
                errors.append(f"{page.relative_to(OUTPUT)}: missing fragment: {target}")
    for path in (OUTPUT / "data").rglob("manifest.json"):
        manifest = json.loads(path.read_text())
        for name, entry in manifest["files"].items():
            target = OUTPUT / name if manifest.get("path_base") == "site/" else path.parent / name
            if not target.resolve().is_relative_to(OUTPUT.resolve()) or not target.is_file():
                errors.append(f"{path.name}: missing or invalid artifact: {name}")
                continue
            expected = entry["sha256"] if isinstance(entry, dict) else entry
            if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
                errors.append(f"{path.name}: hash mismatch: {name}")
            if isinstance(entry, dict) and target.stat().st_size != entry["bytes"]:
                errors.append(f"{path.name}: size mismatch: {name}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Built {len(parsed)} pages; all local links, anchors and artifact hashes pass.")


def build():
    # Generated output must not retain removed pages or renamed images.
    if OUTPUT.exists():
        rmtree(OUTPUT)
    OUTPUT.mkdir()
    for directory in ("assets", "data"):
        copytree(SOURCE / directory, OUTPUT / directory)
    pages = {
        "": (ROOT / "README.md").read_text(),
        "bench": (SOURCE / "bench/index.md").read_text() + "\n" + comparison_markdown(),
        "hardware": public_block("HARDWARE.md"),
        "methods": public_block("METHODS.md"),
    }
    rendered = {route: render(text) for route, text in pages.items()}
    task_links = ''.join(f'<li><a href="bench/#{escape(token["id"])}">{escape(token["name"])}</a></li>'
                         for token in task_headings(rendered["bench"][2]))
    template = Template((SOURCE / "templates/page.html").read_text())
    for route, text in pages.items():
        content, toc, _ = rendered[route]
        nav = ''.join(f'<a href="{target + "/" if target else "./"}"'
                      f'{" aria-current=\"page\"" if target == route else ""}>{label}</a>'
                      for target, label in [("", "Home"), ("bench", "Benchmarks"), ("hardware", "Hardware"), ("methods", "Methods")])
        if route == "bench":
            sidebar = '<nav aria-label="Benchmark tasks"><h2>Benchmarks</h2><ul>' + task_links + '</ul></nav>'
        elif route in ("hardware", "methods"):
            sidebar = '<nav class="page-index" aria-label="On this page"><h2>On this page</h2>' + toc + '</nav>'
        else:
            sidebar = ''
        if not route:
            content += '<div class="home-links"><a class="primary-link" href="bench/">Explore the comparisons →</a><a href="hardware/">View hardware</a><a href="methods/">Read the methods</a></div>'
        html = template.substitute(title=escape(text.splitlines()[0].removeprefix("# ")),
                                   content=content, nav=nav,
                                   sidebar=f'<aside class="sidebar">{sidebar}</aside>' if sidebar else '',
                                   shell_class='no-sidebar' if not sidebar else '')
        destination = OUTPUT / route
        destination.mkdir(exist_ok=True)
        (destination / "index.html").write_text(rebase(html, "../" if route else ""))
    validate()


if __name__ == "__main__":
    build()
