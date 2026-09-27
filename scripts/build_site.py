#!/usr/bin/env python3
"""Build the public site and fail on broken local links or fragment targets."""
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from shutil import copytree, rmtree
from string import Template
from urllib.parse import unquote, urlsplit
import markdown

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site"
OUTPUT = ROOT / "_site"


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


def build():
    # The output directory is generated; remove stale assets after renames.
    if OUTPUT.exists():
        rmtree(OUTPUT)
    OUTPUT.mkdir(exist_ok=True)
    for directory in ("assets", "data"):
        copytree(SOURCE / directory, OUTPUT / directory, dirs_exist_ok=True)
    template = Template((SOURCE / "templates/page.html").read_text())
    for source in sorted(SOURCE.glob("*.md")):
        renderer = markdown.Markdown(extensions=["tables", "fenced_code", "toc"],
                                     extension_configs={"toc": {"toc_depth": "2-3"}})
        content = renderer.convert(source.read_text())
        content = content.replace("<table>", '<div class="table-scroll" tabindex="0" role="region" aria-label="Data table"><table>').replace("</table>", "</table></div>")
        title = source.read_text().splitlines()[0].removeprefix("# ")
        (OUTPUT / (source.stem + ".html")).write_text(template.substitute(
            title=escape(title), content=content, toc=renderer.toc))
    parsed = {}
    for page in OUTPUT.glob("*.html"):
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
            if not destination.is_relative_to(OUTPUT.resolve()):
                errors.append(f"{page.name}: link escapes site: {target}")
            elif not destination.exists():
                errors.append(f"{page.name}: missing target: {target}")
            elif url.fragment and destination in parsed and unquote(url.fragment) not in parsed[destination].ids:
                errors.append(f"{page.name}: missing fragment: {target}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Built {len(parsed)} pages; all local links and fragments resolve.")


if __name__ == "__main__":
    build()
