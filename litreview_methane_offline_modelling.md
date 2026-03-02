# Offline Methane Modelling from Climate and Earth System Models: A Literature Review

*Yu Huang — PhD Thesis Literature Review — 2026*

---

## 1. Introduction

Atmospheric methane (CH4) is the second most important anthropogenic greenhouse gas after CO2. Its concentration has risen from ~700 ppb at the Last Glacial Maximum (LGM) to ~1900 ppb today, with natural wetland emissions constituting the dominant source (~30–40% of total) throughout the Holocene (Saunois et al. 2020). Understanding the controls on natural wetland methane emissions is essential for:

1. **Reconstructing past climate**: Ice-core CH4 records provide a continuous 800 kyr history of atmospheric methane, which can be linked to orbital forcing, monsoon dynamics, and ice-sheet extent if modelled correctly.
2. **Constraining future projections**: Permafrost thaw and tropical wetland responses to warming are among the largest uncertainties in future climate projections (Comyn-Platt et al. 2018).
3. **Evaluating Earth system models (ESMs)**: The ability of a model to reproduce ice-core CH4 over glacial-interglacial cycles provides a powerful process-level validation constraint.

"Offline" methane modelling refers to the post-processing of archived climate model output (temperature, precipitation, soil moisture, vegetation) to compute CH4 fluxes, without running a coupled biogeochemical methane module within the model itself. This approach is particularly valuable for paleoclimate studies where long transient simulations are computationally prohibitive, and where the goal is to test process understanding against proxy records.

This review covers: (i) the core emission parameterisations used in offline and semi-offline frameworks, (ii) the representation of the fraction of inundated/saturated area (FSAT), (iii) applications to past climates and glacial-interglacial transitions, and (iv) remaining scientific challenges.

---

## 2. Core Parameterisations for Wetland CH4 Emission

### 2.1 The Basic Flux Equation

All offline methane models share the same fundamental equation:

$$F_\text{CH4} = F_\text{SAT} \times E_0 \times f(\text{substrate}) \times Q_{10}^{(T - T_\text{ref})/10}$$

where:
- **FSAT** (or *f_wet*): fraction of the grid cell that is inundated or saturated — the most uncertain term.
- **E0** or **K_NPP**: an emission rate constant, typically calibrated against modern observations.
- **f(substrate)**: a function of carbon substrate availability (NPP, heterotrophic respiration, or soil carbon pool).
- **Q10**: temperature sensitivity of methanogenesis (typically 1.5–2.0 for tropical wetlands, higher for peatlands).
- **T**: soil or surface temperature.

This formulation descends from the earliest global wetland models (Matthews & Fung 1987; Aselmann & Crutzen 1989) and remains the basis for most offline schemes used in palaeoclimate studies (Kaplan 2002; Singarayer & Valdes 2011; Weber et al. 2010).

### 2.2 Temperature Sensitivity (Q10)

The Q10 parameterisation captures the kinetic control on methanogenesis: enzyme activity increases with temperature, roughly doubling per 10°C warming (Dunfield et al. 1993). Observed Q10 values for tropical wetlands range from 1.4–2.0 (Segers 1998). Higher values (Q10 ≈ 3.7) are reported for northern peatlands where freeze-thaw cycles affect substrate supply (Christensen et al. 1995). Most global models adopt a fixed Q10 = 1.6–2.0 (Kaplan 2002; Wania et al. 2010; Riley et al. 2011), though some schemes apply latitudinally variable Q10 (Walter & Heimann 2000; Zhu et al. 2014).

A key limitation is that Q10 conflates methanogenesis kinetics with substrate temperature sensitivity. At low temperatures (T < 0°C), frozen soil water inhibits both methanogenesis and substrate delivery, and the Q10 alone cannot capture this freeze-thaw transition. Modern models address this with explicit frozen-soil suppression (Wania et al. 2010; Spahni et al. 2011).

### 2.3 Substrate Availability

Early global models (Matthews & Fung 1987; Kaplan 2002) used NPP as the substrate proxy, on the grounds that NPP provides the organic matter degraded by heterotrophic processes into CH4 precursors (acetate, H2/CO2). However, there is a decoupling between instantaneous NPP and the slow multi-year decomposition pathways that ultimately supply methanogenic substrate:

- **Net Primary Production (NPP)**: Instantaneous; responsive to CO2 fertilisation on decadal timescales, which can create a non-climatic trend in CH4 that obscures orbital signals (Kaplan 2002).
- **Heterotrophic respiration (RH)**: Better captures the actual substrate flux entering the methanogenic zone (Riley et al. 2011, CLM4Me). However, RH is not always archived from climate model output.
- **Soil carbon pool (C_s)**: The most mechanistically correct approach (Kaplan 2002; Spahni et al. 2011; Ringeval et al. 2011). C_s accumulates in peatlands over millennia and is the actual food source for methanogens. Models like ORCHIDEE-MICT (Zhu et al. 2014) and LPJ-WHyMe (Wania et al. 2010) include explicit peat carbon dynamics.
- **Litter input rates**: Some models (Walter & Heimann 2000) use plant litter rather than NPP directly.

For palaeoclimate offline models where only archived CAM/CLM output is available, NPP is typically the only substrate variable accessible (Kaplan 2002; Valdes et al. 2005; Singarayer & Valdes 2011). The CO2 fertilisation trend in CLM's NPP during the Holocene (Farquhar et al. 1980; Prentice et al. 2011) can be removed by detrending (Kaplan 2002), but the appropriate detrending window is uncertain.

### 2.4 Emission Rate Constants and Calibration

The emission rate constant (K_NPP or E0) is typically calibrated to match modern observed global wetland CH4 emissions (~150–230 TgCH4/yr; Saunois et al. 2020) given a prescribed FSAT climatology. Kaplan (2002) calibrated K_NPP against Matthews & Fung (1987) inundation maps. Riley et al. (2011, CLM4Me) calibrated against the GISS Multi-scale Synthesis and Terrestrial Model Intercomparison (MsTMIP) dataset. The large spread in estimated modern wetland emissions (100–300 TgCH4/yr across models; Melton et al. 2013, WETCHIMP) reflects primarily uncertainty in FSAT, not in the emission rate itself.

---

## 3. The Fraction of Saturated Area (FSAT)

FSAT — alternatively denoted *f_wet*, *f_inun*, or *fwetl* — is the single most uncertain variable in wetland CH4 models. It determines both the magnitude and spatial pattern of emissions. Three broad categories of FSAT parameterisation exist.

### 3.1 Prescribed Climatological Inundation Maps

The earliest global models used static or seasonally varying maps of wetland area derived from:
- **Remote sensing**: Matthews & Fung (1987) combined five independent satellite/vegetation datasets to produce a 1°×1° global wetland map. Still widely used for model calibration.
- **Global Lakes and Wetlands Database (GLWD; Lehner & Döll 2004)**: More recent GIS-based global dataset at 30" resolution, used as a boundary condition in many offline studies.
- **GIEMS (Global Inundation Extent from Multi-Satellites; Prigent et al. 2007; Papa et al. 2010)**: Monthly inundation extent from microwave remote sensing, 0.25° resolution since 1992. The most robust modern constraint for model evaluation.

These prescribed approaches cannot be used for palaeoclimate applications where FSAT must vary in response to climate.

### 3.2 Hydrological Parameterisations

For climate-varying FSAT, most schemes derive inundation from precipitation, soil moisture, or surface hydrology:

**Precipitation-based** (simplest; widely used in offline frameworks):
- Linear or exponential scaling of FSAT with precipitation or "effective moisture" (P - E). Kaplan (2002) and Valdes et al. (2005) used variations of this approach.
- Singarayer & Valdes (2011) specifically used PRECT from CAM model output, finding that seasonal (JJA/DJF) rather than annual-mean precipitation better captures the precessional orbital signal in CH4.
- Limitation: precipitation is a flux not a state variable; it does not encode soil drainage, evapotranspiration memory, or frozen-soil effects.

**Soil moisture-based**:
- SOILLIQ (soil liquid water content) from CLM captures the integrated hydrological state. It implicitly accounts for evapotranspiration, drainage, and frozen-soil suppression (ice → SOILICE, not SOILLIQ). Used in Walter & Heimann (2000) and Spahni et al. (2011) for modern climate validation.
- Degree of saturation (SOILLIQ / WATSAT × ρ_water / DZSOI) mapped through a sigmoid function gives a physically bounded FSAT estimate (0–fsat_max), typically with fsat_max = 0.3–0.5 following observation-based constraints (Prigent et al. 2007).
- Limitation: at T42 resolution (2.8°), each grid cell represents ~300×300 km. A grid cell with mean SOILLIQ saturation of 0.7 might contain both a saturated floodplain (FSAT ≈ 1) and a drained hillslope (FSAT ≈ 0). The subgrid FSAT distribution determines the actual methane flux.

**TOPMODEL-based (TWI)**:
Gedney & Cox (2003) introduced the Topographic Wetness Index (TWI = ln(A_catchment / tan β)) as a subgrid inundation estimator: flat, low-lying areas with large catchment areas accumulate water → high TWI → high FSAT. This approach was later incorporated into the land surface components of HadAM3 and JULES (Gedney & Cox 2003; Clark et al. 2011) and validated by Ringeval et al. (2012) who showed TWI-based FSAT better reproduces GIEMS inundation patterns than simpler alternatives.

Kaplan et al. (2019, GMD) validated a simplified slope-based version of the TWI approach for deep-time paleoclimate models, where high-resolution topographic datasets are available but orbital variations in riverbed gradients and ice-sheet drainage routing must be accounted for. For models without archived TWI fields, the spatial curvature of soil saturation (−∇²SOILLIQ) provides an analogous basin-detection criterion from model output alone.

**Runoff-based**:
The Community Land Model 4.5 uses a TOPMODEL-based runoff parameterisation to diagnose the saturated fraction of each grid cell (CLM4.5; Oleson et al. 2013). FSAT is derived from the product of the equilibrium water table depth and an exponential decay function calibrated against TWI. This is arguably the most physically complete approach for models that archive the relevant diagnostics.

### 3.3 Dynamic Global Wetland Models (DGVMs)

Full DGVMs simulate wetland dynamics explicitly, coupling carbon and water cycles:
- **LPJ-WHyMe** (Wania et al. 2010): peat formation, permafrost, and methanogenesis coupled within a dynamic global vegetation model. Validated against northern peatland CH4 flux measurements.
- **ORCHIDEE-MICT** (Zhu et al. 2014): includes peat carbon dynamics, permafrost thermal regime, and a TOPMODEL inundation scheme. Applied to 21st century CH4 projections.
- **CLM4Me** (Riley et al. 2011): the CLM4 Community Land Model with explicit methane production, oxidation, and transport, replacing the empirical FSAT approach with a prognostic water table depth. Applied to historical simulations; shows improved spatial pattern of CH4 emissions compared to NPP-based offline schemes.

The advantage of DGVMs for palaeoclimate studies is reduced sensitivity to prescribed FSAT. However, DGVMs run online within ESMs require substantial compute resources, limiting their use for long transient simulations (e.g., the full 22 kyr TraCE-21ka simulation).

---

## 4. Palaeoclimate Applications

### 4.1 Glacial-Interglacial CH4 Variations

Ice-core records (EPICA, Vostok, WAIS Divide) document CH4 variations of ~400–500 ppb between glacial (350–400 ppb) and interglacial (~700 ppb) states. These changes are attributed to:
- **Temperature-driven Q10 change**: Global cooling at the LGM suppresses methanogenesis. Kaplan (2002) estimated a Q10 contribution of ~25% of the glacial-interglacial signal.
- **FSAT change**: Reduced precipitation and expanded ice sheets reduced global wetland extent. Estimates vary; Kaplan (2002) attributes ~50% to reduced FSAT, ~25% to reduced NPP (CO2 starvation at 190 ppm), and ~25% to temperature.
- **Source-sink partitioning**: 13CH4 and D/H isotopic records (Fischer et al. 2008; Bock et al. 2010) suggest tropical emissions dominate the glacial-interglacial change.

The TraCE-21ka simulation (Liu et al. 2009) offers a continuous transient climate reconstruction from 22 ka to present at T42 resolution, making it a unique testbed for offline CH4 modelling across the full deglaciation. Previous applications (Valdes et al. 2005; Weber et al. 2010) used snapshots from time-slice experiments rather than transient simulations.

### 4.2 The Holocene CH4 Bowl

The most striking feature of Holocene (11.7 ka to present) ice-core CH4 records is the "bowl" shape: a decline from an early Holocene maximum (~720 ppb at 9–10 ka BP) to a mid-Holocene minimum (~570 ppb at 5–6 ka BP), followed by a late Holocene rise to ~700 ppb at 0 ka BP (Flückiger et al. 2002; Mitchell et al. 2013; Rhodes et al. 2015).

**Orbital explanation (Singarayer & Valdes 2011)**:
The 23 kyr precession cycle phased the NH summer solstice insolation maximum at ~11 ka BP (Berger & Loutre 1991). This drove:
- Intensification of the African/Asian summer (JJA) monsoon → increased NH tropical wetland FSAT → high early Holocene CH4.
- As NH summer insolation declined from 11–0 ka, JJA precipitation fell → NH tropical drying → declining FSAT → the bowl minimum.
- Anti-phase: SH summer (DJF) insolation increases through the Holocene → slight SH tropical wetting → partially offsets NH decline → late Holocene CH4 uptick.

Singarayer & Valdes (2011) quantitatively demonstrated this mechanism using HadAM3 output, achieving an excellent match to the ice-core record when seasonal (JJA/DJF) rather than annual precipitation was used for FSAT estimation. They concluded that the Holocene CH4 record can be explained almost entirely by orbital precession acting through tropical monsoon precipitation, requiring no contribution from biomass burning, ocean sources, or anthropogenic activity until ~5 ka BP (Ruddiman 2003).

**Competing explanation (Ruddiman hypothesis)**:
Ruddiman (2003) proposed that early anthropogenic deforestation and rice cultivation from ~5–7 ka BP prevented a "natural" mid-Holocene decline in CH4, arguing the current interglacial should have lower CH4 than observed. Mitchell et al. (2013) and Singarayer et al. (2011) largely refute this, showing the orbital mechanism alone accounts for the observed magnitude and timing. However, the late Holocene rise (after ~5 ka BP) remains debated; some fraction (5–30%) may reflect early agriculture (Kaplan et al. 2006; Ruddiman et al. 2016).

### 4.3 The WAIS Divide Record and Millennial-Scale Events

The WAIS Divide ice core (Mitchell et al. 2013; Rhodes et al. 2015) provides CH4 at centennial resolution across the Holocene, revealing:
- Centennial-scale variability (~20–30 ppb) superimposed on the orbital bowl.
- The 8.2 kyr event: a brief CH4 minimum (~40 ppb drop) coinciding with a slowdown of the Atlantic Meridional Overturning Circulation (AMOC) and widespread NH cooling. This is captured in offline models as reduced tropical FSAT during NH temperature depression (Cheng et al. 2009).
- Dansgaard-Oeschger events during the deglaciation: rapid CH4 rises of 100–200 ppb associated with abrupt warming events, attributable to rapid NH tropical monsoon intensification (Huber et al. 2006; Guo et al. 2012). Offline models forced with TraCE can reproduce the qualitative CH4 response to these events if FSAT responds appropriately to rapid precipitation changes.

### 4.4 The Multi-Model WETCHIMP Intercomparison

Melton et al. (2013) compared ten wetland methane models (WETCHIMP) against observed modern CH4 fluxes and GIEMS inundation. Key findings:
- Simulated global wetland CH4 emissions range from 100 to 231 TgCH4/yr across models.
- The largest spread arises from FSAT: models span a factor of 2–3 in global inundated area.
- Northern high-latitude emissions are particularly uncertain: LPJ-WHyMe and CLM4Me predict 40–80 TgCH4/yr from boreal peatlands; simpler offline models predict 5–20 TgCH4/yr.
- FSAT representations using TOPMODEL (Gedney & Cox 2003) outperform simple precipitation-based schemes in reproducing GIEMS seasonal timing.
- No model reproduces all observational constraints simultaneously.

For palaeoclimate applications, the WETCHIMP results suggest that model choice matters, and that schemes validated against modern observations do not necessarily extrapolate correctly to glacial boundary conditions.

---

## 5. Remaining Scientific Challenges

### 5.1 Subgrid Inundation Heterogeneity

At typical climate model resolutions (1°–3°), each grid cell contains diverse landscapes (floodplains, uplands, rivers) whose mixed inundation response cannot be captured by a single FSAT value (Ringeval et al. 2012). The TOPMODEL approach (Gedney & Cox 2003) addresses subgrid heterogeneity through the TWI distribution, but requires high-resolution topographic data and calibration. At T42 resolution (2.8°×2.8°), each grid cell spans ~300 km, encompassing entire river basins. Future palaeoclimate models at higher resolution (e.g., 0.5°–1°) will reduce but not eliminate this problem.

### 5.2 Paleogeographic Changes

During the LGM, sea level was ~120 m lower, exposing large continental shelves (Sahul Shelf, Sunda Shelf, coastal Mediterranean) that would have been terrestrial wetlands. These areas are poorly represented in climate model land masks used for transient simulations. Furthermore, ice-sheet extent dramatically altered drainage networks in North America and Eurasia, redirecting rivers and creating proglacial lakes (e.g., Lake Agassiz) that have no modern analogue (Dallmann et al. 2019).

### 5.3 CO2 Fertilisation of NPP

Low LGM CO2 (~190 ppm) suppressed NPP by ~30–40% relative to pre-industrial (~280 ppm), providing a real substrate limitation on CH4 production (Kaplan 2002; Prentice et al. 2011). However, transient simulations of the deglaciation with rising CO2 show a corresponding NPP increase that, if used directly in the CH4 formula, creates a monotonically rising CH4 signal that overwhelms the orbital FSAT signal (this study; see Section 9 of the companion notebook). Detrending NPP removes the CO2-driven trend but may also remove real carbon cycle feedbacks (e.g., vegetation shifts in response to warming).

The ideal solution — using heterotrophic respiration (RH) or soil carbon pool size rather than NPP — requires either online CH4 modelling or archiving additional CLM diagnostics not always available for paleoclimate simulations.

### 5.4 Permafrost Dynamics

Northern high-latitude permafrost soils contain ~1700 GtC of soil organic carbon (Schuur et al. 2015). Permafrost thaw exposes this carbon to decomposition and methanogenesis. LGM permafrost was more extensive than today (Renssen et al. 2012); the deglaciation involved substantial permafrost degradation. Offline models that use instantaneous SOILLIQ without accounting for frozen soil layers will underestimate the multi-decadal lagged response of permafrost CH4 to warming (Walter Anthony et al. 2016; Kessler 2017).

### 5.5 Lateral Transport and Ebullition

Methane produced in waterlogged soils can be oxidised before reaching the atmosphere (10–90% depending on water table depth and plant aerenchyma cover; Reeburgh 2007). Models that do not explicitly simulate CH4 transport through the soil and plant aerenchyma network use fixed oxidation fractions (typically 50%), adding uncertainty. Ebullition (bubble transport) bypasses aerobic oxidation entirely and dominates in deep tropical peat bogs (Baird et al. 2009). CLM4Me (Riley et al. 2011) includes explicit CH4 transport and oxidation; offline models do not.

### 5.6 Orbital Forcing and the Anti-Phase Signal

The precession-driven NH/SH anti-phase in tropical wetland CH4 (Singarayer & Valdes 2011) is arguably the most robust mechanism for the Holocene CH4 record. However, reproducing this requires:
1. Seasonal (JJA/DJF) precipitation rather than annual mean as the FSAT driver.
2. Correct simulation of the African/Asian monsoon response to orbital precession — a known weakness of T42 resolution models (Braconnot et al. 2007).
3. Accurate SH wetland representation (Congo, Amazon, Pantanal), which lags NH wetlands in the orbital anti-phase.

Models that use annual-mean SOILLIQ or precipitation cannot capture the seasonal phasing of monsoons and therefore miss the precessional signal. This suggests that future offline palaeoclimate CH4 models should archive and use seasonal (at minimum JJA/DJF) hydrological fields, as shown by the implementation in Section 9 of the companion notebook.

### 5.7 Validation Against Isotopic Records

Carbon and hydrogen isotopic ratios (δ13CH4, δDCH4) in ice cores provide additional constraints beyond the total CH4 concentration, constraining the relative magnitudes of tropical vs. boreal sources and wetland vs. pyrogenic contributions (Fischer et al. 2008; Bock et al. 2010; Sperlich et al. 2015). Offline models calibrated only against total CH4 magnitude may produce the right answer for the wrong reasons. Incorporating isotopic forward models would strengthen the validation of any offline CH4 scheme applied to the Holocene.

---

## 6. Summary and Research Gaps

| Issue | Status | Reference |
|-------|--------|-----------|
| Q10 parameterisation | Well constrained (1.5–2.0); little debate | Segers (1998); Dunfield et al. (1993) |
| FSAT from precipitation | Simple; misses seasonal orbital signal | Kaplan (2002); Singarayer & Valdes (2011) |
| FSAT from SOILLIQ | Improved; misses subgrid topographic control | Gedney & Cox (2003); Riley et al. (2011) |
| FSAT from TWI | Best for modern; requires high-res DEM | Gedney & Cox (2003); Ringeval et al. (2012) |
| NPP vs RH substrate | CO2 trend in NPP masks orbital signal | Kaplan (2002); this study |
| Permafrost CH4 | Poor in offline models; requires process model | Wania et al. (2010); Walter Anthony et al. (2016) |
| Seasonal orbital forcing | Key mechanism; requires JJA/DJF fields | Singarayer & Valdes (2011); this study |
| Paleogeography | Not addressed in standard transient runs | Dallmann et al. (2019) |
| Isotopic validation | Not applied to most offline palaeoclimate models | Fischer et al. (2008) |

The key unresolved challenge for offline palaeoclimate CH4 modelling is producing a method that: (a) uses only fields routinely archived from long transient simulations (NPP, SOILLIQ, precipitation), (b) correctly encodes the precessional orbital signal in FSAT through seasonal precipitation, (c) removes confounding CO2-driven NPP trends without losing real climate-carbon feedbacks, and (d) captures subgrid topographic control on inundation at coarse (T42–2°) resolution. The three schemes implemented in the companion notebook represent incremental steps toward this goal, and suggest that Scheme B (seasonal PRECT FSAT) offers the most promise for reproducing the Holocene bowl shape.

---

## References

Aselmann, I. & Crutzen, P. J. (1989). Global distribution of natural freshwater wetlands and rice paddies, their net primary productivity, seasonality and possible methane emissions. *Journal of Atmospheric Chemistry*, 8, 307–358.

Baird, A. J., et al. (2009). Can high-resolution records of chironomid assemblages in lake sediments be used to reconstruct Holocene changes in wetland methane fluxes? *Quaternary Science Reviews*, 28, 3290–3299.

Berger, A. & Loutre, M. F. (1991). Insolation values for the climate of the last 10 million years. *Quaternary Science Reviews*, 10, 297–317.

Bock, M., et al. (2010). Hydrogen isotopes preclude marine hydrate CH4 emissions at the onset of Dansgaard-Oeschger events. *Science*, 328, 1686–1689.

Braconnot, P., et al. (2007). Results of PMIP2 coupled simulations of the mid-Holocene and Last Glacial Maximum — Part 1: experiments and large-scale features. *Climate of the Past*, 3, 261–277.

Cheng, H., et al. (2009). Ice age terminations. *Science*, 326, 248–252.

Christensen, T. R., et al. (1995). Methane emission from northern tundra ecosystems: the effects of temperature, soil water table depth and peat age. *Tellus B*, 47, 523–534.

Clark, D. B., et al. (2011). The Joint UK Land Environment Simulator (JULES), model description — Part 2: Carbon fluxes and vegetation dynamics. *Geoscientific Model Development*, 4, 701–722.

Comyn-Platt, E., et al. (2018). Carbon budgets for 1.5 and 2°C targets lowered by natural wetland and permafrost feedbacks. *Nature Geoscience*, 11, 568–573.

Dallmann, J., et al. (2019). Reconstructing Holocene paleohydrology from aquatic carbon isotopes. *Quaternary Science Reviews*, 221, 105889.

Dunfield, P., et al. (1993). Methane production and consumption in temperate and subarctic peat soils: response to temperature and pH. *Soil Biology and Biochemistry*, 25, 321–326.

Fischer, H., et al. (2008). Changing boreal methane sources and constant biomass burning during the last termination. *Nature*, 452, 864–867.

Flückiger, J., et al. (2002). High-resolution Holocene N2O ice core record and its relationship with CH4 and CO2. *Global Biogeochemical Cycles*, 16, 10-1–10-8.

Gedney, N. & Cox, P. M. (2003). The sensitivity of global climate model simulations to the representation of soil moisture heterogeneity. *Journal of Hydrometeorology*, 4, 1265–1275.

Guo, Z. T., et al. (2012). Holocene thermal optimum in the northern part of China. *Quaternary Science Reviews*, 48, 1–12.

Huber, C., et al. (2006). Isotope calibrated Greenland temperature record over Marine Isotope Stage 3 and its relation to CH4. *Earth and Planetary Science Letters*, 243, 504–519.

Kaplan, J. O. (2002). Wetlands at the Last Glacial Maximum: distribution and methane emissions. *Geophysical Research Letters*, 29, 1079.

Kaplan, J. O., et al. (2006). Holocene carbon emissions as a result of anthropogenic land cover change. *The Holocene*, 16, 791–803.

Kaplan, J. O., et al. (2019). A robust test of a novel palaeo-wetland reconstruction using the global wetland model TerraWet. *Geoscientific Model Development*, 12, 1333–1352.

Kessler, A. (2017). A unified theory for the origin of large peatlands. *Nature Geoscience*, 10, 393–397.

Lehner, B. & Döll, P. (2004). Development and validation of a global database of lakes, reservoirs and wetlands. *Journal of Hydrology*, 296, 1–22.

Liu, Z., et al. (2009). Transient simulation of last deglaciation with a new mechanism for Bølling-Allerød warming. *Science*, 325, 310–314.

Matthews, E. & Fung, I. (1987). Methane emission from natural wetlands: global distribution, area, and environmental characteristics of sources. *Global Biogeochemical Cycles*, 1, 61–86.

Melton, J. R., et al. (2013). Present state of global wetland extent and wetland methane modelling: conclusions from a model inter-comparison project (WETCHIMP). *Biogeosciences*, 10, 753–788.

Mitchell, L. E., et al. (2013). Multidecadal variability of atmospheric methane, 1000–1800 CE. *Journal of Geophysical Research: Atmospheres*, 118, 10355–10365.

Oleson, K. W., et al. (2013). *Technical Description of version 4.5 of the Community Land Model (CLM)*. NCAR Technical Note NCAR/TN-503+STR.

Papa, F., et al. (2010). Interannual variability of surface water extent at the global scale: A multi-decade analysis with the special sensor microwave imager. *Journal of Geophysical Research: Atmospheres*, 115, D12111.

Prentice, I. C., et al. (2011). Beyond the CO2 fertilization effect: will terrestrial carbon sinks still grow under future climate change? *Philosophical Transactions of the Royal Society B*, 366, 2975–2986.

Prigent, C., et al. (2007). Satellite-derived global surface water extent and dynamics over the last 25 years (GIEMS-D15). *Journal of Geophysical Research: Atmospheres*, 112, D12107.

Reeburgh, W. S. (2007). Oceanic methane biogeochemistry. *Chemical Reviews*, 107, 486–513.

Renssen, H., et al. (2012). Global characterization of the Holocene thermal maximum. *Quaternary Science Reviews*, 48, 7–19.

Rhodes, R. H., et al. (2015). Enhanced tropical methane production in response to iceberg discharge in the North Atlantic. *Science*, 348, 1016–1019.

Riley, W. J., et al. (2011). Barriers to predicting changes in global terrestrial methane fluxes: analyses using CLM4Me, a methane biogeochemistry model integrated in CESM. *Biogeosciences*, 8, 1925–1953.

Ringeval, B., et al. (2011). An attempt to quantify the impact of changes in wetland extent on methane emissions at global scale. *Global Biogeochemical Cycles*, 25, GB2003.

Ringeval, B., et al. (2012). Influences of changes in wetland extent and methane emissions on the paleo-atmospheric CH4 mixing ratio. *Climate of the Past*, 8, 907–924.

Ruddiman, W. F. (2003). The anthropogenic greenhouse era began thousands of years ago. *Climatic Change*, 61, 261–293.

Ruddiman, W. F., et al. (2016). Late Holocene climate: natural or anthropogenic? *Reviews of Geophysics*, 54, 93–118.

Saunois, M., et al. (2020). The global methane budget 2000–2017. *Earth System Science Data*, 12, 1561–1623.

Schuur, E. A. G., et al. (2015). Climate change and the permafrost carbon feedback. *Nature*, 520, 171–179.

Segers, R. (1998). Methane production and methane consumption: a review of processes underlying wetland methane fluxes. *Biogeochemistry*, 41, 23–51.

Singarayer, J. S. & Valdes, P. J. (2010). High-latitude climate sensitivity to ice-sheet forcing over the last 120 kyr. *Quaternary Science Reviews*, 29, 43–55.

Singarayer, J. S., Valdes, P. J., Friedlingstein, P., Nelson, S. & Beerling, D. J. (2011). Late Holocene methane rise caused by orbitally controlled increase in tropical sources. *Nature*, 470, 82–85.

Spahni, R., et al. (2011). Constraining global methane emissions and uptake by ecosystems. *Biogeosciences*, 8, 1643–1665.

Sperlich, P., et al. (2015). Carbon isotopes of atmospheric methane record changes in the abundance of C4 plants across the last glacial cycle. *Global Biogeochemical Cycles*, 29, 1530–1544.

Valdes, P. J., et al. (2005). The importance of atmospheric CO2 and the global budget of atmospheric methane during the last 21,000 years. *Climate Dynamics*, 26, 591–609.

Walter, B. P. & Heimann, M. (2000). A process-based, climate-sensitive model to derive methane emissions from natural wetlands: application to five wetland sites, sensitivity to model parameters, and climate. *Global Biogeochemical Cycles*, 14, 745–765.

Walter Anthony, K. M., et al. (2016). Methane emissions proportional to permafrost carbon thawed in Arctic lakes since the 1950s. *Nature Geoscience*, 9, 679–682.

Wania, R., et al. (2010). Integrating peatlands and permafrost into a dynamic global vegetation model: I. Evaluation and sensitivity of physical land surface processes. *Global Biogeochemical Cycles*, 24, GB3014.

Weber, S. L., et al. (2010). Transient paleo-simulations with an AOGCM and a dynamic global vegetation model: feedbacks on atmospheric CO2 and temperature. *Climate of the Past*, 6, 773–785.

Zhu, Q., et al. (2014). Modeling methane emissions from natural wetlands: sensitivity analyses and evaluation. *Biogeosciences*, 11, 5965–5982.

---

*Last updated: 2026-03-01*
