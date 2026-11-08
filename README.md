# Ascendera Group website

Static HTML site published from the repository root on GitHub Pages. The configured custom domain is `www.ascenderagroup.sa`.

English pages are at the root and Arabic equivalents under `ar/`. Shared styles and behaviour live in `assets/css` and `assets/js`. Preserve reciprocal language links when adding or moving pages.

## Veriso films

The libraries are `veriso/videos/index.html` and `ar/veriso/videos/index.html`. Each film has a dedicated page under the corresponding `veriso/watch/` directory. The catalogue at `assets/video/catalogue.json` records each edition's paths, title, description and running time.

The November 2026 editions include Veriso Platform, Process and Barrier, and Barrier Report. Each language has its own MP4, poster, WebVTT captions and transcript. Keep captions and transcript paired with the exact recording. Preserve `preload="none"`, native controls, and no autoplay on narrated films. The MP4 files already place their metadata first for streaming.

The English and Arabic Group homepages feature the short Platform-in-practice scenario (2:26 and approximately 2:28 respectively), with a secondary link to the full Platform explanation. The longer explainers remain on the relevant product and watch pages.

The library also includes three practical-use scenarios: Platform, Barrier and Barrier Report, each in English and Arabic. Scenario entries use `kind: scenario` and link to their corresponding explainer through `explainer`. They are illustrative applications, not customer case studies. The six new editions and their paired poster, VTT and transcript files were checked against the completed scenario archive and movie hashes in its production audit. The source records describe them as a completed working-session candidate for release. The English HSSE practice film is now featured directly below the practice-page hero, with links from Advisory and the video library. Its media record is `assets/video/practice.json`. It uses native controls, English captions and a transcript; the Arabic page explicitly labels the film and transcript as English because no Arabic MP4 has been exported. The rendered version precedes the separate hazardous-energy wording update; replace the movie, captions and transcript together when that revised edition is completed.

The former Comply URL is retained, with the current Social & Welfare module name displayed. Internal links and existing bookmarks continue to work.

## Advisory & Delivery practice

The HSSE & Critical Risk pages are `advisory/hsse/index.html` and `ar/advisory/hsse/index.html`. They present Build, Run and Prove, fourteen services in four groups, a dedicated managed-function section, delivery steps, the independence boundary and relevant Veriso films. Keep both editions aligned when changing scope or deliverables.

Group and Advisory pages introduce the practice, and the Veriso overview, Barrier and Process pages link back to it. Existing Advisory URLs are preserved. Practice-specific layout rules are in `assets/css/practice.css`.

The practice also connects high-performance leadership and teams, critical thinking and decision-making, and ultra-high-risk work. Specialist pages describe delivered activities and tangible outputs; existing `/advisory/hpo/` and `/advisory/ohtl/` addresses remain unchanged. These are service descriptions, not additional case-study claims.

Service enquiries use allowlisted `service=hsse` or `service=hsse-1` through `hsse-14`, plus `hpo`, `critical-thinking` and `ultra-high-risk` parameters. The contact form preselects the matching service, records its readable name in `service_detail`, and retains the selection when switching language. No message is sent until the visitor submits the existing form.

The practice copy is adapted from the owner's 8 November 2026 draft. Before public release, resolve that draft's managed-service activity-scope question and outstanding certification evidence and product-naming decisions. The new pages make no certification claim; the Advisory hub's unsupported certification wording has been removed. Certification statements elsewhere in the older site have not been reconciled by this change.

## Public delivery summary

The English and Arabic engagement pages describe major infrastructure projects across the Kingdom and Central Asia. Advisory and HSSE practice pages link to the on-page summary. There is no downloadable delivery document on the website.

Keep client identity, specific countries within Central Asia, asset technologies, project imagery, exact counts, timeframes and financial figures out of this delivery story, including metadata and downloads. Describe the work and handover materials without inferring a complete Veriso deployment or quantified performance results. Further client or project disclosure requires client written consent; an NDA alone does not authorise it. Never add the confidential source document to this repository.

## Preview and checks

```text
python -m http.server 4191 --bind 127.0.0.1
python scripts/check-site.py
node --check assets/js/site.js
git diff --check
```

The checker validates local links and anchors, language metadata, sitemap coverage, paired media, caption timing, MP4 duration and fast-start ordering. Also review desktop and phone layouts, Arabic direction and shaping, keyboard navigation, reduced motion, and actual browser playback before release.

The video metadata intentionally omits a first-publication date until the new watch pages are published. Set each VideoObject's `uploadDate` to the actual publication timestamp during release.
