#!/usr/bin/env python3
"""Build the full print-wrap cover (manuscript/cover.pdf) for Book Two.

A single flat sheet — back cover, spine, front cover — in the series
identity: deep purple, Carlito type, magenta rules. Sized for a 6x9 in
paperback with full bleed.

Spine width assumes Amazon KDP black-and-white interior on white paper
(0.002252 in per page). Change PAGE_COUNT / PAGE_THICKNESS if the
interior length or the printer's stock differs.

Usage:  python3 _scripts/build_cover.py
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAN = ROOT / "manuscript"

# ---- trim and bleed ------------------------------------------------------
TRIM_W = 6.0          # in
TRIM_H = 9.0          # in
BLEED = 0.125         # in, each outer edge

PAGE_COUNT = 379      # interior pages — keep in sync with book.pdf
PAGE_THICKNESS = 0.002252   # KDP, b/w interior on white paper
SPINE = round(PAGE_COUNT * PAGE_THICKNESS, 4)

COVER_W = round(2 * TRIM_W + SPINE + 2 * BLEED, 4)
COVER_H = round(TRIM_H + 2 * BLEED, 4)
BACK_W = round(TRIM_W + BLEED, 4)

BOOK_TITLE_LINES = ["HOW TO START", "A BUSINESS", "IN DUBAI"]
BOOK_TITLE_FLAT = "How to Start a Business in Dubai"
BOOK_SERIES = "The Dubai Syndicate Way"
BOOK_SUB = "The Practical Field Guide to 35 Industries"
BOOK_TAG = "From Restaurant to Real Estate, Salon to SaaS"
BOOK_AUTHOR = "Islam Inamdar"
BOOK_PUBLISHER = "Dubai Syndicate"

BACK_HOOK = "Dubai rewards the founder who arrives prepared."
BACK_BODY = [
    "Most business books sell the dream. This one hands you the map. "
    "<em>How to Start a Business in Dubai</em> is a working field guide "
    "to thirty-five industries — the licences, the capital, the "
    "landlords, the regulators, and the honest numbers behind each one.",
    "Part One covers what every Dubai business shares: the city, the "
    "jurisdiction decision, licensing and visas, money, and the operating "
    "mindset. Part Two profiles thirty-five industries — from restaurants "
    "and salons to e-commerce, real estate, and software — each on the "
    "same template, built to be compared. Part Three turns a decision "
    "into an application: a 90-day launch plan, a comparison of free zone "
    "and mainland, a cost ready-reckoner, and a directory of the "
    "authorities that matter.",
]
BACK_BULLETS = [
    "Thirty-five industries on one comparable template",
    "Real capital ranges, licences, and launch timelines",
    "A 90-day launch plan and a cost ready-reckoner",
]


CSS = f"""
@page {{ size: {COVER_W}in {COVER_H}in; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{ font-family: Carlito, Calibri, sans-serif; hyphens: manual; }}

.wrap {{
  position: relative;
  width: {COVER_W}in; height: {COVER_H}in;
  background: #6b2c7e; overflow: hidden;
}}

.back  {{ position: absolute; top: 0; left: 0;
          width: {BACK_W}in; height: {COVER_H}in; }}
.spine {{ position: absolute; top: 0; left: {BACK_W}in;
          width: {SPINE}in; height: {COVER_H}in; }}
.front {{ position: absolute; top: 0; right: 0;
          width: {BACK_W}in; height: {COVER_H}in; }}

/* ---- front cover ---------------------------------------------------- */
.front .frame {{
  position: absolute;
  top: 0.6in; bottom: 0.6in; left: 0.52in; right: 0.66in;
  border: 0.9pt solid rgba(255,255,255,0.34);
}}
.f-el {{ position: absolute; left: 0.82in; right: 0.95in;
         text-align: center; margin: 0; }}
.f-head {{ top: 1.04in; }}
.f-series {{
  text-transform: uppercase; letter-spacing: 0.2em;
  font-size: 10pt; color: #e7d9ec; margin: 0; white-space: nowrap;
}}
.f-booktwo {{
  text-transform: uppercase; letter-spacing: 0.34em;
  font-size: 8pt; color: #dd97c4; margin: 0.17in 0 0; white-space: nowrap;
}}
.f-center {{ top: 2.62in; }}
.f-rule {{ width: 1.4in; height: 1.4pt; background: #b83b7e;
           border: 0; margin: 0 auto; }}
.f-title {{
  text-transform: uppercase; font-weight: 700;
  font-size: 37pt; line-height: 1.13; color: #ffffff;
  margin: 0.26in 0; white-space: nowrap;
}}
.f-sub {{ font-size: 13pt; color: #ffffff; margin: 0.32in 0 0; }}
.f-tag {{ font-style: italic; font-size: 10.5pt;
          color: #e7d9ec; margin: 0.11in 0 0; }}
.f-author {{
  top: 7.62in;
  text-transform: uppercase; letter-spacing: 0.2em;
  font-weight: 700; font-size: 13.5pt; color: #ffffff;
}}

/* ---- spine ---------------------------------------------------------- */
.spine-text {{
  position: absolute; top: 50%; left: 50%;
  width: {COVER_H}in; height: {SPINE}in;
  transform: translate(-50%, -50%) rotate(90deg);
  display: flex; align-items: center; justify-content: center;
  white-space: nowrap;
}}
.s-title {{
  text-transform: uppercase; font-weight: 700;
  font-size: 13pt; color: #ffffff; letter-spacing: 0.02em;
}}
.s-dot {{ color: #b83b7e; margin: 0 0.2in; font-size: 12pt; }}
.s-author {{
  text-transform: uppercase; letter-spacing: 0.13em;
  font-size: 10.5pt; color: #e7d9ec;
}}

/* ---- back cover ----------------------------------------------------- */
.back .pad {{
  position: absolute;
  top: {BLEED + 0.62}in; left: {BLEED + 0.5}in; right: 0.55in;
}}
.b-hook {{
  font-weight: 700; font-size: 16pt; line-height: 1.32;
  color: #ffffff; margin: 0 0 0.26in;
}}
.b-body {{
  font-size: 10.6pt; line-height: 1.6; color: #ece1f0;
  margin: 0 0 0.15in; text-align: justify; hyphens: auto;
}}
.b-body em {{ font-style: italic; }}
.b-list {{ list-style: none; margin: 0.26in 0 0; padding: 0; }}
.b-list li {{
  font-size: 10.8pt; color: #ffffff; margin: 0.1in 0;
  padding-left: 0.34in; position: relative;
}}
.b-list li::before {{
  content: ""; position: absolute; left: 0; top: 0.05in;
  width: 0.12in; height: 0.12in; background: #b83b7e;
}}
.b-foot {{
  position: absolute; right: 0.55in; bottom: {BLEED + 0.52}in;
  text-align: right;
}}
.b-series {{
  text-transform: uppercase; letter-spacing: 0.13em;
  font-size: 8.5pt; color: #e7d9ec; margin: 0 0 0.05in;
}}
.b-pub {{ font-weight: 700; font-size: 11pt; color: #ffffff; margin: 0; }}
.barcode {{
  position: absolute; left: {BLEED + 0.32}in; bottom: {BLEED + 0.32}in;
  width: 2in; height: 1.2in; background: #ffffff;
}}
.barcode span {{
  position: absolute; left: 0; right: 0; bottom: 0.12in;
  text-align: center; font-size: 6.5pt; color: #a09aa3;
  letter-spacing: 0.08em;
}}
"""


def build():
    title_html = "<br>".join(BOOK_TITLE_LINES)
    body_html = "".join(f'<p class="b-body">{p}</p>' for p in BACK_BODY)
    bullets_html = "".join(f"<li>{b}</li>" for b in BACK_BULLETS)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{BOOK_TITLE_FLAT} — cover</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">

  <section class="back">
    <div class="pad">
      <p class="b-hook">{BACK_HOOK}</p>
      {body_html}
      <ul class="b-list">{bullets_html}</ul>
    </div>
    <div class="b-foot">
      <p class="b-series">Book Two &middot; {BOOK_SERIES}</p>
      <p class="b-pub">Published by {BOOK_PUBLISHER}</p>
    </div>
    <div class="barcode"><span>ISBN / BARCODE AREA</span></div>
  </section>

  <div class="spine">
    <div class="spine-text">
      <span class="s-title">{BOOK_TITLE_FLAT}</span>
      <span class="s-dot">&middot;</span>
      <span class="s-author">{BOOK_AUTHOR}</span>
    </div>
  </div>

  <section class="front">
    <div class="frame"></div>
    <div class="f-el f-head">
      <p class="f-series">{BOOK_SERIES}</p>
      <p class="f-booktwo">Book Two</p>
    </div>
    <div class="f-el f-center">
      <hr class="f-rule">
      <h1 class="f-title">{title_html}</h1>
      <hr class="f-rule">
      <p class="f-sub">{BOOK_SUB}</p>
      <p class="f-tag">{BOOK_TAG}</p>
    </div>
    <p class="f-el f-author">{BOOK_AUTHOR}</p>
  </section>

</div>
</body>
</html>
"""
    (MAN / "cover.html").write_text(html, encoding="utf-8")

    try:
        from weasyprint import HTML
    except ImportError:
        print("  (WeasyPrint not installed - wrote cover.html only)")
        return
    HTML(string=html).write_pdf(str(MAN / "cover.pdf"))
    print(f"Built manuscript/cover.pdf  "
          f"({COVER_W} x {COVER_H} in, spine {SPINE} in / "
          f"{PAGE_COUNT} pages)")


if __name__ == "__main__":
    build()
