# Data Science — Neurosteer Brain Metrics Research

Research and analysis workspace for Neurosteer's EEG-based cognitive assessment metrics. This directory contains the data, models, analysis notebooks, and the Physician Guide that feed into the production Offline Session Pipeline (OSP) and the RCM report template.

## What This Directory Produces

1. **Brain Age model** (`brain_age_model_v3-0-0.json`) — Ridge regression model predicting brain age from 20 EEG features. Trained here, copied to `lib/report_data/assets/` in the OSP.

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

## Brain Age Model (v3-0-0)

- **Method**: Ridge regression (alpha=100) trained on healthy participants only
- **Features (20)**: TBR, BAR, Beta, Gamma, A0, responsetime — per task (d1, d2, nb1) and session-wide means
- **Required tasks**: d1, d2, nb1, nb2, rest_closed (4 of 5 minimum)
- **Performance**: CV r=0.41, MAE=11.3 years (N=280 healthy)
- **Bias correction**: Age-dependent (slope=-0.83, intercept=49.6), healthy gap centers at ~0
- **Clinical group gaps** (age-matched 60-85): Healthy +0.3, MCI +6.4, Dementia +7.2 years
- **Error margin**: +/- 6.4 years
- **Model file**: `brain_age_model_v3-0-0.json`

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
| `brain_age_model_v3-0-0.json` | Brain Age model v3: weights, scaler stats, imputation means, bias correction |
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

1. **Brain Age Model**: `brain_age_model_v3-0-0.json` is copied to `lib/report_data/assets/` in the OSP. The OSP's `brain_age.py` loads and applies it during report generation. Supports derived features (TBR, BAR) and MeanAll aggregation.

2. **Config**: Metric definitions (task groupings, features, ranges) are in `lib/report_data/config.py` in the OSP.

3. **RCM Template**: The report template in `rcm_bundle_windows/` uses population norms and clinical interpretations derived from this research data.
