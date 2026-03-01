#!/usr/bin/env python
"""
Offline methane model for TraCE transient climate simulation.
Computes methane flux from temperature, precipitation, and NPP 
following the approach: F_CH4 = FSAT * Knpp * NPP * Q10^((T - Tref)/10) * 365

Author: Yu Huang
Date: 2026-02-19
"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from pathlib import Path


class MethaneOfflineModel:
    """
    Offline methane flux model for paleoclimate simulations.
    """
    
    def __init__(self, knpp=1e-2, q10=1.6, tref=273.16):
        """
        Initialize methane model parameters.
        
        Parameters:
        -----------
        knpp : float
            NPP scaling factor (default: 1e-2)
        q10 : float
            Temperature sensitivity factor (default: 1.6)
        tref : float
            Reference temperature in Kelvin (default: 273.16, i.e., 0°C)
        """
        self.knpp = knpp
        self.q10 = q10
        self.tref = tref
        
    def compute_grid_area(self, lat, lon):
        """
        Compute grid cell area for each lat/lon cell.
        
        Parameters:
        -----------
        lat : array-like
            Latitude array (degrees)
        lon : array-like
            Longitude array (degrees)
            
        Returns:
        --------
        area : ndarray
            Grid cell area in m^2 (lon × lat)
        """
        R = 6371000  # Earth radius in meters
        
        # Calculate grid spacing
        dlat = np.abs(lat[1] - lat[0]) if len(lat) > 1 else 1.0
        dlon = np.abs(lon[1] - lon[0]) if len(lon) > 1 else 1.0
        
        # Create meshgrid
        lon_grid, lat_grid = np.meshgrid(lon, lat)
        
        # Calculate area for each grid cell
        area = 2 * np.pi * R**2 * \
               (np.sin(np.deg2rad(lat_grid + dlat/2)) - 
                np.sin(np.deg2rad(lat_grid - dlat/2))) * \
               dlon / 360
        
        # Transpose to match (lon, lat) ordering
        return area.T
    
    def estimate_fsat_from_precip(self, precip, temp, method='linear'):
        """
        Estimate fraction of saturated area (FSAT) from precipitation.
        This is a simplified parameterization since TraCE doesn't have FSAT output.
        
        Parameters:
        -----------
        precip : ndarray
            Precipitation (mm/day or m/s)
        temp : ndarray
            Temperature (K)
        method : str
            Method for estimation ('linear', 'threshold', 'exponential')
            
        Returns:
        --------
        fsat : ndarray
            Estimated fraction of saturated area (0-1)
        """
        if method == 'linear':
            # Simple linear scaling with precipitation
            # Normalize precipitation to 0-1 range (rough estimate)
            precip_norm = np.clip(precip / np.percentile(precip[precip > 0], 95), 0, 1)
            fsat = 0.1 + 0.3 * precip_norm  # Base 0.1, up to 0.4 max
            
        elif method == 'threshold':
            # Threshold-based approach
            # High precipitation and moderate temps -> high FSAT
            fsat = np.zeros_like(precip)
            fsat[precip > np.percentile(precip[precip > 0], 75)] = 0.3
            fsat[(precip > np.percentile(precip[precip > 0], 50)) & 
                 (precip <= np.percentile(precip[precip > 0], 75))] = 0.2
            fsat[(precip > 0) & (precip <= np.percentile(precip[precip > 0], 50))] = 0.1
            
        elif method == 'exponential':
            # Exponential relationship
            precip_norm = precip / np.mean(precip[precip > 0])
            fsat = 0.05 + 0.35 * (1 - np.exp(-precip_norm))
        
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Apply temperature constraint (reduce FSAT if too cold)
        temp_factor = np.clip((temp - 273.16) / 15, 0, 1)  # Reduce below 0°C
        fsat = fsat * temp_factor
        
        return np.clip(fsat, 0, 1)
    
    def compute_methane_flux(self, npp, temp, fsat=None, precip=None, 
                            fsat_method='linear'):
        """
        Compute methane flux from NPP, temperature, and saturated fraction.
        
        Parameters:
        -----------
        npp : ndarray
            Net Primary Production (gC/m2/s or similar units)
        temp : ndarray
            Soil/surface temperature (K)
        fsat : ndarray, optional
            Fraction of saturated area (0-1). If None, will estimate from precip.
        precip : ndarray, optional
            Precipitation (needed if fsat is None)
        fsat_method : str
            Method for estimating FSAT if not provided
            
        Returns:
        --------
        f_ch4 : ndarray
            Methane flux (gC/m2/yr)
        """
        # Estimate FSAT if not provided
        if fsat is None:
            if precip is None:
                raise ValueError("Either fsat or precip must be provided")
            fsat = self.estimate_fsat_from_precip(precip, temp, method=fsat_method)
        
        # Compute methane flux
        # F_CH4 = FSAT * Knpp * NPP * Q10^((T - Tref)/10)
        # Note: If NPP is already in gC/m2/yr, do NOT multiply by 365
        # The *365 is only needed if NPP is in gC/m2/day
        temp_factor = self.q10 ** ((temp - self.tref) / 10)
        f_ch4 = fsat * self.knpp * npp * temp_factor
        
        return f_ch4
    
    def compute_global_emissions(self, f_ch4, area):
        """
        Compute global methane emissions from flux and area.
        
        Parameters:
        -----------
        f_ch4 : ndarray
            Methane flux (gC/m2/yr)
        area : ndarray
            Grid cell area (m2)
            
        Returns:
        --------
        emissions : float or ndarray
            Total emissions (TgCH4/yr) - scalar if 2D input, array if 3D
        """
        # Convert gC to gCH4 (molecular weight ratio: 16/12)
        ch4_mass_factor = 16 / 12
        
        # Sum over spatial dimensions
        if f_ch4.ndim == 3:  # (lon, lat, time)
            # Expand area to match time dimension
            area_3d = np.broadcast_to(area[:, :, np.newaxis], f_ch4.shape)
            emissions = np.sum(f_ch4 * area_3d, axis=(0, 1))
        else:  # 2D (lon, lat)
            emissions = np.sum(f_ch4 * area)
        
        # Convert from gCH4/yr to TgCH4/yr
        emissions = emissions * ch4_mass_factor / 1e12
        
        return emissions


def load_trace_data(data_dir='.'):
    """
    Load TraCE simulation data from NetCDF files.
    
    Parameters:
    -----------
    data_dir : str or Path
        Directory containing the NetCDF files
        
    Returns:
    --------
    datasets : dict
        Dictionary containing loaded datasets
    """
    data_dir = Path(data_dir)
    datasets = {}
    
    # Load NPP data
    npp_file = data_dir / 'trace.01-36.22000BP.clm2.NPP.22000BP_decavg_400BCE.nc'
    if npp_file.exists():
        print(f"Loading NPP data from {npp_file.name}...")
        datasets['npp'] = xr.open_dataset(npp_file)
    else:
        # Try parent directory
        npp_file = data_dir.parent / npp_file.name
        if npp_file.exists():
            print(f"Loading NPP data from {npp_file.name}...")
            datasets['npp'] = xr.open_dataset(npp_file)
        else:
            print(f"Warning: NPP file not found")
    
    # Load precipitation data
    precip_file = data_dir / 'trace.01-36.22000BP.cam2.PRECT.22000BP_decavg_400BCE.nc'
    if precip_file.exists():
        print(f"Loading precipitation data from {precip_file.name}...")
        datasets['precip'] = xr.open_dataset(precip_file)
    else:
        print(f"Warning: Precipitation file not found")
    
    # Load temperature data
    temp_file = data_dir / 'trace.01-36.22000BP.cam2.T.22000BP_decavg_400BCE.nc'
    if temp_file.exists():
        print(f"Loading temperature data from {temp_file.name}...")
        datasets['temp'] = xr.open_dataset(temp_file)
    else:
        print(f"Warning: Temperature file not found")
    
    return datasets


def main():
    """
    Main function to run the methane offline model.
    """
    print("=" * 60)
    print("TraCE Offline Methane Model")
    print("=" * 60)
    
    # Load data
    data_dir = Path(__file__).parent
    datasets = load_trace_data(data_dir)
    
    if not datasets:
        print("Error: No data files found!")
        return
    
    # Initialize model
    model = MethaneOfflineModel(knpp=1e-2, q10=1.6, tref=273.16)
    
    # Extract data
    if 'npp' in datasets:
        ds_npp = datasets['npp']
        npp_data = ds_npp['NPP'].values  # Should be in gC/m2/s
        lat = ds_npp['lat'].values
        lon = ds_npp['lon'].values
        time = ds_npp['time'].values
        
        print(f"\nNPP data shape: {npp_data.shape}")
        print(f"Lat range: {lat.min():.2f} to {lat.max():.2f}")
        print(f"Lon range: {lon.min():.2f} to {lon.max():.2f}")
        print(f"Time steps: {len(time)}")
    else:
        print("Error: NPP data required!")
        return
    
    # Get temperature (use surface temp as proxy for soil temp)
    if 'temp' in datasets:
        ds_temp = datasets['temp']
        # Assuming lowest level or surface temperature
        temp_var = list(ds_temp.data_vars)[0]
        temp_data = ds_temp[temp_var].values
        
        # Handle different dimensions
        if temp_data.ndim == 4:  # (time, lev, lat, lon)
            temp_data = temp_data[:, -1, :, :]  # Take lowest level
            temp_data = np.transpose(temp_data, (2, 1, 0))  # -> (lon, lat, time)
        elif temp_data.ndim == 3:  # (time, lat, lon)
            temp_data = np.transpose(temp_data, (2, 1, 0))  # -> (lon, lat, time)
        
        print(f"Temperature data shape: {temp_data.shape}")
    else:
        print("Warning: Using default temperature (288 K)")
        temp_data = np.ones_like(npp_data) * 288
    
    # Get precipitation
    if 'precip' in datasets:
        ds_precip = datasets['precip']
        precip_var = list(ds_precip.data_vars)[0]
        precip_data = ds_precip[precip_var].values
        
        # Handle dimensions
        if precip_data.ndim == 3:  # (time, lat, lon)
            precip_data = np.transpose(precip_data, (2, 1, 0))  # -> (lon, lat, time)
        
        print(f"Precipitation data shape: {precip_data.shape}")
    else:
        precip_data = None
    
    # Compute grid cell area
    print("\nComputing grid cell areas...")
    area = model.compute_grid_area(lat, lon)
    print(f"Total Earth surface area: {area.sum() / 1e12:.2f} million km²")
    
    # Compute methane flux
    print("\nComputing methane flux...")
    f_ch4 = model.compute_methane_flux(
        npp=npp_data,
        temp=temp_data,
        precip=precip_data,
        fsat_method='linear'
    )
    
    print(f"Methane flux shape: {f_ch4.shape}")
    print(f"Methane flux range: {f_ch4.min():.2e} to {f_ch4.max():.2e} gC/m2/yr")
    
    # Compute global emissions
    print("\nComputing global methane emissions...")
    emissions = model.compute_global_emissions(f_ch4, area)
    
    print(f"\nGlobal methane emissions time series:")
    print(f"Mean: {emissions.mean():.2f} TgCH4/yr")
    print(f"Range: {emissions.min():.2f} to {emissions.max():.2f} TgCH4/yr")
    
    # Create output dataset
    print("\nCreating output dataset...")
    ds_out = xr.Dataset(
        data_vars={
            'F_CH4': (['lon', 'lat', 'time'], f_ch4,
                     {'units': 'gC/m2/yr', 
                      'long_name': 'Methane flux'}),
            'CH4_emissions': (['time'], emissions,
                             {'units': 'TgCH4/yr',
                              'long_name': 'Global methane emissions'}),
            'area': (['lon', 'lat'], area,
                    {'units': 'm2',
                     'long_name': 'Grid cell area'})
        },
        coords={
            'lon': lon,
            'lat': lat,
            'time': time
        },
        attrs={
            'title': 'Offline methane model output from TraCE simulation',
            'model_parameters': f'Knpp={model.knpp}, Q10={model.q10}, Tref={model.tref}',
            'created': '2026-02-19'
        }
    )
    
    # Save output
    output_file = data_dir / 'trace_methane_offline_output.nc'
    print(f"\nSaving output to {output_file.name}...")
    ds_out.to_netcdf(output_file)
    
    # Create simple plot
    print("\nCreating diagnostic plots...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Time series of global emissions
    ax = axes[0, 0]
    ax.plot(range(len(emissions)), emissions, 'b-', linewidth=2)
    ax.set_xlabel('Time step')
    ax.set_ylabel('CH4 emissions (TgCH4/yr)')
    ax.set_title('Global Methane Emissions')
    ax.grid(True, alpha=0.3)
    
    # Spatial pattern (time average)
    ax = axes[0, 1]
    f_ch4_mean = np.mean(f_ch4, axis=2)
    im = ax.pcolormesh(lon, lat, f_ch4_mean.T, shading='auto', cmap='YlOrRd')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Mean Methane Flux')
    plt.colorbar(im, ax=ax, label='gC/m2/yr')
    
    # Latitudinal distribution
    ax = axes[1, 0]
    f_ch4_zonal = np.mean(f_ch4_mean, axis=0)
    ax.plot(lat, f_ch4_zonal, 'g-', linewidth=2)
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Zonal mean flux (gC/m2/yr)')
    ax.set_title('Latitudinal Distribution')
    ax.grid(True, alpha=0.3)
    
    # Histogram
    ax = axes[1, 1]
    ax.hist(f_ch4.flatten(), bins=50, edgecolor='black', alpha=0.7)
    ax.set_xlabel('Methane flux (gC/m2/yr)')
    ax.set_ylabel('Frequency')
    ax.set_title('Flux Distribution')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plot_file = data_dir / 'trace_methane_diagnostics.png'
    plt.savefig(plot_file, dpi=150, bbox_inches='tight')
    print(f"Saved diagnostics plot to {plot_file.name}")
    
    print("\n" + "=" * 60)
    print("Methane model run complete!")
    print("=" * 60)
    
    # Close datasets
    for ds in datasets.values():
        ds.close()


if __name__ == '__main__':
    main()
