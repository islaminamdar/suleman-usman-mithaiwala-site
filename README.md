# AG Suleman Usman Mithaiwala — Dubai Website

Premium, single-page marketing site for **AG Suleman Usman Mithaiwala** — a 100-year-old Bombay sweets and Mughlai restaurant brand, now expanding across the GCC.

## Stack
Plain HTML, CSS, vanilla JS. No build step. ~5 MB total page weight including 38 product photos.

## Sections
- Sticky promo bar — Panipuri Champion's Cup (ad-campaign landing zone)
- Hero ("A Legacy of Sweetness Since 1926")
- **Panipuri Champion's Cup** — AED 10 entry, AED 1,000 prize, daily 4 PM at UAE branches. Full rules, 5-step entry flow, Instagram tag-and-collab requirement.
- Legacy story + 3-generation timeline
- Global Presence (UAE / KSA / India)
- Filterable menu (38 dishes across 8 categories)
- Why Choose Us
- Leadership (GCC + India)
- Technology & modern approach (Internext)
- Locations (Bur Dubai, Sharjah, Business Bay, Riyadh, Madinah, Mumbai)
- Vision & Mission
- Investor / Partnership form (auto-routes submission to WhatsApp)
- Contact + Final CTA
- Floating WhatsApp button (+971 55 713 3786)

## Files
- `index.html` — markup, OG tags, JSON-LD structured data
- `styles.css` — design system (black + gold + magenta palette)
- `script.js` — sticky nav, mobile menu, filter chips, partner form, reveal-on-scroll
- `images/` — 38 product photos (compressed from originals at 1200px / quality 78)
- `_scripts/compress_images.py` — one-shot script that produced the `images/` set from source photos. Re-run only if source photos change.

## Run locally
Open `index.html` in any browser, or:

```bash
python -m http.server 8000
```

then visit `http://localhost:8000`.

## Deploy
Already wired up to GitHub Pages on the `main` branch.

Live URL: **https://islaminamdar.github.io/suleman-usman-mithaiwala-site/**

Push to `main` → Pages rebuilds automatically (1–2 minutes).

## Partner-form behaviour
The "Become a Partner" form does NOT email anywhere. On submit it opens WhatsApp with a pre-composed message addressed to **+971 55 713 3786**. The user can then send it. Zero backend, zero spam.

If a real form-handler is needed later, swap the JS in `script.js` for a Formspree / Web3Forms / Google Forms POST.

## Image credits
All product photos are by Kailash, originally shot for AG Suleman Usman Mithaiwala. Compressed copies live in `images/`. The Bur Dubai storefront photo (`images/storefront.jpg`) was provided by the brand.

## Brand logo
The site references `images/logo.png` for the nav brand mark, favicon and Apple touch icon. Drop your final logo PNG (square, transparent background recommended) at that exact path and re-deploy. Until then, the nav falls back gracefully to a pink "SUM" monogram.

## Google AdSense
- `ads.txt` at site root carries the publisher line (`pub-7910994933427279`).
- AdSense auto-ads script is loaded in `<head>` of `index.html`.
- Submit the live Pages URL to AdSense for approval — the snippet alone does not start serving ads.
