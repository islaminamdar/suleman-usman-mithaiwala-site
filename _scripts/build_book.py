#!/usr/bin/env python3
"""Build a single combined manuscript (manuscript/BOOK.md) and a readable,
self-contained reading copy (manuscript/book.html) from the per-chapter
Markdown files under manuscript/.

Usage:  python3 _scripts/build_book.py
"""

import pathlib
import re
import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAN = ROOT / "manuscript"

BOOK_TITLE = "How to Start a Business in Dubai"
BOOK_SERIES = "The Dubai Syndicate Way"
BOOK_SUB = "The Practical Field Guide to 35 Industries"
BOOK_TAG = "From Restaurant to Real Estate, Salon to SaaS"

PARTS = [
    ("part-1-foundations", "Part One", "Foundations",
     "What every Dubai business shares — the city, the jurisdiction, "
     "the licence, the money, and the mindset."),
    ("part-2-industries", "Part Two", "The Field Guide",
     "Thirty-five industries, eight categories, one template — "
     "six pages each, built to be compared."),
    ("part-3-resources", "Part Three", "Resources",
     "Directories, checklists, and tools to turn a decision "
     "into an application."),
]
PART_IDS = {"Part One": "part-one", "Part Two": "part-two",
            "Part Three": "part-three"}


def ordered_files():
    files = [p for p in MAN.rglob("*.md")
             if p.name not in ("OUTLINE.md", "BOOK.md")]
    return sorted(files, key=lambda p: str(p).lower())


def first_heading(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"#\s+(.*)", line.strip())
        if m:
            return m.group(1).strip()
    return path.stem


def part_key(path):
    for key, *_ in PARTS:
        if key in str(path):
            return key
    return ""


def slug(path):
    return path.relative_to(MAN).with_suffix("").as_posix().replace("/", "-")


def build_combined_md(files):
    out = [f"# {BOOK_TITLE}\n",
           f"### {BOOK_SERIES}\n",
           f"**{BOOK_SUB}**\n",
           f"*{BOOK_TAG}*\n",
           "\n*Book Two — working draft.*\n\n---\n"]
    current = None
    for f in files:
        pk = part_key(f)
        if pk != current:
            current = pk
            label, name, blurb = next((n, nm, bl) for k, n, nm, bl in PARTS
                                       if k == pk)
            out.append(f"\n\n# {label} — {name}\n\n*{blurb}*\n\n---\n")
        out.append("\n\n" + f.read_text(encoding="utf-8").strip() + "\n")
    (MAN / "BOOK.md").write_text("\n".join(out) + "\n", encoding="utf-8")


def render_article(path):
    md = markdown.Markdown(extensions=["extra", "sane_lists"])
    html = md.convert(path.read_text(encoding="utf-8").strip())
    html = html.replace("<p>", '<p class="eyebrow">', 1)
    html = re.sub(r"(</h1>\s*)<p>", r'\1<p class="subtitle">', html, count=1)
    return f'<article id="{slug(path)}">\n{html}\n</article>'


def build_html(files):
    toc, body = [], []
    current = None
    for f in files:
        pk = part_key(f)
        if pk != current:
            current = pk
            label, name, blurb = next((n, nm, bl) for k, n, nm, bl in PARTS
                                       if k == pk)
            pid = PART_IDS[label]
            body.append(
                f'<section class="part" id="{pid}"><div class="part-inner">'
                f'<p class="part-kicker">{label}</p><h1>{name}</h1>'
                f'<p class="part-blurb">{blurb}</p></div></section>')
            toc.append(f'<li class="toc-part">'
                       f'<a href="#{pid}">{label} — {name}</a></li>')
        title = first_heading(f)
        if f.name == "category-intro.md":
            cls = "toc-cat"
        elif pk == "part-2-industries":
            cls = "toc-ch2"
        else:
            cls = "toc-ch1"
        toc.append(f'<li class="{cls}">'
                   f'<a href="#{slug(f)}">{title}</a></li>')
        body.append(render_article(f))

    template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {series}</title>
<style>
:root {{ --ink:#262320; --muted:#6f6857; --gold:#9a7b2e; --paper:#fbfaf6;
  --line:#e3ddcf; }}
@page {{ size:6in 9in; margin:19mm 16mm 21mm;
  @bottom-center {{ content:counter(page); font-size:8pt;
    color:#9a958a; }} }}
* {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}
body {{ margin:0; background:var(--paper); color:var(--ink);
  font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,
  "Times New Roman",serif; line-height:1.72; font-size:19px;
  -webkit-text-size-adjust:100%; }}
.wrap {{ max-width:42rem; margin:0 auto; padding:0 1.4rem 6rem; }}
p {{ margin:0 0 1.05rem; }}
h1, h2, h3 {{ font-weight:600; line-height:1.25; }}
a {{ color:var(--gold); }}

/* cover */
.cover {{ min-height:96vh; display:flex; flex-direction:column;
  justify-content:center; text-align:center; border-bottom:1px solid var(--line); }}
.cover .series {{ text-transform:uppercase; letter-spacing:.32em;
  font-size:.78rem; color:var(--gold); margin-bottom:2.2rem; }}
.cover h1 {{ font-size:2.7rem; margin:0 0 1.3rem; }}
.cover .sub {{ font-size:1.22rem; color:var(--ink); margin:0 0 .5rem; }}
.cover .tag {{ font-style:italic; color:var(--muted); margin:0 0 2.4rem; }}
.cover .meta {{ text-transform:uppercase; letter-spacing:.2em;
  font-size:.72rem; color:var(--muted); }}

/* contents */
nav.toc {{ padding:3.5rem 0 2rem; border-bottom:1px solid var(--line); }}
nav.toc h2 {{ text-transform:uppercase; letter-spacing:.22em; font-size:.85rem;
  color:var(--gold); margin:0 0 1.6rem; }}
nav.toc ul {{ list-style:none; margin:0; padding:0; }}
nav.toc li {{ margin:.18rem 0; }}
nav.toc a {{ text-decoration:none; color:var(--ink); }}
nav.toc a:hover {{ color:var(--gold); }}
nav.toc .toc-part {{ margin:1.5rem 0 .5rem; font-weight:600;
  text-transform:uppercase; letter-spacing:.08em; font-size:.88rem;
  color:var(--gold); }}
nav.toc .toc-cat {{ margin-top:.7rem; padding-left:1rem; font-weight:600; }}
nav.toc .toc-ch1 {{ padding-left:1rem; }}
nav.toc .toc-ch2 {{ padding-left:2.3rem; font-size:.94rem;
  color:var(--muted); }}
nav.toc .toc-ch2 a {{ color:var(--muted); }}

/* part dividers */
section.part {{ min-height:78vh; display:flex; align-items:center;
  justify-content:center; text-align:center; }}
.part-kicker {{ text-transform:uppercase; letter-spacing:.3em;
  font-size:.8rem; color:var(--gold); margin:0 0 .8rem; }}
section.part h1 {{ font-size:2.4rem; margin:0 0 1rem; }}
.part-blurb {{ font-style:italic; color:var(--muted); max-width:26rem;
  margin:0 auto; }}

/* chapters */
article {{ padding:3.6rem 0 1rem; border-top:1px solid var(--line); }}
article:first-of-type {{ border-top:0; }}
article h1 {{ font-size:1.95rem; margin:.2rem 0 .2rem; }}
article h2 {{ font-size:1.16rem; color:var(--gold); margin:2.3rem 0 .9rem;
  letter-spacing:.01em; }}
article h3 {{ font-size:1.02rem; margin:1.6rem 0 .7rem; }}
.eyebrow {{ text-transform:uppercase; letter-spacing:.17em; font-size:.7rem;
  color:var(--muted); margin:0 0 .6rem; }}
.subtitle {{ font-style:italic; color:var(--muted); font-size:1.08rem;
  margin:0 0 1.4rem; }}
article hr {{ border:0; border-top:1px solid var(--line); margin:1.5rem 0; }}
article ul, article ol {{ margin:0 0 1.05rem; padding-left:1.3rem; }}
article li {{ margin:.3rem 0; }}
blockquote {{ margin:1.2rem 0; padding-left:1.1rem;
  border-left:3px solid var(--gold); color:var(--muted); font-style:italic; }}
table {{ width:100%; border-collapse:collapse; margin:1.3rem 0;
  font-size:.92rem; }}
th, td {{ border:1px solid var(--line); padding:.5rem .6rem;
  text-align:left; vertical-align:top; }}
th {{ background:#f2eee2; }}
.totop {{ display:block; margin-top:2rem; font-size:.76rem;
  text-transform:uppercase; letter-spacing:.16em; text-decoration:none; }}

@media (max-width:480px) {{ body {{ font-size:17.5px; }}
  .cover h1 {{ font-size:2rem; }} }}
@media print {{ body {{ background:#fff; font-size:10.5pt;
    line-height:1.42; }}
  p {{ margin-bottom:.5rem; }}
  article {{ padding-top:2.4rem; }}
  article h2 {{ margin:1.5rem 0 .6rem; }}
  .wrap {{ max-width:none; padding:0; }}
  section.part, article {{ page-break-before:always; }}
  .cover {{ page-break-after:always; min-height:86vh; }}
  nav.toc {{ page-break-after:always; }}
  .totop {{ display:none; }}
  a {{ color:var(--ink); }} }}
</style>
</head>
<body>
<div class="wrap">

<header class="cover">
  <p class="series">{series}</p>
  <h1>{title}</h1>
  <p class="sub">{sub}</p>
  <p class="tag">{tag}</p>
  <p class="meta">Book Two &nbsp;&middot;&nbsp; Working Draft</p>
</header>

<nav class="toc">
  <h2>Contents</h2>
  <ul>
{toc}
  </ul>
</nav>

{body}

<a class="totop" href="#">&uarr; Back to top</a>
</div>
</body>
</html>
"""
    out = template.format(
        title=BOOK_TITLE, series=BOOK_SERIES, sub=BOOK_SUB, tag=BOOK_TAG,
        toc="\n".join("    " + t for t in toc),
        body="\n\n".join(body))
    (MAN / "book.html").write_text(out, encoding="utf-8")


def main():
    files = ordered_files()
    build_combined_md(files)
    build_html(files)
    words = sum(len(f.read_text(encoding="utf-8").split()) for f in files)
    print(f"Built BOOK.md and book.html from {len(files)} files "
          f"(~{words:,} words).")


if __name__ == "__main__":
    main()
