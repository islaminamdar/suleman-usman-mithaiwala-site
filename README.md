# Suleman Usman Mithaiwala — Website

A heritage-themed marketing site for Suleman Usman Mithaiwala, Mumbai's iconic mithai house since 1936.

## Stack
Plain HTML, CSS, and a small JS file. No build step. Drop-in deploy.

## Structure
- `index.html` — single-page site (Hero, Heritage, Signature, Catalogue, Press, Locations, Contact)
- `styles.css` — design system (heritage palette, responsive, reveal-on-scroll)
- `script.js` — sticky nav, mobile menu, tabs, scroll reveal

## Run locally
Open `index.html` directly in a browser, or:

```
python -m http.server 8000
```

then visit `http://localhost:8000`.

## Deploy on GitHub Pages
1. Push this folder to a GitHub repo.
2. Settings → Pages → Deploy from branch → `main` / root.
3. Site will be live at `https://<username>.github.io/<repo>/`.

## Notes
- All product imagery is currently CSS-rendered placeholders so the site loads instantly with zero external image dependencies. Swap in real photography later by replacing `.card__image--*` background rules in `styles.css`.
- Phone, email and addresses pulled from public listings (official site, Justdial, Zomato). Verify before going live.
