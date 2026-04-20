# Data Science — Neurosteer Brain Metrics Research

Research and analysis workspace for Neurosteer's EEG-based cognitive assessment metrics. This directory contains the data, models, analysis notebooks, and the Physician Guide that feed into the production Offline Session Pipeline (OSP) and the RCM report template.

## What This Directory Produces

1. **Brain Age model** (`brain_age_model_v2-0-1.json`) — ElasticNet-selected linear regression model predicting brain age from 20 EEG + behavioral features. Trained here, copied to `lib/report_data/assets/` in the OSP.

2. **Physician Guide** (`Neurosteer_Physician_Guide_v6.md` / `.docx`) — Comprehensive clinical reference document describing all 16 metrics, Brain Age, validation data, and interpretation guidelines.

3. **Metric definitions** (`config.py` in OSP) — 16 per-task metrics organized by cognitive load level. Defined here through validation analysis, then configured in the OSP.

## Current Metrics (February 2026)

16 metrics validated against MMSE cognitive scores, HRV, and cortisol across 977 participants.

| Feature | Cognitive Loads | What It Measures | Validation |
|---------|----------------|------------------|------------|
| A0 | rest, mid, hi | Cognitive Resource Allocation | r(MMSE) -0.34 to -0.44 |
| TBR | lo, hi | Attention Regulation (Theta - Beta) | r(MMSE) +0.37 to +0.48 |
| BAR | lo, hi | Stress Reactivity (Beta - Alpha) | r(MMSE) -0.39 to -0.50, cortisol-validated |
| ST4 | rest | Physiological Stress at Rest | HRV-validated |
| T2 | hi | Stress Under High Load | Informational |
| RT | lo, hi | Cognitive Processing Speed | r(MMSE) -0.22 to -0.46 |
| Error | lo, hi | Cognitive Accuracy | d(H vs MD) up to +1.24 |
| VC9 | rest, hi, diff | Working Memory / Individual Performance | rho=-0.44 vs RT (healthy) |

Full details with population norms, flag thresholds, and clinical descriptions: see `metric_reference.md`.

## Brain Age Model

### Production: v2-0-1 (current)
- **Method**: ElasticNet feature selection + LinearRegression, trained on full population
- **Features (20)**: Response time, accuracy, A0, T2, Delta, Alpha, Gamma — per task and between-task contrasts
- **Required tasks**: d1, d2, nb1, nb2, rest_closed (4 of 5 minimum)
- **Performance**: CV r=0.65, MAE=13.2 years (N=653)
- **Bias correction**: Age-dependent (slope=-0.61, intercept=29.8), healthy gap centers at ~0
- **Clinical group gaps** (age-matched 60-85): Healthy +1.5, MCI +7.0, Dementia +16.8 years
- **Error margin**: +/- 7.5 years
- **Model file**: `brain_age_model_v2-0-1.json` (in OSP assets)

### Retired: v3-0-0
- Ridge regression (alpha=100), EEG-only features (TBR, BAR, Beta, Gamma, A0), trained on healthy-only (N=280)
- CV r=0.41, MAE=11.3 — reverted because raw scores clustered around ~58 for all participants regardless of brain health, making the model unreliable when real age is unavailable
- Model JSON kept in OSP assets for reference; `brain_age.py` retains backward-compatible v3 code (derived features, MeanAll)

## Files

### Data
| File | Description |
|------|-------------|
| `df_hrv.pkl` | Main dataset — per-task EEG + behavioral + HRV + MMSE, 977 participants |
| `first_session_all.csv` | First session data for all subjects |

### Notebooks
| File | Description |
|------|-------------|
| `hrv_analysis.ipynb` | Main analysis notebook — data exploration, metric computation, validation |
| `brain_age_exploration.ipynb` | Brain age model exploration — feature correlations, model comparison, v3 development |

### Models & References
| File | Description |
|------|-------------|
| `brain_age_model_v3-0-0.json` | Brain Age model v3 (retired): weights, scaler stats, imputation means, bias correction |
| `metric_reference.md` | Complete metric reference with population norms and clinical descriptions |

### Physician Guide
| File | Description |
|------|-------------|
| `Neurosteer_Physician_Guide_v6.md` | Source markdown for the physician guide (20 sections + appendices) |
| `Neurosteer_Physician_Guide_v6.docx` | Built Word document from the markdown |
| `build_physician_guide_docx.py` | Script to build the docx from the markdown |
| `physician_guide_figures_v2.py` | Script to generate all 12 validation figures |
| `physician_guide_figures/` | 12 curated PNG figures referenced in the guide |

## Relationship to OSP

1. **Brain Age Model**: `brain_age_model_v2-0-1.json` in `lib/report_data/assets/` in the OSP. The OSP's `brain_age.py` loads and applies it during report generation. Code also supports derived features (TBR, BAR) and MeanAll aggregation for future model versions.

2. **Config**: Metric definitions (task groupings, features, ranges) are in `lib/report_data/config.py` in the OSP.

3. **RCM Template**: The report template in `rcm_bundle_windows/` uses population norms and clinical interpretations derived from this research data.

## Physician Guide Website (Live)

Interactive web version of the physician guide, deployed to GitHub Pages.

| | |
|---|---|
| **Live URL** | https://netacello.github.io/-ns-guide-private/ |
| **Publications** | https://netacello.github.io/-ns-guide-private/publications.html |
| **Source files** | `physician guide/website/` (index.html, publications.html, styles.css, js/, assets/) |
| **Launch email** | `physician guide/website/email_physician_guide_launch.html` |
| **Repo branch** | `main` = deployed; `master` = working source |

### Deploy process
```bash
WTREE=$(mktemp -d)
git worktree add "$WTREE" main
cp "physician guide/website/styles.css"                   "$WTREE/styles.css"
cp "physician guide/website/Neurosteer Physician Guide.html" "$WTREE/index.html"
cp "physician guide/website/publications.html"            "$WTREE/publications.html"
# copy any new assets into $WTREE/assets/ if needed
cd "$WTREE" && git add -A && git commit -m "deploy: ..." && git push origin main
git worktree remove "$WTREE"
```

### Interactive figures
Generated by `generate_plotly_data.py` → writes `physician guide/website/js/data.js`.  
Re-run after any data or figure changes, then redeploy.

### CSS cache-busting
Currently at `styles.css?v=4` in both HTML files. Bump to `?v=5` on next CSS-only deploy.

### Known issues fixed (April 2026)
- **Mobile overlay bug**: `nav-overlay` had `display:block` in media query even when closed → invisible z-index:1050 wall blocked all taps. Fixed with `pointer-events:none` when inactive.
- **iOS anchor scroll**: `body.overflow:hidden` during drawer open swallowed anchor navigation. Fixed with double-`requestAnimationFrame` + manual `scrollIntoView`.

### Publications — pending
SSRN paper `abstract_id=6520190` is in the "Under Review" section with placeholder title/authors. Update `publications.html` once the page is accessible.

## Version History

| Date | Change |
|------|--------|
| 2026-02-22 | Reverted Brain Age to v2-0-1; v3 EEG-only model unreliable without age input. Updated physician guide with new gap figure (5 groups including young healthy). |
| 2026-02-19 | Brain Age v3-0-0: Ridge regression on healthy-only with derived TBR/BAR features |
| 2026-02-18 | Cognitive-load-aligned metrics revision: 16 per-task metrics + Brain Age v2 |
| 2026-02-17 | Physician Guide v6: reordered sections, updated VC9 behavioral correlation, all figures regenerated |
| 2026-02-05 | Brain Age v1-0-0: initial ElasticNet model |
