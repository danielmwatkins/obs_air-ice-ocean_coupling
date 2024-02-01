# Air-Ice-Ocean Coupling During a Strong Mid-Winter Cyclone: Observations
This repository contains code used in the analysis of sea ice motion and storm structure during a pair of winter cyclones observed during the MOSAiC Arctic Expedition in January and February 2020. The results produced here are a portion of a collaborative project funded by the US Department of Energy. Results have been shared in numerous scientific conferences, and will be available in a peer-reviewed journal article in the _Journal of Geophysical Research: Atmospheres_ in the near future. A poster summarizing the results was presented at the American Geophysical Union 2023 Annual Meeting and can be viewed here: [Sea Ice and Ocean Response to a Strong Mid-Winter Cyclone in the Arctic Ocean](https://doi.org/10.22541/essoar.170365235.53452562/v1)

## Setting up a computing environment
The analysis was carried out using open-source libraries for Python 3.9. The computing environment can be recreated using the package list in the file `airsea.yml`. If you do not already have an installation of the environment manager `conda`, follow the instructions to download [microconda](https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html)(a minimal installation of the conda environment manager). You can then create an environment with the necessary packages by running this code in a terminal window:

```conda env create --file airsea.yml```

## Preparing data
The data preparation scripts require the following datasets to be downloaded. For ERA5, a download script is included. Using this script requires an account at the Copernicus Data Store. Similarly, a download script for the sigma6 radar product is provided.
1. Drifting buoy dataset: [Bliss et al. data paper](https://www.nature.com/articles/s41597-023-02311-y)
    * `prepare_buoy_data.py` Applies `standard_qc` and `interpolate_buoy_track` funtions from the `drifter.py` file to the MOSAiC buoy data files to produce quality controlled, hourly-resolution time series with stereographic coordinates and velocity estimates. Trajectories are saved to the folder `data/interpolated_tracks/`. Data from the Arctic Data Center should be placed in the folder `data/adc_dn_tracks`.

2. Meteorological data from flux towers and sleds: [Cox et al. data paper](https://www.nature.com/articles/s41597-023-02415-5)
    * `compile_met_data.py` Produces CSV files from the Level 3 Met City and ASFS netCDF datasets. Data must first be downloaded from the Arctic Data Center and the user specifies the location where the data are stored.
      
3. Meteorological data from ERA5 reanalysis: [Single level](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview) and [pressure level](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=overview) data from the Copernicus Data Store
    * `prepare_era_data.py` Downloads ERA5 data from 2020-01-25 to 2020-02-05 and saves it locally, then uses xesmf to regrid onto the NSIDC polar stereographic grid. Data is saved to the folder `data/era5_regridded`.
      
4. Sea ice concentration from AMSR Unified 12 km: [National Snow and Ice Data Center](https://nsidc.org/data/au_si12/versions/1)
    * `compile_amsr.py` Reads in the daily 12 km AMSR data obtained from NSIDC and compiles the files into a single netcdf file. Expects hdf-5 files from NSIDC to be in the folder `data/amsr`.
      
6. Sea ice sigma 6 radar: [Krumpen et al. (2021), Pangaea Data Repository](https://doi.pangaea.de/10.1594/PANGAEA.929435)

## Parameter files
* `array_info.csv` Table containing the buoys used in the deformation arrays, and the color scheme.
* `buoy_info.csv`. TBD table with the buoy parameters, used to make a table for manuscript.

## Utilities
* `drifter.py` Functions for processing the drifting buoy data

## Calculations
* calculate_deformation.py
    - depends on array_info
* calculate_cusp_timing.py

## Figures
### Figure 1: Map of the MOSAiC drifting buoy array
![Two panel map showing the position of the MOSAiC drifting buoys on February 1, 2020. The left panel shows the region from approximately 65 to 115 degrees E in longitude and latitudes from 79 degrees N to 89.5 N. The central observatory is indicated by a star, and the positions of 13 drifters comprising the MOSAiC Extended DN surround it. On the right, a zoomed in map shows an additional set of approximately 50 buoys and three L sites, which are sites with many autonomous sensors.](/figures/fig01_distributed_network_map.png?raw=true "Map of the MOSAiC Distributed Network")


* `plot_maps.py` Produces Figure 1. Requires interpolated buoy tracks.
* `plot_multi_storm_overview.py` Produces Figure 2. Requires gridded ERA5, AMSR2, and buoy data.
* `plot_storm_system.py` Produces Figure 3. Requires gridded ERA5 and buoy data.
* `plot_velocity_time_series.py` Produces the two components of Figure 7 and Figure S1 and merges them.
* `plot_deformation_time_series.py` Produces the two components of Figure 9 and Figures S1 and S2 and merges them.
* `plot_cusp_analysis.py`

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