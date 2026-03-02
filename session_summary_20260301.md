# Session Summary — 2026-03-01

## What was done

### 1. Implemented three alternative CH4 modelling schemes (Section 9)

Added to `20260301_yu_soilliq_fsat_methane.ipynb`:

#### Scheme A — Detrended NPP
- **Problem addressed**: CLM2 CO₂-fertilisation drives NPP up ~42% through the Holocene, swamping the orbital FSAT signal by a factor of 2.1×.
- **Method**: Subtract a 2000-yr Gaussian running mean (σ = 100 timesteps = 1000 yr) from each grid cell's NPP time series, add back the temporal mean. Detrended NPP retains orbital/monsoon variability while removing the CO₂ trend. SOILLIQ FSAT unchanged.
- **Reference**: Kaplan (2002, *GRL*)

#### Scheme B — Seasonal PRECT FSAT
- **Problem addressed**: Annual-mean SOILLIQ/PRECT misses the precessional NH/SH anti-phase signal driven by JJA (NH monsoon) vs. DJF (SH monsoon) precipitation shifts.
- **Method**: Load `PRECT.22000BP_decavgJJA_400BCE.nc` and `PRECT.22000BP_decavgDJF_400BCE.nc` (already on disk). For each grid cell, blend the appropriate hemisphere's seasonal precipitation with the annual mean using a latitude weight `w = |lat|/30` (0% seasonal at equator → 100% at ±30°). Apply `estimate_fsat_from_precip(method='exponential')`.
- **Reference**: Singarayer & Valdes (2011, *Nature*)

#### Scheme C — Curvature-TWI SOILLIQ FSAT
- **Problem addressed**: SOILLIQ FSAT ignores subgrid topographic control (steep slopes drain quickly; flat basins accumulate water → wetlands).
- **Method**: Could not use ETOPO1 DEM (file in repo is Antarctic-only, EPSG:3031). Instead, computed Topographic Wetland Potential (TWP) from the spatial Laplacian of long-term mean SOILLIQ saturation: `TWP = clip(−∇²(sat̄_shallow), 0)`. Negative Laplacian = local saturation maximum = topographic basin. Multiply saturation by TWP before the sigmoid.
- **Reference**: Gedney & Cox (2003, *GRL*); Kaplan et al. (2019, *GMD*)
- **Note**: If global topography (PHIS) is downloaded from GDEX, Scheme C can be upgraded to use actual model-native slope.

#### Comparison plot
Added 4-panel figure `alternative_schemes_comparison.png`:
- (a) Global CH4 emissions time series for all 4 schemes
- (b) Holocene zoom (does any scheme show the bowl shape?)
- (c) NH/SH tropical FSAT ratio (expected to fall through Holocene if precession signal is captured)
- (d) Time-mean zonal CH4 flux

### 2. Committed and pushed to GitHub
- Repo: `https://github.com/yu-huang-1/offline-methane-trace21ka`
- Commit: `3b14afb` — "Add alternative methane modelling schemes (Section 9)"

---

## Key findings / diagnostics

| Scheme | Mean emissions | FSAT land mean | Notes |
|--------|---------------|----------------|-------|
| Original SOILLIQ | ~749 TgCH4/yr | 0.011 | Baseline |
| A: Detrended NPP | ~733 TgCH4/yr | 0.011 | NPP trend removed; FSAT unchanged |
| B: Seasonal PRECT | ~2307 TgCH4/yr | higher | Exponential FSAT, seasonal precip |
| C: Curvature-TWI | ~87 TgCH4/yr | very low | Basin mask very restrictive |

- Scheme B is the most scientifically motivated for reproducing the Holocene bowl (orbital precession → seasonal monsoon → FSAT anti-phase).
- Scheme A may help isolate the FSAT-driven CH4 signal by removing the CO₂ trend from NPP.
- Scheme C needs calibration (sat_crit, k) or a better TWP source (PHIS from GDEX).

---

## Data note

- The user can download additional CESM outputs from: **https://gdex.ucar.edu/datasets/d651050/dataaccess/**
- Specifically, `PHIS` (surface geopotential, m²/s²) from CAM would allow a proper slope-based TWP for Scheme C: `elevation = PHIS / 9.81` (m), then compute slope magnitude at T42 resolution.

---

## Files modified / created

| File | Status |
|------|--------|
| `20260301_yu_soilliq_fsat_methane.ipynb` | Section 9 added (5 new cells) |
| `session_summary_20260301.md` | This file |

---

## Earlier sessions (pre-compaction summary)

1. GitHub repo created and pushed: `offline-methane-trace21ka` (public)
2. `CLAUDE.md` created documenting project structure and conventions
3. New notebook `20260301_yu_soilliq_fsat_methane.ipynb` created with:
   - SOILLIQ-based FSAT (Sections 1–6, 4-panel comparison plot)
   - CH4 flux evolution GIF (`ch4_flux_evolution.gif`, 221 frames)
   - FSAT evolution GIF (`fsat_evolution.gif`)
   - Bowl-shape analysis: NH/SH decomposition, quantitative metrics
4. Key diagnostic: NH/SH FSAT anti-phase correlation r = +0.73 (in-phase, not anti-phase as expected); NPP dominates FSAT by 2.1× → bowl shape suppressed in original model
