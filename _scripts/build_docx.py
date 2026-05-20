#!/usr/bin/env python3
"""Assemble the manuscript into a single 6x9 DOCX (manuscript/book.docx).

Convert to PDF with LibreOffice:
  soffice --headless --convert-to pdf --outdir manuscript manuscript/book.docx
"""

import pathlib
import re

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAN = ROOT / "manuscript"

CENTER = WD_ALIGN_PARAGRAPH.CENTER
LEFT = WD_ALIGN_PARAGRAPH.LEFT
JUSTIFY = WD_ALIGN_PARAGRAPH.JUSTIFY

INK = RGBColor(0x26, 0x23, 0x20)
GOLD = RGBColor(0x8A, 0x6D, 0x28)
MUTED = RGBColor(0x66, 0x60, 0x52)
SERIF = "Liberation Serif"

BOOK_TITLE = "How to Start a Business in Dubai"
BOOK_SERIES = "THE DUBAI SYNDICATE WAY"
BOOK_SUB = "The Practical Field Guide to 35 Industries"
BOOK_TAG = "From Restaurant to Real Estate, Salon to SaaS"

PARTS = [
    ("part-1-foundations", "PART ONE", "Foundations",
     "What every Dubai business shares — the city, the jurisdiction, "
     "the licence, the money, and the mindset."),
    ("part-2-industries", "PART TWO", "The Field Guide",
     "Thirty-five industries, eight categories, one template — "
     "six pages each, built to be compared."),
    ("part-3-resources", "PART THREE", "Resources",
     "Directories, checklists, and tools to turn a decision "
     "into an application."),
]

INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*]+?\*)")
SUBTITLE = re.compile(r"^\*[^*].*[^*]\*$")
LISTITEM = re.compile(r"^([-*+]\s|\d+\.\s)")

doc = Document()


def ordered_files():
    files = [p for p in MAN.rglob("*.md")
             if p.name not in ("OUTLINE.md", "BOOK.md")]
    return sorted(files, key=lambda p: str(p).lower())


def part_key(path):
    for key, *_ in PARTS:
        if key in str(path):
            return key
    return ""


def is_special(s):
    return (not s or s.startswith("#") or s.startswith("|")
            or s.startswith(">") or re.fullmatch(r"[-*_]{3,}", s)
            or LISTITEM.match(s)
            or (SUBTITLE.match(s) and not s.startswith("**")))


def style_run(run, size=10.5, bold=False, italic=False, color=INK):
    run.font.name = SERIF
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color


def add_runs(paragraph, text, size=10.5, color=INK):
    for tok in INLINE.split(text):
        if not tok:
            continue
        bold = italic = False
        if tok.startswith("**") and tok.endswith("**"):
            tok, bold = tok[2:-2], True
        elif tok.startswith("*") and tok.endswith("*"):
            tok, italic = tok[1:-1], True
        style_run(paragraph.add_run(tok), size=size, bold=bold,
                  italic=italic, color=color)


def para(text="", size=10.5, color=INK, align=None, italic_all=False,
         bold_all=False, space_before=0, space_after=6, indent=0.0):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.alignment = align if align is not None else JUSTIFY
    if indent:
        pf.left_indent = Inches(indent)
    if text:
        if italic_all or bold_all:
            style_run(p.add_run(text), size=size, color=color,
                      italic=italic_all, bold=bold_all)
        else:
            add_runs(p, text, size=size, color=color)
    return p


def heading(text, level):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = LEFT
    if level == 1:
        pf.page_break_before = True
        pf.space_before = Pt(6)
        pf.space_after = Pt(15)
        style_run(p.add_run(text), size=19, bold=True, color=INK)
    elif level == 2:
        pf.space_before = Pt(16)
        pf.space_after = Pt(5)
        style_run(p.add_run(text), size=12.5, bold=True, color=GOLD)
    else:
        pf.space_before = Pt(11)
        pf.space_after = Pt(4)
        style_run(p.add_run(text), size=11, bold=True, color=INK)
    return p


def render_table(block):
    def cells(row):
        return [c.strip() for c in row.strip().strip("|").split("|")]
    header = cells(block[0])
    data = [cells(r) for r in block[2:]]
    ncol = len(header)
    table = doc.add_table(rows=1 + len(data), cols=ncol)
    table.style = "Table Grid"
    for j, text in enumerate(header):
        cell = table.rows[0].cells[j]
        cell.paragraphs[0].text = ""
        cell.paragraphs[0].alignment = LEFT
        add_runs(cell.paragraphs[0], text, size=9)
        for run in cell.paragraphs[0].runs:
            run.bold = True
    for ri, row in enumerate(data):
        for j in range(ncol):
            cell = table.rows[ri + 1].cells[j]
            cell.paragraphs[0].text = ""
            cell.paragraphs[0].alignment = LEFT
            add_runs(cell.paragraphs[0], row[j] if j < len(row) else "",
                     size=9)
    para(space_after=4)


def render_file(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    i, n = 0, len(lines)
    first = True
    while i < n:
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if first:
            para(s, size=8, color=MUTED, align=LEFT, space_after=2)
            first = False
            i += 1
            continue
        if s.startswith("### "):
            heading(s[4:].strip(), 3)
            i += 1
            continue
        if s.startswith("## "):
            heading(s[3:].strip(), 2)
            i += 1
            continue
        if s.startswith("# "):
            heading(s[2:].strip(), 1)
            i += 1
            continue
        if re.fullmatch(r"[-*_]{3,}", s):
            i += 1
            continue
        if SUBTITLE.match(s) and not s.startswith("**"):
            para(s[1:-1], size=11.5, color=MUTED, align=LEFT,
                 italic_all=True, space_after=12)
            i += 1
            continue
        if s.startswith("|"):
            block = []
            while i < n and lines[i].strip().startswith("|"):
                block.append(lines[i].strip())
                i += 1
            if len(block) >= 2:
                render_table(block)
            continue
        m = re.match(r"^[-*+]\s+(.*)$", s)
        if m:
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(2)
            add_runs(p, m.group(1))
            i += 1
            continue
        m = re.match(r"^\d+\.\s+(.*)$", s)
        if m:
            p = doc.add_paragraph(style="List Number")
            p.paragraph_format.space_after = Pt(2)
            add_runs(p, m.group(1))
            i += 1
            continue
        if s.startswith(">"):
            para(re.sub(r"^>\s?", "", s), color=MUTED, align=LEFT,
                 italic_all=True, indent=0.3)
            i += 1
            continue
        buf = [s]
        i += 1
        while i < n and not is_special(lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        para(" ".join(buf))


def render_title_page():
    for _ in range(3):
        para(space_after=0)
    para(BOOK_SERIES, size=11.5, color=GOLD, align=CENTER, space_after=34)
    p = doc.add_paragraph()
    p.paragraph_format.alignment = CENTER
    p.paragraph_format.space_after = Pt(16)
    style_run(p.add_run(BOOK_TITLE), size=29, bold=True, color=INK)
    para(BOOK_SUB, size=14, color=INK, align=CENTER, space_after=6)
    para(BOOK_TAG, size=11.5, color=MUTED, align=CENTER, italic_all=True,
         space_after=44)
    para("BOOK TWO  ·  WORKING DRAFT", size=9, color=MUTED,
         align=CENTER)


def render_part_divider(key):
    _, label, name, blurb = next(p for p in PARTS if p[0] == key)
    doc.add_page_break()
    for _ in range(6):
        para(space_after=0)
    para(label, size=12.5, color=GOLD, align=CENTER, space_after=12)
    p = doc.add_paragraph()
    p.paragraph_format.alignment = CENTER
    p.paragraph_format.space_after = Pt(14)
    style_run(p.add_run(name), size=24, bold=True, color=INK)
    para(blurb, size=11.5, color=MUTED, align=CENTER, italic_all=True)


def main():
    section = doc.sections[0]
    section.page_width = Inches(6)
    section.page_height = Inches(9)
    section.left_margin = section.right_margin = Inches(0.72)
    section.top_margin = section.bottom_margin = Inches(0.78)

    normal = doc.styles["Normal"]
    normal.font.name = SERIF
    normal.font.size = Pt(10.5)
    pf = normal.paragraph_format
    pf.line_spacing = 1.18
    pf.space_after = Pt(6)

    render_title_page()
    current = None
    files = ordered_files()
    for f in files:
        key = part_key(f)
        if key != current:
            current = key
            render_part_divider(key)
        render_file(f)

    doc.save(str(MAN / "book.docx"))
    print(f"Built manuscript/book.docx from {len(files)} files.")


if __name__ == "__main__":
    main()
