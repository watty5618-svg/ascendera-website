# Ascendera Group website

Static HTML site published from the repository root on GitHub Pages. The configured custom domain is `www.ascenderagroup.sa`.

English pages are at the root and Arabic equivalents under `ar/`. Shared styles and behaviour live in `assets/css` and `assets/js`. Preserve reciprocal language links when adding or moving pages.

## Veriso films

The libraries are `veriso/videos/index.html` and `ar/veriso/videos/index.html`. Each film has a dedicated page under the corresponding `veriso/watch/` directory. The catalogue at `assets/video/catalogue.json` records each edition's paths, title, description and running time.

The November 2026 editions include Veriso Platform, Process and Barrier, and Barrier Report. Each language has its own MP4, poster, WebVTT captions and transcript. Keep captions and transcript paired with the exact recording. Preserve `preload="none"`, native controls, and no autoplay on narrated films. The MP4 files already place their metadata first for streaming.

The former Comply URL is retained, with the current Social & Welfare module name displayed. Internal links and existing bookmarks continue to work.

## Advisory & Delivery practice

The HSSE & Critical Risk pages are `advisory/hsse/index.html` and `ar/advisory/hsse/index.html`. They present Build, Run and Prove, fourteen services in four groups, a dedicated managed-function section, delivery steps, the independence boundary and relevant Veriso films. Keep both editions aligned when changing scope or deliverables.

Group and Advisory pages introduce the practice, and the Veriso overview, Barrier and Process pages link back to it. Existing Advisory URLs are preserved. Practice-specific layout rules are in `assets/css/practice.css`.

Service enquiries use allowlisted `service=hsse` or `service=hsse-1` through `hsse-14` parameters. The contact form preselects the matching service, records its readable name in `service_detail`, and retains the selection when switching language. No message is sent until the visitor submits the existing form.

The practice copy is adapted from the owner's 8 November 2026 draft. Before public release, resolve that draft's managed-service activity-scope question and outstanding certification evidence and product-naming decisions. The new pages make no certification claim; the Advisory hub's unsupported certification wording has been removed. Certification statements elsewhere in the older site have not been reconciled by this change.

## Preview and checks

```text
python -m http.server 4191 --bind 127.0.0.1
python scripts/check-site.py
node --check assets/js/site.js
git diff --check
```

The checker validates local links and anchors, language metadata, sitemap coverage, paired media, caption timing, MP4 duration and fast-start ordering. Also review desktop and phone layouts, Arabic direction and shaping, keyboard navigation, reduced motion, and actual browser playback before release.

The video metadata intentionally omits a first-publication date until the new watch pages are published. Set each VideoObject's `uploadDate` to the actual publication timestamp during release.
