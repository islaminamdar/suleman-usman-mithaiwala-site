"""
One-shot script: pick selected photos, resize to 1200px wide (max),
compress to JPEG quality 78, save to ../images/ with clean filenames.
"""
from pathlib import Path
from PIL import Image, ImageOps

SRC = Path(r"G:/Other computers/HP LAPTOP/Desktop/Suleman Usman Mithaiwala Restaurant/S.M/S.M")
DST = Path(__file__).resolve().parent.parent / "images"
DST.mkdir(parents=True, exist_ok=True)

# (output filename without extension, source-filename substring to match)
PICKS = [
    # Sweets / Mithai
    ("mawa-jalebi",        "Mawa Jalebi"),
    ("malpua-rabdi",       "Malpua With Rabdi"),
    ("special-pista-aflatoon", "Special Pista Aflatoon"),
    ("special-badam-aflatoon", "Special badam aflatoon"),
    ("dryfruit-aflatoon",  "Dry Fruits Aflatoon"),
    ("kaju-aflatoon",      "Kaju aflatoon"),
    ("normal-aflatoon",    "Normal Aflatoon"),
    ("mix-peda",           "Mix Peda"),
    ("pink-barfi",         "Pink Barfi"),
    ("mawa-khaja",         "Mawa Khaja"),
    ("malai-rabdi",        "Malai Rabdi"),
    # Halwa
    ("dryfruit-halwa",     "Dryfruit Halwa"),
    ("akhrot-halwa",       "Akhrot Halwa"),
    ("anjeer-halwa",       "Anjeer Halwa"),
    ("gajar-halwa",        "Gajar Halwa"),
    ("dudhi-halwa",        "Dudhi Halwa"),
    # Bakery / Nankhatai
    ("nankhatai-rawa",     "Nankhati Rawa"),
    ("nankhatai-dryfruit", "Nankhati dry fruit"),
    ("maska-khari",        "Maska Khari"),
    ("maska-pav",          "Maska Pav Kadak"),
    # Restaurant — Mughlai / Tikka / Kabab
    ("chicken-tikka",      "Chicken Tikka (8 Pieces)"),
    ("chicken-malai-tikka","Chicken Malai Tikka"),
    ("chicken-seekh-kabab","Chicken Seekh Kabab"),
    ("mutton-seekh-kabab", "Mutton Seekh Kabab"),
    ("paneer-tikka",       "Paneer Tikka"),
    # Curries
    ("chicken-korma",      "Chicken Korma"),
    ("chicken-curry",      "Chicken Curry"),
    ("chicken-kali-mirch", "Chicken Kali Mirch"),
    ("karahi-paneer",      "Karahi Paneer"),
    ("paneer-methi-malai", "Paneer Methi Malai"),
    # Rice / Khichra
    ("mutton-khichra",     "MUTTON KHICHRA"),
    ("dalcha-chawal",      "DALCHA CHAWAL"),
    ("chicken-fried-rice", "CHICKEN FRIED RICE"),
    # Tawa / Specials
    ("bheja-fry",          "BHEJA FRY"),
    ("tawa-kaleji",        "TAWA KALEJI"),
    # Pav / Snacks
    ("keema-pav",          "Keema Pav"),
    ("double-kabab-pav",   "Double Kabab Pav"),
    ("jeera-butter",       "Jeera Butter"),
]

MAX_W = 1200
QUALITY = 78

def find_source(needle: str) -> Path | None:
    needle_low = needle.lower()
    for p in SRC.iterdir():
        if needle_low in p.name.lower():
            return p
    return None

processed, skipped = 0, []
for out_name, needle in PICKS:
    src = find_source(needle)
    if not src:
        skipped.append(needle)
        continue
    out = DST / f"{out_name}.jpg"
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode != "RGB":
            im = im.convert("RGB")
        if im.width > MAX_W:
            ratio = MAX_W / im.width
            im = im.resize((MAX_W, int(im.height * ratio)), Image.LANCZOS)
        im.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    print(f"  {out.name:<32}  {out.stat().st_size//1024} KB")
    processed += 1

print(f"\nDone: {processed} processed, {len(skipped)} skipped.")
if skipped:
    print("Skipped:", skipped)
