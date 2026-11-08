# Ascendera Group website

Static HTML site published from the repository root on GitHub Pages. The configured custom domain is `www.ascenderagroup.sa`.

English pages are at the root and Arabic equivalents under `ar/`. Shared styles and behaviour live in `assets/css` and `assets/js`. Preserve reciprocal language links when adding or moving pages.

## Veriso films

The libraries are `veriso/videos/index.html` and `ar/veriso/videos/index.html`. Each film has a dedicated page under the corresponding `veriso/watch/` directory. The catalogue at `assets/video/catalogue.json` records each edition's paths, title, description and running time.

The November 2026 editions include Assurance Platform, Process and Barrier, and Barrier Report. Each language has its own MP4, poster, WebVTT captions and transcript. Keep captions and transcript paired with the exact recording. Preserve `preload="none"`, native controls, and no autoplay on narrated films. The MP4 files already place their metadata first for streaming.

The former Comply URL is retained, with the current Social & Welfare module name displayed. Internal links and existing bookmarks continue to work.

## Preview and checks

```text
python -m http.server 4191 --bind 127.0.0.1
python scripts/check-site.py
node --check assets/js/site.js
git diff --check
```

The checker validates local links and anchors, language metadata, sitemap coverage, paired media, caption timing, MP4 duration and fast-start ordering. Also review desktop and phone layouts, Arabic direction and shaping, keyboard navigation, reduced motion, and actual browser playback before release.

The video metadata intentionally omits a first-publication date until the new watch pages are published. Set each VideoObject's `uploadDate` to the actual publication timestamp during release.
