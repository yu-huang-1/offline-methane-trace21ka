# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a paleoclimate research project that computes offline methane flux from the [TraCE-21ka](https://www.cesm.ucar.edu/models/paleo/trace/) transient climate simulation dataset (22,000 BP to 400 BCE, decadal averages). The core formula is:

```
F_CH4 = FSAT × Knpp × NPP × Q10^((T - Tref) / 10)
```

where FSAT (fraction of saturated area) is not directly available in TraCE output and must be estimated from precipitation and temperature.

## Running the Model

```bash
# Run the offline methane model (requires all NetCDF data files present)
python methane_offline_model.py

# Interactive exploration is done in the Jupyter notebook
jupyter notebook 20260219_yu_offline_methane_model.ipynb
```

## Data Files

NetCDF data files are downloaded from NCAR GDEX (`osdf-director.osg-htc.org/ncar/gdex/d651050/TraCE/`). Download scripts are provided for each variable:

| Script | Variable |
|--------|----------|
| `gdex-download.csh` | FSA (absorbed solar radiation) |
| `gdex-download_npp.csh` | NPP (net primary production) |
| `gdex-download-soil.csh` | QSOIL (soil evaporation) |
| `gdex-download-soilliq.csh` | SOILLIQ (soil liquid water) |

The `.nc` files follow the pattern `trace.01-36.22000BP.{component}.{VAR}.22000BP_decavg_400BCE.nc` where component is `cam2` (atmosphere) or `clm2` (land model).

## Key Data Variables (NetCDF)

- `NPP` — Net Primary Production (gC/m²/s), CLM2 land model output
- `PRECT` — Total precipitation (m/s), CAM2 atmosphere output
- `T` — Atmospheric temperature (K), 4D: (time, lev, lat, lon) — lowest level used as surface proxy
- `TS` — Surface temperature (K), 3D
- `T10` — 10-cm soil temperature (K), CLM2
- `SOILLIQ` — Soil liquid water (kg/m²), CLM2
- `FSA` — Absorbed shortwave radiation (W/m²), CLM2

## Architecture

- `methane_offline_model.py` — Main model: `MethaneOfflineModel` class + `load_trace_data()` + `main()`. Outputs `trace_methane_offline_output.nc` and `trace_methane_diagnostics.png`.
- `20260219_yu_offline_methane_model.ipynb` — Interactive Jupyter notebook for analysis and visualization.
- `ETOPO1/` — Global topography/bathymetry data (GeoTIFF + shapefiles) for land/ocean masking.

## Model Parameters

Default values in `MethaneOfflineModel.__init__`:
- `knpp = 1e-2` — NPP scaling factor
- `q10 = 1.6` — Temperature sensitivity
- `tref = 273.16` — Reference temperature (0°C in Kelvin)

## Coordinate Conventions

TraCE data uses `(time, lat, lon)` ordering. The model internally works with `(lon, lat, time)` ordering — transpositions are applied in `main()` when loading data.

## Dependencies

Python: `numpy`, `xarray`, `matplotlib`. For notebook work, also `jupyter`.
