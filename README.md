# Ascendera Group — Website

The public website for **Ascendera Group** (Riyadh, Saudi Arabia) — advisory, assurance technology (Veriso) and experiential training (Kalibra).

**Advise. Verify. Prove.**

## What this is

A static, hand-built website. No framework, no build step, no dependencies — plain HTML, CSS and JavaScript. It can be hosted anywhere that serves static files (GitHub Pages, Netlify, Cloudflare Pages, S3, any web server).

## Structure

```
index.html                  Group hub — Advise. Verify. Prove.
contact.html                Shared contact page

advisory/                   Ascendera Advisory
  index.html                Practice overview, engagement model, HPO & OHTL focus areas, partners
  engagement/               Selected engagement record

veriso/                     Veriso — assurance technology
  index.html                Two products, one standard of proof
  qualify/  ready/  control/  process/  comply/  environment/
                            The six platform products
  barrier/                  Veriso Barrier — live barrier management (product 02)
  doctrine/                 The Veriso doctrine — rules and confidence bands

kalibra/                    Kalibra — the experiential campus
  index.html                Teaser
  register/                 Register interest

leadership/                 Group leadership — principals, partnerships, board advisory

assets/
  css/site.css              One design system; per-brand accent swap (body.brand-*)
  js/site.js                Shared behaviour (reveals, count-ups, nav)
  img/                      Imagery
```

## Design system

One shared stylesheet for the whole group. Each brand page sets a class on `<body>`
(`brand-advisory`, `brand-veriso`, `brand-kalibra`) which swaps the accent colour.
This is what lets Veriso and Kalibra lift out as standalone sites later without a redesign.

## Running locally

Any static server works:

```bash
python3 -m http.server 8080
# open http://localhost:8080
```

## Deployment

GitHub Pages: Settings → Pages → Deploy from branch → `main` / root.
No build command needed.
