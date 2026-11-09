# Ascendera Group website

Static HTML site published from the repository root on GitHub Pages. The configured custom domain is `www.ascenderagroup.sa`.

English pages are at the root, Arabic equivalents under `ar/`, and Simplified Chinese equivalents under `zh/`. Shared styles and behaviour live in `assets/css` and `assets/js`. Preserve reciprocal language links and all four hreflang entries when adding or moving pages. Chinese pages use `lang="zh-Hans"`; their typography adjustments are in `assets/css/zh.css`.

## Veriso films

The libraries are `veriso/videos/index.html`, `ar/veriso/videos/index.html` and `zh/veriso/videos/index.html`. Each film has a dedicated page under the corresponding `veriso/watch/` directory. The catalogue at `assets/video/catalogue.json` records each edition's paths, title, description and running time.

The Chinese edition adds Mandarin AI narration, Simplified Chinese screen text, timed captions and matching full transcripts for all nine website films. The recordings use the licensed native Mandarin James Gao voice and Eleven v4. Their visual treatment is a Chinese presentation edition using existing brand marks and imagery; it does not replace the English and Arabic motion editions. Use each Chinese film's actual duration when updating cards and structured metadata. The separate Mandarin Group introduction is in the owner's film delivery collection, alongside the nine website films.

The November 2026 editions include Veriso Platform, Process and Barrier, and Barrier Report. Each language has its own MP4, poster, WebVTT captions and transcript. Keep captions and transcript paired with the exact recording. Preserve `preload="none"`, native controls, and no autoplay on narrated films. The MP4 files already place their metadata first for streaming.

The English and Arabic Group homepages feature the short Platform-in-practice scenario (2:26 and approximately 2:28 respectively), with a secondary link to the full Platform explanation. The longer explainers remain on the relevant product and watch pages. Film cards use the existing site photography with a readable HTML title, duration and play control; recordings, captions and player posters remain paired with their source editions. Keep one featured film per main page and place further films in relevant product sections or the library. The site’s brand styles, colours, fonts and marks are unchanged by this presentation pass.

The library also includes three practical-use scenarios: Platform, Barrier and Barrier Report, each in English and Arabic. Scenario entries use `kind: scenario` and link to their corresponding explainer through `explainer`. They are illustrative applications, not customer case studies. The six new editions and their paired poster, VTT and transcript files were checked against the completed scenario archive and movie hashes in its production audit. The source records describe them as a completed working-session candidate for release. The practice collection now has three films in English and Arabic: updated HSSE and critical risk (including energy isolation and stored-energy control), High Performance with Dr Dan Cooper, and Transmission with Lee Stevenson. Each plays on its relevant Advisory practice page and is discoverable through the film library. The practice catalogue is `assets/video/practice.json`, an array with per-language editions and their page routes. Videos use native controls, no autoplay, matching captions and a collapsible transcript. The latest Transmission editions use NVQ without a level and include experience in the Kingdom and overseas emerging markets. Movies are verified against production QA hashes; posters, captions and transcripts are imported together. Versioned media paths prevent previously cached videos being paired with updated captions.

The former Comply URL is retained, with the current Social & Welfare module name displayed. Internal links and existing bookmarks continue to work.

## Advisory & Delivery practice

The HSSE & Critical Risk pages are `advisory/hsse/index.html` and `ar/advisory/hsse/index.html`. They present Build, Run and Prove, fourteen services in four groups, a dedicated managed-function section, delivery steps, the independence boundary and relevant Veriso films. Keep both editions aligned when changing scope or deliverables.

Group and Advisory pages introduce the practice, and the Veriso overview, Barrier and Process pages link back to it. Existing Advisory URLs are preserved. The HSSE page uses four native expandable service groups, retaining all fourteen services and enquiry links. Hash links open the relevant group. Specialist services use compact rows; the practice film follows the engagement routes in a split layout. Additional support remains available within the delivery section. Practice-specific layout rules are in `assets/css/practice.css`.

The practice also connects high-performance leadership and teams, critical thinking and decision-making, and ultra-high-risk work. Specialist pages describe delivered activities and tangible outputs; existing `/advisory/hpo/` and `/advisory/ohtl/` addresses remain unchanged. These are service descriptions, not additional case-study claims.

Service enquiries use allowlisted `service=hsse` or `service=hsse-1` through `hsse-14`, plus `hpo`, `critical-thinking` and `ultra-high-risk` parameters. The contact form preselects the matching service, records its readable name in `service_detail`, and retains the selection when switching language. No message is sent until the visitor submits the existing form.

The practice copy is adapted from the owner's 8 November 2026 draft. Before public release, resolve that draft's managed-service activity-scope question and outstanding certification evidence and product-naming decisions. The new pages make no certification claim; the Advisory hub's unsupported certification wording has been removed. The remaining bare ISO certification labels on Group and specialist pages have been omitted pending supporting evidence; service descriptions about alignment to standards remain. The unverified fixed deployment-time promise has also been replaced with scope-dependent wording.

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

VideoObject metadata records the first website publication on 8 November 2026. Preserve this date for the existing editions; use the actual publication timestamp for future new editions.
