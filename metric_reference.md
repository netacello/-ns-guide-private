# Neurosteer Brain Metrics — Metric Reference

Version: Revised Metrics v4 (February 2026)
Population: 977 participants, 859 healthy reference subjects
Validation: MMSE cognitive scores, HRV, cortisol, age, group differentiation (Healthy / MCI / Mild Dementia)

---

## Summary Table

| # | Metric | Level | Scale | P5 | P80 | Flag | Dir | r(MMSE) | d(H/MD) |
|---|--------|-------|-------|----:|----:|------|-----|--------:|--------:|
| 1 | A0 | rest | 0–100 | 60.7 | 79.2 | 79.2 | above | +0.20 | +0.91 |
| 2 | A0 | mid_cog | 0–100 | 65.5 | 84.8 | 84.8 | above | +0.42 | +1.27 |
| 3 | A0 | hi_cog | 0–100 | 62.5 | 82.8 | 82.8 | above | +0.21 | +1.44 |
| 4 | TBR | lo_cog | -30–30 | -0.9 | 12.1 | -0.9 | below | -0.07 | -0.93 |
| 5 | TBR | hi_cog | -30–30 | -2.6 | 11.1 | -2.6 | below | -0.13 | -0.85 |
| 6 | BAR | lo_cog | -30–30 | -6.3 | 1.5 | 1.5 | above | +0.04 | +1.07 |
| 7 | BAR | hi_cog | -30–30 | -5.7 | 2.4 | 2.4 | above | +0.11 | +1.13 |
| 8 | ST4 | rest | 0–100 | 34.1 | 52.8 | — | none | -0.10 | -0.15 |
| 9 | T2 | hi_cog | 0–100 | 35.8 | 57.3 | — | none | +0.01 | +0.13 |
| 10 | RT | lo_cog | 500–5000 | 1167 | 2348 | 2348 | above | +0.31 | +1.44 |
| 11 | RT | hi_cog | 500–5000 | 1050 | 2295 | 2295 | above | +0.20 | — |
| 12 | Error | lo_cog | 0–50 | 0.0 | 5.9 | 5.9 | above | +0.15 | +1.25 |
| 13 | Error | hi_cog | 0–50 | 6.2 | 32.1 | 32.1 | above | +0.20 | +1.23 |
| 14 | VC9 | rest | 0–100 | 43.6 | 58.6 | — | none | -0.10 | +0.16 |
| 15 | VC9 | hi_cog | 0–100 | 43.7 | 63.0 | — | none | -0.11 | +0.23 |
| 16 | VC9 | diff | -50–50 | -4.2 | 9.8 | — | none | +0.01 | -0.25 |

**Legend:**
- P5/P80 = 5th/80th percentile of healthy reference population
- Flag = threshold for clinical attention; Dir = flagged if value is above/below threshold
- r(MMSE) = Spearman correlation with MMSE cognitive score (positive r means higher metric = higher MMSE)
- d(H/MD) = Cohen's d effect size between Healthy and Mild Dementia groups

---

## Task Groupings

| Level | Tasks | Description |
|-------|-------|-------------|
| rest | rest_closed | Eyes-closed resting state |
| rest (ST4/VC9) | rest_closed, rest_positive, rest_open, rest_music, rest_clear, rest_med | All rest variants |
| lo_cog | d1, nb0, immediate_recall | Low cognitive load (TBR/BAR); d1, nb0 only for RT/Error |
| mid_cog | nb0, statements | Moderate cognitive load (A0 only) |
| hi_cog | nb2, nb3, late_recall, clock | High cognitive load (A0/TBR/BAR/ST4/T2/VC9); nb2, nb3 only for RT |
| hi_cog (Error) | nb2, nb3, immediate_recall, late_recall | High cognitive load for Error rate |

---

## Metric Details

### 1–3. A0 — Cognitive Resource Allocation

**What it measures:** Overall brain activation level. Lower A0 indicates more efficient neural processing — the brain accomplishes the same cognitive work with fewer resources. Higher A0 suggests the brain is working harder, which correlates with cognitive decline.

**Tasks:**
- A0 rest: `rest_closed` — brain at rest, purest baseline (r(MMSE)=+0.20)
- A0 mid_cog: `nb0, statements` — moderate verbal/working memory load (r(MMSE)=+0.42, strongest MMSE correlation)
- A0 hi_cog: `nb2, nb3, late_recall, clock` — peak executive demand (d=+1.44, largest group separation)

**Validation:**
- r(MMSE) = +0.20 to +0.42 (higher A0 → lower MMSE → worse cognition)
- d(H vs MD) = +0.91 to +1.44 (large effect sizes)
- Clinical gradient: Healthy 72–78 → MCI 80–85 → Mild Dementia 80–89

**Patient description:** This metric measures how much energy your brain uses during [rest / moderate tasks / challenging tasks]. A value within the healthy range indicates efficient brain function. A value above the healthy range may suggest your brain is working harder than typical to maintain performance.

**Flag:** Above P80 (79.2 / 84.8 / 82.8) — brain overactivation

---

### 4–5. TBR — Attention Regulation (Theta minus Beta)

**What it measures:** Balance between theta (slow, internally-directed) and beta (fast, externally-focused) brain activity. Higher TBR indicates better top-down attention regulation. Lower TBR in dementia populations reflects disrupted attention control networks.

**Tasks:**
- TBR lo_cog: `d1, nb0, immediate_recall` — simple attention tasks
- TBR hi_cog: `nb2, nb3, late_recall, clock` — complex attention tasks

**Validation:**
- r(MMSE) = -0.07 to -0.13 (lower TBR → lower MMSE)
- d(H vs MD) = -0.85 to -0.93 (MD group has lower TBR)
- Healthy mean: 6.8–7.5; MD mean: 2.1–2.8

**Patient description:** This metric reflects your brain's ability to regulate attention. A value within the healthy range indicates normal attention control. A value below the healthy range may indicate difficulty maintaining focused attention.

**Flag:** Below P5 (-0.9 / -2.6) — impaired attention regulation

---

### 6–7. BAR — Stress Reactivity (Beta minus Alpha)

**What it measures:** Neural stress response. Higher BAR (more beta relative to alpha) indicates greater cortical stress activation. Validated against pre-session salivary cortisol levels (r=-0.42, p<0.05).

**Tasks:**
- BAR lo_cog: `d1, nb0, immediate_recall` — baseline stress under easy tasks
- BAR hi_cog: `nb2, nb3, late_recall, clock` — stress under demanding tasks

**Validation:**
- r(MMSE) = +0.04 to +0.11 (higher BAR → marginally higher MMSE; weak direct MMSE link)
- d(H vs MD) = +1.07 to +1.13 (MD group has higher stress)
- Cortisol-validated: BAR correlates with pre-session cortisol (r=-0.42)
- Healthy mean: -1.2 to -0.5; MD mean: 2.4 to 3.5

**Patient description:** This metric measures your brain's stress response during [easy / challenging] cognitive tasks. A value within the healthy range indicates a normal stress response. A value above the healthy range may suggest elevated neural stress reactivity.

**Flag:** Above P80 (1.5 / 2.4) — elevated stress reactivity

---

### 8. ST4 — Physiological Stress at Rest

**What it measures:** Resting-state physiological stress indicator from transformer model. Validated via HRV autonomic markers (PNN50, RMSSD). Not a primary cognitive decline marker — used for stress monitoring.

**Tasks:** All rest variants (rest_closed, rest_positive, rest_open, rest_music, rest_clear, rest_med)

**Validation:**
- r(MMSE) = -0.10 (weak; not a cognitive decline marker)
- d(H vs MD) = -0.15 (minimal group difference)
- HRV-validated (autonomic stress)

**Patient description:** This metric reflects your physiological stress level during rest periods. It is shown for informational purposes as part of your overall brain health profile.

**Flag:** None (informational)

---

### 9. T2 — Physiological Stress Under High Load

**What it measures:** Stress response under cognitive demand from transformer model. Weak HRV support (SDNN). Not a primary cognitive decline marker — used for stress monitoring under load.

**Tasks:** nb2, nb3, late_recall, clock

**Validation:**
- r(MMSE) = +0.01 (not correlated with cognition)
- d(H vs MD) = +0.13 (minimal group difference)

**Patient description:** This metric reflects your physiological stress level during challenging cognitive tasks. It is shown for informational purposes as part of your overall brain health profile.

**Flag:** None (informational)

---

### 10–11. Response Time — Cognitive Processing Speed

**What it measures:** Average reaction time in milliseconds on button-press tasks. Lower is better (faster processing). Only uses button-press tasks (d1, nb0, nb2, nb3) for comparable paradigm.

**Tasks:**
- RT lo_cog: `d1, nb0` — simple detection/working memory
- RT hi_cog: `nb2, nb3` — complex working memory

**Validation:**
- r(MMSE) = +0.20 to +0.31 (slower RT → lower MMSE)
- d(H vs MD) = +1.44 (lo_cog; large effect size)
- Healthy mean: 1841–1945 ms; MD mean: 2580–3537 ms

**Patient description:** This metric measures how quickly you respond during [easy / challenging] cognitive tasks. A value within the healthy range indicates normal processing speed. A value above the healthy range may suggest slower cognitive processing.

**Flag:** Above P80 (2348 / 2295 ms)

---

### 12–13. Error Rate — Cognitive Accuracy

**What it measures:** Percentage of incorrect responses. Lower is better (fewer errors). Computed as `(1 - accuracy) * 100`.

**Tasks:**
- Error lo_cog: `d1, nb0` — should be near zero for healthy subjects
- Error hi_cog: `nb2, nb3, immediate_recall, late_recall` — errors emerge under load

**Validation:**
- r(MMSE) = +0.15 to +0.20 (more errors → lower MMSE)
- d(H vs MD) = +1.23 to +1.25 (large effect sizes)
- Healthy mean: 5.4% (lo) / 23.1% (hi); MD mean: 24.8% (lo) / 38.1% (hi)

**Patient description:** This metric measures your accuracy during [easy / challenging] cognitive tasks. A value within the healthy range indicates normal cognitive accuracy. A value above the healthy range may suggest difficulty maintaining accuracy under cognitive demand.

**Flag:** Above P80 (5.9% / 32.1%)

---

### 14–16. VC9 — Working Memory / Individual Performance

**What it measures:** Vigilance component indexing individual cognitive performance style. Not correlated with MMSE — represents within-subject variability rather than cognitive decline. The difference metric (hi_cog minus rest) measures working memory engagement.

**Tasks:**
- VC9 rest: All rest variants
- VC9 hi_cog: nb2, nb3, late_recall, clock
- VC9 diff: hi_cog minus rest (computed in OSP, arrives as `PerTaskDif.VC9.HicogRest`)

**Validation:**
- r(MMSE) = -0.10 to +0.01 (not correlated — individual marker, not cognitive decline)
- d(H vs MD) = -0.25 to +0.23 (minimal group differences)
- Healthy mean: 53.2 (rest) / 56.1 (hi_cog) / 4.5 (diff)

**Patient description:** This metric reflects your individual brain activity pattern during [rest / challenging tasks]. It shows how your brain engages working memory resources. The difference between rest and cognitive load reflects your working memory engagement level.

**Flag:** None (informational/exploratory)

---

## Appendix: Validation Methodology

- **Population**: 977 participants total. 306 healthy, 85 MCI, 33 mild dementia (MD), 553 without MMSE classification
- **MMSE correlation**: Spearman rank correlation between per-user metric and MMSE score
- **Effect sizes**: Cohen's d between healthy and MD groups (pooled standard deviation)
- **HRV validation**: Correlation with PNN50, RMSSD, SDNN for stress-related metrics
- **Cortisol validation**: BAR correlated with pre-session salivary cortisol (n=~40, r=-0.42, p<0.05)
- **Age sensitivity**: Spearman correlation with age to confirm age-related cognitive changes
- **Population norms**: P5 and P80 percentiles computed from healthy reference subjects only
- **Flag thresholds**: P80 for "higher is worse" metrics, P5 for "lower is worse" metrics
