# Neurosteer Guide HTML — Development Log

> A complete record of every iteration of the physician guide — from `neurosteer_guide.html` prototypes to the live GitHub Pages website.

---

## Current State — April 2026 (Live Website)

The guide is now a **multi-page GitHub Pages website** at https://netacello.github.io/-ns-guide-private/

### Architecture
- `main` branch = deployed site (GitHub Pages root)
- `master` branch = working source in `physician guide/website/`
- Deploy: git worktree → copy files → commit → push (see README.md for full command)

### Pages
| Page | URL | Description |
|------|-----|-------------|
| Physician Guide | `/` (index.html) | 13 sections, all neuromarkers, interactive Plotly charts |
| Publications | `/publications.html` | 13+ papers sorted newest-first, expandable abstracts |
| Launch email | `/email_physician_guide_launch.html` | HTML email template for team announcement |

### Features implemented
- 12 interactive Plotly.js figures (hover, zoom, group filter) via `js/data.js` + `js/figures.js`
- Expandable scientific background sections (`<details>/<summary>` + CSS)
- Collapsible left rail on desktop (‹/› toggle)
- Mobile hamburger menu (slide-in drawer, overlay backdrop, auto-close on link tap)
- Sample patient reports with 42-point scoring table and gauge cards
- Neurofeedback protocol section
- Subtle photo animations (hero float + hover lift on all figures)
- OG/Twitter meta tags for WhatsApp social thumbnail

### Plotly figure IDs (in js/data.js)
`brain-age-sci-fig1`, `brain-age-sci-fig2`, `nei-sci-fig1/2/3`, `tbr-bar-sci-fig1/2`, `rsi-sci-fig1`, `rt-sci-fig1/2`, `nfb-sci-fig1`, `tai-sci-fig1`

### Critical bugs found and fixed
1. **Mobile overlay pointer-events** (April 2026): `@media (max-width:900px) { .nav-overlay { display:block } }` made the overlay visible to pointer events even when closed (opacity:0 but blocking). All mobile taps were intercepted. Fix: `pointer-events:none` on inactive overlay.
2. **iOS anchor scroll** (April 2026): `body.overflow:hidden` during drawer open ate anchor navigation. Fix: `e.preventDefault()` + double `requestAnimationFrame` + `scrollIntoView()`.
3. **Brain age bias formula**: `generate_hq_figures.py` had wrong formula. Correct: `bias = bias_intercept + bias_slope * real_age; brain_age = score - bias` (from `generate_sample_reports.py`).
4. **HRV/PNN50 data scope**: Only exists in Forest cohort (`mmse_group=0`), not in clinical GROUPS. `rsi-sci-fig1` needed `has_group_data` fallback.

### CSS cache version
Currently `styles.css?v=4`. Bump on next CSS-only deploy.

### Pending
- SSRN paper `abstract_id=6520190` in publications.html has placeholder title — update once accessible.

---

---

## Origin Story — Why HTML Instead of PPT

The guide started as a **PowerPoint presentation** request (v3, 18 slides) that kept failing:

1. The user wanted real report-style range-bar strips and Brain Age arc gauges — not generic Plotly gauges
2. Every screenshot crop was "way off" — captured extra content, wrong sizes
3. The PDF → PNG → PPT pipeline couldn't produce the pixel-precise metric cards the user wanted

At **line 1310 of session `0d5b73f2`** the user proposed:
> *"I think of a new approach! maybe instead of building a ppt, you will build a website — just a landing page of these slides. In this way you would be able to design via html and be sure of all the sizes, fonts, alignments."*

This became the `neurosteer_guide.html` project. All 4 versions (+ v5) were built in Claude Code sessions.

---

## Recovered Versions

All previous versions are saved as:
- `neurosteer_guide_v1_recovered.html` — 58,837 chars
- `neurosteer_guide_v2_recovered.html` — 67,574 chars
- `neurosteer_guide_v3_recovered.html` — 67,692 chars — **BEST DESIGN**
- `neurosteer_guide_v4_recovered.html` — 48,415 chars
- `neurosteer_guide.html` — current (v5), 51,446 chars — user said "we went back"

---

## Version 1 — "The Foundation" (58,837 chars)

**User reaction: "thank you!!! looks great!!! what a progress!!!!"**

### Structure
21 full-screen sections (each `min-height:100vh`), alternating dark/light:
```
title → brain-age-report → brain-age-science →
sbs-eeg → a0-report → a0-science →
tbr-bar-report → tbr-bar-science →
l1-report → l1-science →
vc9-report → vc9-science →
st4-t2-report → st4-science →
rt-report → rt-science →
error-report → error-science →
summary → abnormal → nfb
```

### Visual Design
- **Font**: `'Segoe UI', Arial, sans-serif`, 18px base
- **Nav**: `#topnav` sticky, background `#0a1628`, blue active highlight `#1e3a6e`
- **Sections alternated**:
  - `.report` — dark navy `#0f1e3d`, light text `#e8edf8`
  - `.science` — white `#ffffff`
  - `.dark-alt` — near-black `#111827`
  - `.abnormal` — dark blood red `#1a0808`, red text
  - `.nfb` — dark forest green `#0d1f17`
- **Typography**: h1=3rem/800, h2=2.4rem/700 — large, impactful
- **Content cards**: `.key-panel` with colored left borders (blue/green/teal/brown/red/purple)
- **Stats**: glass-morphism `.stat-box` with semi-transparent colored backgrounds
- **Metric strips**: **IMAGE BASED** — `<img>` tags pointing to `physician_guide_prep/crop_*.png` files

### What Was Wrong
- Strips were **PNG screenshots** from the PDF — not recreated as HTML/Canvas
- No speedometer gauges in abnormal section
- Neurofeedback section was minimal text-only
- No interactive needle positioning

---

## Version 2 — "Canvas Strips" (67,574 chars)

**User reaction:** immediate follow-up request to recreate figures as HTML/Canvas. No additional positive feedback captured before context ran out.

### Changes from v1
- Added **JavaScript `drawRangeStrip()`** — Canvas-drawn metric strips replacing PNG screenshots
- Added **`posNeedle()`** — positioned a needle image (`Needle Generic.png`) on each strip
- Added **Canvas speedometer gauges** in the abnormal section
- Defined `METRICS` and `METRICS_ABN` JS objects with all 16+ metric configs
- Added `METRICS_ABN` for abnormal patient example values (A0=88, TBR=30, ST4=68, BAR=22)
- Canvas-based Brain Age arc gauge (JS drawn)
- Canvas-based SBS EEG chart (`#sbsCanvas`)

### What Was Wrong (identified by user, line 1462)
- Logo "smur, too much stretched" — needed `width:auto; height:32px; object-fit:contain`
- Woman photo: low resolution, AI watermark ("Gemini sign") visible bottom-right
- Text color invisible on dark blue backgrounds
- Nav anchor links not working (ID/href mismatches)
- Brain Age must use actual `brain_age_background.png` from rcm_bundle assets, not Canvas-drawn
- SBS EEG must use real payload JSON with rest/low/high background shading

---

## Version 3 — "Design Overhaul" (67,692 chars) ⭐ BEST VERSION

**Status:** User context ran out again before reviewing this version directly.
**This is the most polished and complete version that was built.**

### Major Design Changes
- **Font**: Added `Inter` via Google Fonts CDN — professional, clean
- **Nav**: Changed to `<nav>` with `position:fixed`, `backdrop-filter:blur(12px)` glass effect,
  background `rgba(8,18,44,0.97)`, border `rgba(255,255,255,0.07)`
- **Hero section** (`#home`, full-viewport):
  - Layered background: `#040d1e → #091b48 → #0d2b65` gradient + radial overlay
  - **Hero photo card**: 320×400px rounded box (`border-radius:18px`) with `overflow:hidden`
  - Photo enhancement CSS: `filter:brightness(1.06) contrast(1.04) saturate(1.07)`
  - **Watermark overlay**: `::after` with `linear-gradient(135deg, transparent 52%, rgba(4,13,30,.88) 100%)` — obscures bottom-right corner
  - Glass-morphism stat cards at bottom of photo card
  - **Pulsing dot animation** on hero badge: `@keyframes pulse`
  - **CTA button**: `linear-gradient(135deg,#42a5f5,#1565c0)` with hover lift effect
  - `clamp(34px,5vw,56px)` responsive typography
- **Section structure**: `.section` + `.section-inner{max-width:1060px}` — full-width bg, centered content
- **Consolidated**: 21 → 11 sections (L1+VC9 merged, RT+Error merged)

### Key Technical Features
- Brain Age: CSS `.ba-txt` overlays at `left:21.55%/50.29%/79.69%`, `top:55%` on actual image
- SBS EEG: Canvas chart loading real `payload_F_1953__AD.json` data with category-colored bands
- All metric strips: Canvas-drawn (no PNG screenshots), needle as `▼` Unicode char at 27px
- Speedometers in abnormal section: Canvas semicircle gauges (green arc = healthy, red needle)
- IntersectionObserver → replaced with `updateNav()` scroll-based active link detection
- Science figures embedded: `fig_l1_groups_parkinson.png`, `fig_l1_age_cortisol.png`, `fig_vc9_load_profile.png`

### Sections (11)
```
home → brain-age → sbs-eeg →
a0 → tbr-bar → l1-vc9 → st4-t2 → rt-error →
summary → abnormal → nfb-plan
```

---

## Version 4 — "Targeted Rebuild" (48,415 chars)

Built in same context as v3, immediately after — appears to be a focused rebuild targeting the specific issue list.

### Changes from v3
- **Smaller** (48K vs 67K) — stripped down, more focused
- Same 11-section structure
- Preserved Inter font, fixed nav, hero with `::after` overlay
- Strip width: `flex:0 0 46%` — strips now ~46% of row width (as requested: ~50% reduction)
- Scale row: min/mid/max labels below each strip
- `.interp` and `.interp.flag` panels in description column
- Summary: side-by-side `<img>` pair — no sliders
- Abnormal: `drawSpeedo()` Canvas gauges for 4 metrics
- SBS: loads `payload_2202a.json`

### What Was Lost vs v3
- Less visual polish overall
- Hero section may have been simplified
- Some science content sections condensed

---

## Version 5 — Current (51,446 chars)

Written in session `current` after context was fully lost from v3/v4.

### What It Has
- 11 sections, same structure
- `'Segoe UI'` (no Inter — Google Fonts CDN dropped)
- Nav: `position:sticky` (not `fixed` with backdrop-filter)
- Hero: basic flex layout, woman photo as `<img>` (not inside 320×400 rounded card)
- Strip col 46%, `▼` needle at 27px, Canvas strips
- TBR/BAR: 2 strips only (correct)
- Summary: side-by-side images (correct)
- Speedometers: Canvas semicircle for 4 metrics
- NFB: 3 cards (patient stats, how-it-works, Block 1 Cognitive, Block 2 Stress) — dark section
- SBS: loads `sbs_compact.json`

### What Regressed vs v3
- No Inter font (fell back to Segoe UI)
- Nav not `fixed` + no `backdrop-filter` glass effect
- Hero photo not in rounded 320×400 card — just a full-section background
- No `::after` double-gradient watermark remover on photo card
- No pulsing dot animation on hero badge
- No CTA button in hero
- `clamp()` typography partially dropped
- Sections not `min-height:100vh` (v1 feature that was nice for slide-like feel)
- Less rich science content in each section

---

## What Made Each Version Feel "Better" or "Worse"

| Feature | v1 | v2 | v3 ⭐ | v4 | v5 (current) |
|---|---|---|---|---|---|
| Full-screen slide feel (`min-height:100vh`) | ✅ | ✅ | ✅ | ❌ | ❌ |
| Inter font | ❌ | ❌ | ✅ | ✅ | ❌ |
| Fixed nav + glass blur | ❌ | ❌ | ✅ | ✅ | ❌ |
| Hero photo in rounded card | ❌ | ❌ | ✅ | partial | ❌ |
| Watermark gradient `::after` on photo | ❌ | ❌ | ✅ | ✅ | partial |
| Hero pulsing dot + CTA button | ❌ | ❌ | ✅ | ❌ | ❌ |
| Canvas strips (no PNG) | ❌ | ✅ | ✅ | ✅ | ✅ |
| Needle correct size | ❌ | ❌ | ✅ | ✅ | ✅ |
| Strip ~46% width | ❌ | ❌ | ✅ | ✅ | ✅ |
| TBR/BAR 2 strips only | ❌ | ❌ | ✅ | ✅ | ✅ |
| Brain Age CSS overlays on image | ❌ | ❌ | ✅ | ✅ | partial |
| SBS from real JSON | ❌ | partial | ✅ | ✅ | ✅ (sbs_compact.json) |
| Canvas speedometers | ❌ | ✅ | ✅ | ✅ | ✅ |
| NFB 3-section plan | ❌ | ❌ | partial | ✅ | ✅ |
| Summary images (no slider) | ❌ | ❌ | ✅ | ✅ | ✅ |
| Science figures per section | partial | ✅ | ✅ | partial | ✅ |

---

## Version 6 — "Exports-Based" (1,889 lines) ✅ BUILT

**Approach pivot:** Instead of Canvas-drawn strips/speedometers, uses extracted PNG images from `exports/` folder directly. Zero JavaScript canvas code.

### Key Changes vs All Previous Versions
- **ALL slider strips** → `exports/slider_*.png` (extracted from actual report PDF)
- **ALL speedometer gauges** → `exports/speedo_*.png` (extracted from abnormal patient report)
- **SBS chart** → `exports/sbs_chart.png` (no Canvas SBS at all)
- **Brain Age** → `exports/brain_age.png`
- **Hero photo** → `exports/woman_hires.png` (high resolution)
- **Zero canvas JavaScript** — only a scrollspy for nav active state
- **1,889 lines** of rich clinical content from v7 physician guide

### Structure (12 nav sections, 19 total sections)
- Home hero (Inter font, fixed glass nav, 310×400 photo card, pulsing dot, CTA)
- Brain Age report (dark) → Brain Age science (light)
- SBS EEG (dark alt)
- A0 report (dark) → A0 science (light)
- TBR/BAR report (dark) → TBR/BAR science (light)
- L1 report (dark) → L1 science (light)
- VC9 report (dark) → VC9 science (light)
- ST4/T2 report (dark) → ST4 science (light)
- RT/Error report (dark) → RT/Error science (light)
- Summary (light grey)
- Abnormal case (dark crimson) — speedo images
- NFB plan (deep navy)

### Design Features
- All v3 best-design features preserved (Inter, fixed blur nav, pulsing dot, clamp() fonts, min-height:100vh)
- CSS custom properties (--navy, --deep-navy, --crimson etc.)
- Report sections: dark navy #0e1f3d with slider images as centerpiece
- Science sections: alternating white / #f8f9fc
- Metric cards with colored header bars, two-column layout (slider + text)
- Flag boxes (red for abnormal), info boxes (blue for informational metrics)
- Population data tables, MMSE correlation tables, HRV validation tables

---

## The Right Next Version (v6) [COMPLETED — see above]

To build the definitive version, combine the BEST of v1+v3 (design) with the BEST of v4+v5 (correct feature set):

### Must Keep from v3 (the design gold standard)
```css
/* Inter font */
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap">
font-family:'Inter',system-ui,sans-serif;

/* Fixed nav + glass */
nav{position:fixed;backdrop-filter:blur(12px);background:rgba(8,18,44,0.97);}

/* Hero photo card */
.hero-photo-wrap{width:320px;height:400px;border-radius:18px;overflow:hidden;}
.hero-photo-wrap::after{background:linear-gradient(135deg,transparent 52%,rgba(4,13,30,.88) 100%)}
filter:brightness(1.06) contrast(1.04) saturate(1.07)

/* Pulsing badge dot */
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(1.3)}}

/* clamp() typography */
font-size:clamp(34px,5vw,56px)

/* CTA button */
background:linear-gradient(135deg,#42a5f5,#1565c0)
```

### Must Keep from v1 (the slide feel)
```css
section{min-height:100vh; display:flex; flex-direction:column; justify-content:center;}
/* Alternating dark/light for report/science feel */
```

### Must Keep from v4/v5 (correct technical features)
- Strip col `flex:0 0 46%` + `▼` needle 27px + no value badge
- TBR LoCog + BAR HiCog only (2 strips)
- Summary: side-by-side crop images
- Speedometers: Canvas semicircle
- NFB: 3-section plan (stats + how-it-works + Block1 Cog + Block2 Stress)
- SBS from `sbs_compact.json`
- `physician_guide_figures/` science figures per section

### New Feature Gaps to Fill
1. `brain_age_background.png` — need to confirm exact asset path:
   `../report-creation-data/rcm_bundle_windows/data/templates/reports/clinics/assets/images/`
2. Woman photo path — try: `physician_photo.png` or `woman_photo.png` in same assets dir
3. Logo path: same assets dir → `logo.png`
4. SBS data: `sbs_compact.json` already exists in `data_science/`
5. Summary table crops: `physician_guide_prep/crop_summary_table.png` + `physician_guide_prep_abn/crop_summary_table_abn.png`

---

## Asset Map (relative to `data_science/`)

```
Images from rcm_bundle (../report-creation-data/rcm_bundle_windows/data/templates/reports/clinics/assets/images/):
  logo.png                    — Neurosteer logo for nav
  physician_photo.png         — woman/physician hero photo (may vary)
  brain_age_background.png    — Brain Age arc background image

Report crop images (physician_guide_prep/):
  crop_brain_age_section.png  — healthy patient brain age section
  crop_summary_table.png      — healthy patient full summary table
  crop_sbs_eeg_full.png       — healthy patient SBS EEG chart crop

Report crop images (physician_guide_prep_abn/):
  crop_brain_age_section_abn.png  — abnormal patient brain age section
  crop_summary_table_abn.png      — abnormal patient full summary table

Science figures (physician_guide_figures/):
  fig02_a0_load_profile.png       — A0 by group across load levels
  fig_a0_mmse_scatter.png         — A0 vs MMSE (3-panel)
  fig_a0_cortisol1_clean.png      — A0 vs CORTISOL_1
  fig_l1_groups_parkinson.png     — L1 by diagnostic group
  fig_l1_age_cortisol.png         — L1 vs age + cortisol
  fig_vc9_load_profile.png        — VC9 load profile
  fig08_st4_hrv.png               — ST4 vs PNN50/RMSSD (2-panel)

Data files (data_science/):
  sbs_compact.json                — 1072-point SBS data (Category, A0, TBR, ST4, BAR)
```

---

## Patient Data Used in the Guide

### Healthy Patient: F_1953__AD (Age 73, Female)
Source: `batch_reports/Ariel_group/payload_F_1953__AD.json`

| Metric | Value | In Range? |
|---|---|---|
| BrainAge | 72.1 (Gap: −0.9 yr) | ✅ |
| A0 Rest | 77.9 | ~border |
| A0 Mid | 86.2 | above |
| A0 Hi | 86.1 | above |
| TBR LoCog | −7.6 | ✅ (lower end) |
| BAR HiCog | 9.36 | ✅ |
| L1 LoCog | 42.1 | border (low end) |
| VC9 HiCog | 48.6 | ✅ |
| ST4 Rest | 37.2 | ✅ |
| T2 HiCog | 80.1 | ✅ |

### Abnormal Patient: M_1970__RC (Age 56, Male, "Ariel")
Source: synthetic — patched from real payload, values set to abnormal

| Metric | Value | Flag | Clinical significance |
|---|---|---|---|
| BrainAge | 70.0 (Gap: +14 yr) | ❌ | Accelerated neural aging |
| A0 Rest | 88.0 | ❌ above 75.4 | Over-activation, MMSE r=−0.44 |
| A0 Mid | 86.5 | ❌ | Flat load profile |
| A0 Hi | 85.0 | ❌ | Failure to modulate |
| TBR LoCog | 30.0 | ❌ above 7.1 | Theta dominance, d≈−0.9 |
| BAR HiCog | 22.0 | ❌ above 12.0 | Cortisol-validated, r=−0.42 |
| ST4 Rest | 68.0 | ❌ above 55.0 | HRV-validated, PNN50 r=−0.34 |

---

## DrawRangeStrip() Specification

All strip Canvases are 500×52px (CSS: width 100%, height 52px).

```javascript
function drawStrip(canvasId, cfg) {
  // cfg: {sMin, sMax, hMin, hMax, hex, flagLo?, flagHi?, dual?}
  // 1. Gray gradient background (#dcdcdc → #c4c4c4)
  // 2. Healthy band: tint(hex, 0.84) top half, tint(hex, 0.56) bottom half
  // 3. "Healthy" label centered in band
  // 4. Flag lines: #CC3333 dashed [4,3] at flagLo/flagHi (or both hMin+hMax if dual:true)
  // 5. Border: rgba(0,0,0,0.1)
}

// Needle: Unicode ▼ at font-size:27px, position:absolute, top:-10px
// Positioned via: el.style.left = (val-sMin)/(sMax-sMin)*100 + '%'
```

### Metric Ranges (age 40-59 norms for abnormal patient)

| Metric | sMin | sMax | hMin | hMax | Color | Flag type |
|---|---|---|---|---|---|---|
| A0 Rest/Mid/Hi | 50 | 100 | 62.5 | 75.4 | `#117711` | flagHi |
| TBR LoCog | −20 | 40 | −0.4 | 7.1 | `#0A5555` | dual (both sides) |
| BAR HiCog | −10 | 30 | −4 | 12 | `#338888` | flagHi |
| L1 LoCog | 30 | 80 | 45 | 70 | `#115577` | flagLo (low is bad) |
| VC9 HiCog | 30 | 70 | 40 | 60 | `#3399BB` | flagHi |
| ST4 Rest | 10 | 80 | 20 | 55 | `#994422` | flagHi |
| T2 HiCog | 50 | 120 | 55 | 90 | `#CC7744` | flagHi |

---

## Canvas Speedometer Specification

For the Abnormal section — 4 gauges (300×170px each):

```javascript
function drawSpeedo(canvasId, cfg) {
  // cfg: {val, sMin, sMax, nMin, nMax}
  // Center: cx=W/2, cy=H*0.88, radius=min(W*0.40, H*0.76)
  // Arc: Math.PI → 2*Math.PI (bottom semicircle)
  // Track: gray #e8e8e8, lineWidth=R*0.26
  // Healthy band: green #c8e6c9 from ang(nMin) to ang(nMax)
  // Needle: from center to arc at val angle, color #2e7d32 (in) or #c62828 (out)
  // Value text: bold, color matches needle
  // Scale: sMin (right of arc left end), sMax (right of arc right end)
}
```

| Gauge | val | sMin | sMax | nMin | nMax |
|---|---|---|---|---|---|
| A0 | 88 | 50 | 100 | 62.5 | 75.4 |
| TBR | 30 | −20 | 40 | −0.4 | 7.1 |
| ST4 | 68 | 10 | 80 | 20 | 55 |
| BAR | 22 | −10 | 30 | −4 | 12 |

---

## SBS EEG Chart Specification

Data from `sbs_compact.json` (1072 data points):
- Keys: `Category` (string array), `A0`, `TBR`, `ST4`, `BAR` (float arrays)
- Category values: `rest`, `low`, `mid`, `high`, `unknown`, `instructions`

Background zone colors:
```javascript
const CAT_CLR = {
  rest:         'rgba(140,185,220,0.22)',
  low:          'rgba(140,210,140,0.22)',
  mid:          'rgba(240,195,100,0.22)',
  high:         'rgba(255,175,100,0.28)',
  unknown:      'rgba(180,180,180,0.10)',
  instructions: 'rgba(200,170,220,0.18)'
};
```

Biomarker line colors: A0=`#55CC55`, TBR=`#33AAAA`, ST4=`#DD8855`, BAR=`#55AACC`

---

## NFB Plan Content

Three components for the "Abnormal" patient (Ariel, 56M, flagged: A0+TBR+ST4+BAR):

**Overview card** — patient stats table:
- Name: Ariel B. | Age/Sex: 56/M | Sessions: 0/20
- Flagged: A0, TBR, ST4, BAR | Brain Age Gap: +14 yr
- Protocol: Cognitive + Stress (20 sessions)

**How It Works card** — description of operant EEG conditioning

**Block 1 — Cognitive (Sessions 1–10)**
- Targets: A0 (over-activation), TBR (theta dominance), L1 (alertness)
- Exercises: Focused Attention Training, Alpha Modulation Protocol, Working Memory Enhancement

**Block 2 — Stress (Sessions 11–20)**
- Targets: ST4 (resting stress), BAR (stress reactivity)
- Exercises: Resting Stress Reduction, Stress Reactivity Training, HRV Biofeedback Integration

---

## Session History

| Session file | Content | HTML writes |
|---|---|---|
| `d5afd8b6` | Physician guide markdown, notebook analysis | 0 |
| `5a18a21c` | L1/cortisol exploration, HRV analysis | 0 |
| `8ce1374d` | Brief session | 0 |
| `08b4fcd6` | Email drafts (L1 Lior, NFB Ariel) | emails only |
| `0d5b73f2` | **PPT → HTML pivot; all 4 HTML versions** | **4 writes** |
| Current | Context rebuild → v5 (user: "went back") | 1 write |

---

## Instructions for the Next Builder (v6)

1. **Start from `neurosteer_guide_v3_recovered.html`** — it has the best visual design
2. **Apply v4/v5 corrections** to v3: strip width 46%, no value badge, 2 TBR/BAR strips, summary images, speedometers
3. **Do NOT lose** from v3: Inter font, fixed+blur nav, 320×400 rounded hero photo card with `::after` gradient, pulsing dot, CTA button, `clamp()` fonts, `min-height:100vh` sections
4. **Update SBS** to use `sbs_compact.json` (not `payload_2202a.json`)
5. **Add missing physician interpretation text** in the freed right column of each metric row
6. **Test image paths** — all relative to `data_science/` directory
7. **Keep it self-contained** — single HTML file, no build step, no server required
