#!/usr/bin/env python3
"""Build the combined manuscript and the print-ready reading copies.

Outputs (all under manuscript/):
  BOOK.md    - single combined Markdown manuscript
  book.html  - self-contained print-ready HTML
  book.pdf   - 6x9 in PDF, rendered from book.html with WeasyPrint

The page design matches Book One of the series, "The Dubai Syndicate Way":
Carlito type, a royal-purple / magenta palette, full-page chapter openers,
and proper title, copyright and contents pages.

Usage:  python3 _scripts/build_book.py
"""

import html
import pathlib
import re

import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAN = ROOT / "manuscript"

BOOK_TITLE = "How to Start a Business in Dubai"
BOOK_SERIES = "The Dubai Syndicate Way"
BOOK_SUB = "The Practical Field Guide to 35 Industries"
BOOK_TAG = "From Restaurant to Real Estate, Salon to SaaS"
BOOK_AUTHOR = "Islam Inamdar"
BOOK_EDITION = "First Edition · 2026"
BOOK_PUBLISHER = "Published by Dubai Syndicate"

PARTS = [
    ("part-1-foundations", "Part One", "Foundations",
     "What every Dubai business shares — the city, the jurisdiction, "
     "the licence, the money, and the mindset."),
    ("part-2-industries", "Part Two", "The Field Guide",
     "Thirty-five industries, eight categories, one template — "
     "built to be read against each other."),
    ("part-3-resources", "Part Three", "Resources",
     "Directories, checklists, and tools to turn a decision "
     "into an application."),
]

esc = html.escape

H1_RE = re.compile(r"^#\s+(.+?)\s*$")
THEMATIC_RE = re.compile(r"^\s*([-*_])\1{2,}\s*$")
SUBTITLE_RE = re.compile(r"^\*[^*].*[^*]\*$|^\*[^*]\*$")
DOT = "·"


def ordered_files():
    files = [p for p in MAN.rglob("*.md")
             if p.name not in ("OUTLINE.md", "BOOK.md")]
    return sorted(files, key=lambda p: str(p).lower())


def part_key(path):
    for key, *_ in PARTS:
        if key in str(path):
            return key
    return ""


def part_meta(key):
    return next(p for p in PARTS if p[0] == key)


def slug(path):
    return path.relative_to(MAN).with_suffix("").as_posix().replace("/", "-")


def first_heading(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        m = H1_RE.match(line.strip())
        if m:
            return m.group(1).strip()
    return path.stem


def parse_file(path):
    """Return (h1, subtitle, body_markdown) for a chapter file.

    The leading kicker line (e.g. 'PART TWO - THE FIELD GUIDE'), the H1, the
    italic subtitle and the divider rule after it are pulled out as metadata;
    the remaining Markdown is the body.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    h1, idx = "", 0
    for i, line in enumerate(lines):
        m = H1_RE.match(line.strip())
        if m:
            h1, idx = m.group(1).strip(), i + 1
            break
    rest = lines[idx:]
    while rest and not rest[0].strip():
        rest.pop(0)
    subtitle = ""
    if rest and SUBTITLE_RE.match(rest[0].strip()):
        subtitle = rest[0].strip()[1:-1].strip()
        rest.pop(0)
    while rest and not rest[0].strip():
        rest.pop(0)
    if rest and THEMATIC_RE.match(rest[0]):
        rest.pop(0)
    return h1, subtitle, "\n".join(rest).strip()


def classify(path, h1):
    if path.name == "category-intro.md":
        return "category"
    if h1.startswith("Chapter "):
        return "chapter"
    if h1.startswith("Part "):
        return "partintro"
    return "resource"


def split_dot(text):
    if DOT in text:
        left, right = text.split(DOT, 1)
        return left.strip(), right.strip()
    return "", text.strip()


def md_to_html(body_md):
    md = markdown.Markdown(extensions=["extra", "sane_lists"])
    return md.convert(body_md)


def opener(eyebrow, title, subtitle, anchor):
    sub = f'<p class="op-sub">{esc(subtitle)}</p>' if subtitle else ""
    return (
        f'<section class="opener" id="{anchor}">'
        f'<p class="op-kicker">{esc(eyebrow)}</p>'
        f'<hr class="op-rule">'
        f'<h1 class="op-title">{esc(title)}</h1>'
        f'<hr class="op-rule">'
        f'{sub}</section>')


def article(anchor, body_html):
    return f'<article class="body" id="{anchor}-text">{body_html}</article>'


def toc_entry(badge, title, anchor):
    return (
        f'<li class="toc-ch"><a href="#{anchor}">'
        f'<span class="toc-badge">{esc(badge)}</span>'
        f'<span class="toc-title">{esc(title)}</span></a></li>')


# --------------------------------------------------------------------------

def build_combined_md(files):
    out = [f"# {BOOK_TITLE}\n",
           f"### {BOOK_SERIES}\n",
           f"**{BOOK_SUB}**\n",
           f"*{BOOK_TAG}*\n",
           f"\nBy {BOOK_AUTHOR}. {BOOK_EDITION}.\n\n---\n"]
    current = None
    for f in files:
        pk = part_key(f)
        if pk != current:
            current = pk
            _, label, name, blurb = part_meta(pk)
            out.append(f"\n\n# {label} — {name}\n\n*{blurb}*\n\n---\n")
        out.append("\n\n" + f.read_text(encoding="utf-8").strip() + "\n")
    (MAN / "BOOK.md").write_text("\n".join(out) + "\n", encoding="utf-8")


CSS = """
@page {
  size: 6in 9in;
  margin: 20mm 18mm 19mm;
  @bottom-center {
    content: counter(page);
    font-family: Carlito, Calibri, sans-serif;
    font-size: 9pt;
    color: #8f8f8f;
  }
}

* { box-sizing: border-box; }

html { font-size: 10.5pt; }

body {
  margin: 0;
  font-family: Carlito, Calibri, "Segoe UI", sans-serif;
  color: #1d1b19;
  line-height: 1.5;
  hyphens: manual;
}

p { margin: 0 0 0.62em; orphans: 2; widows: 2; }

.body p, .cat-intro p, .pi-body p { text-align: justify; }
.body p, .cat-intro p, .pi-body p,
.body li, .body td, .body th { hyphens: auto; }

a { color: inherit; text-decoration: none; }

/* ---- title page ------------------------------------------------------ */
.titlepage {
  text-align: center;
  padding-top: 1.35in;
  break-after: page;
}
.tp-series {
  text-transform: uppercase;
  letter-spacing: 0.23em;
  font-size: 11pt;
  color: #6f6a64;
  margin: 0 0 0.5in;
}
.tp-title {
  text-transform: uppercase;
  font-weight: 700;
  font-size: 28pt;
  line-height: 1.12;
  color: #6b2c7e;
  margin: 0 0 0.34in;
}
.tp-sub { font-size: 13pt; color: #46423d; margin: 0 0 0.1in; }
.tp-tag {
  font-style: italic;
  font-size: 11pt;
  color: #6f6a64;
  margin: 0 0 0.62in;
}
.tp-author {
  text-transform: uppercase;
  letter-spacing: 0.17em;
  font-weight: 700;
  font-size: 12.5pt;
  color: #46423d;
}

/* ---- copyright page -------------------------------------------------- */
.copyright {
  text-align: center;
  padding-top: 1.95in;
  break-after: page;
}
.cp-title { font-weight: 700; font-size: 12pt; margin: 0 0 0.14in; }
.cp-line { font-size: 10pt; color: #6f6a64; margin: 0; }
.cp-rights {
  font-size: 9.5pt;
  color: #6f6a64;
  line-height: 1.6;
  max-width: 3.6in;
  margin: 0.5in auto;
}
.cp-foot { font-size: 10pt; color: #6f6a64; margin: 0.04in 0; }

/* ---- contents -------------------------------------------------------- */
.contents { break-before: page; break-after: page; padding-top: 0.3in; }
.toc-head {
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.11em;
  font-size: 19pt;
  font-weight: 700;
  color: #6b2c7e;
  margin: 0 0 0.42in;
}
.toc { list-style: none; margin: 0 auto; padding: 0; max-width: 4.35in; }
.toc-part {
  text-transform: uppercase;
  font-weight: 700;
  font-size: 10pt;
  letter-spacing: 0.07em;
  color: #6b2c7e;
  margin: 0.34in 0 0.13in;
}
.toc-part:first-child { margin-top: 0; }
.toc-cat {
  font-weight: 700;
  font-size: 10pt;
  margin: 0.2in 0 0.07in;
  padding-left: 0.16in;
}
.toc-ch { font-size: 10pt; margin: 0.058in 0; padding-left: 0.34in; }
.toc-badge {
  display: inline-block;
  width: 0.46in;
  color: #6b2c7e;
  font-weight: 700;
}
.toc-title { color: #2c2825; }

/* ---- part dividers --------------------------------------------------- */
.part {
  break-before: page;
  break-after: page;
  text-align: center;
  padding-top: 2.55in;
}
.part-kicker {
  text-transform: uppercase;
  letter-spacing: 0.27em;
  font-size: 11pt;
  font-weight: 700;
  color: #b83b7e;
  margin: 0 0 0.22in;
}
.part-name {
  font-weight: 700;
  font-size: 25pt;
  text-transform: uppercase;
  color: #6b2c7e;
  margin: 0 0 0.22in;
}
.part-blurb {
  font-style: italic;
  color: #6f6a64;
  font-size: 11pt;
  line-height: 1.5;
  max-width: 3.6in;
  margin: 0 auto;
}

/* ---- chapter / resource openers ------------------------------------- */
.opener {
  break-before: page;
  text-align: center;
  padding-top: 1.5in;
}
.op-kicker {
  text-transform: uppercase;
  letter-spacing: 0.22em;
  font-size: 11pt;
  font-weight: 700;
  color: #b83b7e;
  margin: 0 0 0.16in;
}
.op-rule {
  border: 0;
  border-top: 0.8pt solid #c7b2cf;
  width: 100%;
  margin: 0.12in 0;
}
.op-title {
  font-weight: 700;
  font-size: 21pt;
  line-height: 1.18;
  text-transform: uppercase;
  color: #6b2c7e;
  margin: 0.13in 0;
}
.op-sub {
  font-style: italic;
  color: #6f6a64;
  font-size: 11pt;
  line-height: 1.5;
  max-width: 3.8in;
  margin: 0.26in auto 0;
}

/* ---- category openers ----------------------------------------------- */
.category { break-before: page; padding-top: 0.25in; }
.cat-kicker {
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 0.22em;
  font-size: 10.5pt;
  font-weight: 700;
  color: #b83b7e;
  margin: 0 0 0.1in;
}
.cat-title {
  text-align: center;
  font-weight: 700;
  font-size: 20pt;
  text-transform: uppercase;
  color: #6b2c7e;
  margin: 0 0 0.12in;
}
.cat-sub {
  text-align: center;
  font-style: italic;
  color: #6f6a64;
  font-size: 11pt;
  max-width: 3.9in;
  margin: 0 auto 0.34in;
}

/* ---- part-three intro ------------------------------------------------ */
.partintro { break-before: page; padding-top: 0.3in; }
.pi-sub {
  text-align: center;
  font-style: italic;
  color: #6f6a64;
  font-size: 12pt;
  line-height: 1.5;
  max-width: 4in;
  margin: 0 auto 0.36in;
}

/* ---- chapter body ---------------------------------------------------- */
.body { break-before: page; }
.body > :first-child { margin-top: 0; }
.body h2 {
  font-size: 12pt;
  font-weight: 700;
  color: #6b2c7e;
  line-height: 1.3;
  margin: 1.5em 0 0.5em;
  break-after: avoid;
}
.body h3 {
  font-size: 10.8pt;
  font-weight: 700;
  color: #1d1b19;
  margin: 1.25em 0 0.4em;
  break-after: avoid;
}
.body ul, .body ol { margin: 0.25em 0 0.85em; padding-left: 1.35em; }
.body li { margin: 0.26em 0; }
.body ul { list-style: disc; }
.body strong { font-weight: 700; }
.body hr { border: 0; border-top: 0.5pt solid #d8cbdd; margin: 1.1em 0; }
.body blockquote {
  margin: 1em 0;
  padding: 0.1em 0 0.1em 0.95em;
  border-left: 2.5pt solid #b83b7e;
  color: #555049;
  font-style: italic;
}
.body table {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
  font-size: 9pt;
}
.body th, .body td {
  border: 0.5pt solid #cbb9d2;
  padding: 4pt 6pt;
  text-align: left;
  vertical-align: top;
}
.body th { background: #f3edf5; color: #6b2c7e; font-weight: 700; }
"""


def build_html(files):
    sections = []
    toc = []
    current = None

    sections.append(
        '<section class="titlepage">'
        f'<p class="tp-series">{esc(BOOK_SERIES)}</p>'
        f'<h1 class="tp-title">{esc(BOOK_TITLE)}</h1>'
        f'<p class="tp-sub">{esc(BOOK_SUB)}</p>'
        f'<p class="tp-tag">{esc(BOOK_TAG)}</p>'
        f'<p class="tp-author">{esc(BOOK_AUTHOR)}</p>'
        '</section>')

    sections.append(
        '<section class="copyright">'
        f'<p class="cp-title">{esc(BOOK_TITLE)}</p>'
        f'<p class="cp-line">Copyright © 2026 {esc(BOOK_AUTHOR)}</p>'
        '<p class="cp-rights">All rights reserved. No part of this '
        'publication may be reproduced, distributed, or transmitted in any '
        'form or by any means without the prior written permission of the '
        'author, except in the case of brief quotations embodied in '
        'critical reviews.</p>'
        f'<p class="cp-foot">{esc(BOOK_EDITION)}</p>'
        '<p class="cp-foot">Book Two in <em>The Dubai Syndicate Way</em> '
        'series</p>'
        f'<p class="cp-foot">{esc(BOOK_PUBLISHER)}</p>'
        '</section>')

    body = []
    for f in files:
        pk = part_key(f)
        if pk != current:
            current = pk
            key, label, name, blurb = part_meta(pk)
            body.append(
                f'<section class="part" id="{key}">'
                f'<p class="part-kicker">{esc(label.upper())}</p>'
                f'<h1 class="part-name">{esc(name)}</h1>'
                f'<p class="part-blurb">{esc(blurb)}</p></section>')
            toc.append(
                f'<li class="toc-part"><a href="#{key}">'
                f'{esc(label.upper())} {DOT} {esc(name)}</a></li>')

        h1, subtitle, body_md = parse_file(f)
        kind = classify(f, h1)
        anchor = slug(f)
        body_html = md_to_html(body_md)

        if kind == "chapter":
            left, title = split_dot(h1)
            m = re.search(r"\d+", left)
            num = int(m.group()) if m else 0
            body.append(opener(f"Chapter {num:02d}", title, subtitle, anchor))
            body.append(article(anchor, body_html))
            toc.append(toc_entry(f"CH {num}", title, anchor))
        elif kind == "category":
            kicker, title = split_dot(h1)
            sub = f'<p class="cat-sub">{esc(subtitle)}</p>' if subtitle else ""
            body.append(
                f'<section class="category" id="{anchor}">'
                f'<p class="cat-kicker">{esc(kicker.upper())}</p>'
                f'<h1 class="cat-title">{esc(title)}</h1>'
                f'{sub}<div class="cat-intro">{body_html}</div></section>')
            toc.append(
                f'<li class="toc-cat"><a href="#{anchor}">'
                f'{esc(title)}</a></li>')
        elif kind == "partintro":
            sub = f'<p class="pi-sub">{esc(subtitle)}</p>' if subtitle else ""
            body.append(
                f'<section class="partintro" id="{anchor}">'
                f'{sub}<div class="pi-body">{body_html}</div></section>')
        else:  # resource
            m = re.search(r"resource-(\d+)", f.name)
            num = int(m.group(1)) if m else 0
            body.append(opener(f"Resource {num:02d}", h1, subtitle, anchor))
            body.append(article(anchor, body_html))
            toc.append(toc_entry("", h1, anchor))

    sections.append(
        '<section class="contents">'
        '<p class="toc-head">Contents</p>'
        '<ul class="toc">\n' + "\n".join(toc) + '\n</ul></section>')
    sections.extend(body)

    doc = (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, '
        'initial-scale=1">\n'
        f'<title>{esc(BOOK_TITLE)} — {esc(BOOK_SERIES)}</title>\n'
        '<style>' + CSS + '</style>\n</head>\n<body>\n'
        + "\n\n".join(sections)
        + '\n</body>\n</html>\n')
    (MAN / "book.html").write_text(doc, encoding="utf-8")


def build_pdf():
    try:
        from weasyprint import HTML
    except ImportError:
        print("  (WeasyPrint not installed - skipped book.pdf; "
              "install with: pip install weasyprint)")
        return
    HTML(filename=str(MAN / "book.html")).write_pdf(str(MAN / "book.pdf"))
    print("Built manuscript/book.pdf")


def main():
    files = ordered_files()
    build_combined_md(files)
    build_html(files)
    build_pdf()
    words = sum(len(f.read_text(encoding="utf-8").split()) for f in files)
    print(f"Built BOOK.md and book.html from {len(files)} files "
          f"(~{words:,} words).")


if __name__ == "__main__":
    main()
