# Observations of the air-sea ice-ocean response to a winter cyclone

This repository contains the code to reproduce the analysis of sea ice motion and storm structure. The scripts can be divided into code for obtaining and preparing the data and code for carrying out the analysis of the data. 

Key components
1. Drifting buoy dataset
2. Meteorological data from flux towers and sleds
3. Meteorological data from ERA5 reanalysis


## Instructions for obtaining the MOSAiC drifting buoy data
I downloaded the data from the Arctic Data Center on YYYYMMDD. The script drifter.py contains tools for the buoy analysis, QC, and interpolation. The script prepare_buoy_data.py uses the drifter.py tools to prepare the data and saves it in the folder 'data'.

## Instructions for obtaining the ERA5 data
You'll need the cdsapi installed. Potentially xESMF if I can get it to work. For CDS API you have to take some steps to link your CDS account. 
Fields: u,v,q,t at 925, 950

Components
- transform data to polar stereographic coordinates
- find path of low and save it
- potentially get shapefile for february sea ice extent for plotting
- potentially get shapefiles for coastlines; it would be good to have those on the overview plots too

Current version makes a separate dataset for each variable. It's fairly trivial to make these into one, I just don't have time to do that today.