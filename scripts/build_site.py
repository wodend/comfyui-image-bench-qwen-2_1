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
import markdown

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site"
OUTPUT = ROOT / "_site"


def public_block(filename):
    text = (ROOT / filename).read_text()
    return text.split("<!-- public:start -->", 1)[1].split("<!-- public:end -->", 1)[0].strip()


def render(text):
    renderer = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "md_in_html"],
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
        "bench": (SOURCE / "bench/index.md").read_text(),
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
        sidebar = '<nav aria-label="Benchmark tasks"><h2>Benchmarks</h2><ul>' + task_links + '</ul></nav>'
        if route in ("hardware", "methods"):
            sidebar += '<nav class="page-index" aria-label="On this page"><h2>On this page</h2>' + toc + '</nav>'
        if not route:
            content += '<div class="home-links"><a class="primary-link" href="bench/">Explore the comparisons →</a><a href="hardware/">View hardware</a><a href="methods/">Read the methods</a></div>'
        html = template.substitute(title=escape(text.splitlines()[0].removeprefix("# ")),
                                   content=content, nav=nav, sidebar=sidebar)
        destination = OUTPUT / route
        destination.mkdir(exist_ok=True)
        (destination / "index.html").write_text(rebase(html, "../" if route else ""))
    validate()


if __name__ == "__main__":
    build()
