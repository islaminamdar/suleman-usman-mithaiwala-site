"""
Wire <picture> + WebP + width/height/decoding attributes into HTML files.
Run with: python _scripts/wire_webp.py
"""
import re, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIMS = json.loads((ROOT / "_scripts" / "img_dims.json").read_text())

def parse_attrs(attr_str: str) -> dict:
    """Pull out attr="value" pairs from inside an <img ...> tag."""
    return dict(re.findall(r'(\w+)="([^"]*)"', attr_str))

def build_picture(src: str, attrs: dict, *, eager: bool = False, fetchpriority: str = None) -> str:
    """Wrap an img in <picture> with a WebP source. Add width/height/decoding."""
    name = src.rsplit("/", 1)[-1]                       # e.g. "mawa-jalebi.jpg"
    stem, _, ext = name.rpartition(".")
    webp_name = f"{stem}.webp"
    webp_path = src.rsplit("/", 1)[0] + "/" + webp_name if "/" in src else webp_name

    w, h = DIMS.get(name, (None, None))

    # Build img attrs
    img_attrs = ['src="' + src + '"']
    if "alt" in attrs:           img_attrs.append(f'alt="{attrs["alt"]}"')
    if "class" in attrs:         img_attrs.append(f'class="{attrs["class"]}"')
    if w and h:
        img_attrs.append(f'width="{w}"')
        img_attrs.append(f'height="{h}"')
    if "loading" in attrs:
        img_attrs.append(f'loading="{attrs["loading"]}"')
    elif not eager:
        img_attrs.append('loading="lazy"')
    img_attrs.append('decoding="async"')
    if fetchpriority:
        img_attrs.append(f'fetchpriority="{fetchpriority}"')

    img_tag = "<img " + " ".join(img_attrs) + " />"
    source = f'<source srcset="{webp_path}" type="image/webp" />'
    return f"<picture>{source}{img_tag}</picture>"

# Match <img ... /> tags
IMG_RE = re.compile(r'<img\s+([^>]*?)/>', re.DOTALL)

def transform_html(html: str) -> str:
    def replace(m):
        attrs = parse_attrs(m.group(1))
        src = attrs.get("src", "")
        # Only wrap images we have webp variants for
        name = src.rsplit("/", 1)[-1] if src else ""
        stem, _, ext = name.rpartition(".")
        webp_name = f"{stem}.webp"
        if webp_name not in DIMS:
            # No webp variant: still add width/height + decoding for CLS
            w, h = DIMS.get(name, (None, None))
            extra = ""
            if w and h and "width" not in attrs:
                extra += f' width="{w}" height="{h}"'
            if "decoding" not in attrs:
                extra += ' decoding="async"'
            if extra:
                return m.group(0).rstrip("/>").rstrip() + extra + " />"
            return m.group(0)

        # Hero photo gets fetchpriority="high"
        is_hero = attrs.get("class", "").find("hero__photo") >= 0
        fp = "high" if is_hero else None
        eager = is_hero or attrs.get("loading") == "eager"
        return build_picture(src, attrs, eager=eager, fetchpriority=fp)

    return IMG_RE.sub(replace, html)

# Run on index.html and 404.html
for filename in ("index.html", "404.html"):
    path = ROOT / filename
    if not path.exists():
        continue
    original = path.read_text(encoding="utf-8")
    new = transform_html(original)
    path.write_text(new, encoding="utf-8")
    diff = new.count("<picture>") - original.count("<picture>")
    print(f"{filename}: +{diff} <picture> wrappings, {new.count('decoding=')} decoding attrs total")
