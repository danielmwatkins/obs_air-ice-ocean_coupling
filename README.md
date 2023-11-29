# Observations of the air-sea ice-ocean response to a winter cyclone

This repository contains the code to reproduce the analysis of sea ice motion and storm structure. The scripts can be divided into code for obtaining and preparing the data and code for carrying out the analysis of the data. Code is subject to change! 

Key data components
1. Drifting buoy dataset
2. Meteorological data from flux towers and sleds
3. Meteorological data from ERA5 reanalysis
4. Sea ice concentration from AMSR Unified 12 km

## Parameter files
* `array_info.csv` Table containing the buoys used in the deformation arrays, and the color scheme.
* `buoy_info.csv`. TBD table with the buoy parameters, used to make table for manuscript.

## Utilities
* `drifter.py` Functions for processing the drifting buoy data

## Preparing data
* `prepare_buoy_data.py` Applies `standard_qc` and `interpolate_buoy_track` funtions from the `drifter.py` file to the MOSAiC buoy data files from the Arctic Data Center. Trajectories are then saved to the folder `data/interpolated_tracks/`.
* `prepare_era_data.py` Downloads ERA5 data from 1/25 to 2/05 and saves it, then uses xesmf to regrid onto the NSIDC polar stereographic grid.
* `compile_amsr.py` Reads in the daily 12 km AMSR data obtained from NSIDC and compiles the files into a single netcdf file.
* `compile_met_data.py` Produces CSV files of the Met City and ASFS datasets

## Calculations
* calculate_deformation.py
    - depends on array_info
* calculate_cusp_timing.py
* compile_met_data.py

## Plotting
* `plot_maps.py` Produces Figure 1. Requires interpolated buoy tracks.
* `plot_multi_storm_overview.py` Produces Figure 2. Requires gridded ERA5, AMSR2, and buoy data.
* `plot_storm_system.py` Produces Figure 3. Requires gridded ERA5 and buoy data.
* `plot_velocity_time_series.py` Produces the two components of Figure 7 and Figure S1 and merges them.
* `plot_deformation_time_series.py` Produces the two components of Figure 9 and Figures S1 and S2 and merges them.
* `plot_cusp_analysis.py`
    
## Instructions for obtaining the MOSAiC drifting buoy data
I downloaded the data from the Arctic Data Center on YYYYMMDD. The script drifter.py contains tools for the buoy analysis, QC, and interpolation. The script prepare_buoy_data.py uses the drifter.py tools to prepare the data and saves it in the folder 'data'.

## Instructions for obtaining the ERA5 data
You'll need the cdsapi installed. For CDS API you have to take some steps to link your CDS account. 

Components
- transform data to polar stereographic coordinates
- find path of low and save it
- potentially get shapefile for february sea ice extent for plotting
- potentially get shapefiles for coastlines; it would be good to have those on the overview plots too

Current version makes a separate dataset for each variable. Script can be customized with different start and end dates. It uses xESMF to re-grid the data to a 25-km polar stereographic grid. 

## To-do items
* plot_maps.py
    - add dependence on array_info.csv
    - add scale bar for zoomed in map
* plot_storm_system.py
    - add dependence on plot_times.csv
    - add dependence on array_info.csv
* plot_velocity_time_series.py
    - add dependence on plot_times.csv
    - set up multipanel plot to show the 4 panel display with wind direction
* plot_deformation_time_series.py
    - depends on plot_times.csv
    - depends on array_info.csv
    - produce multipanel plot with 4 panel display with velocity anomalies
* plot_cusp_analysis.py
    - scatter plot with time series of reversals
    - trajectory with wind and ice drift arrows
    - anomaly trajectories - i.e., trajectory minus origin