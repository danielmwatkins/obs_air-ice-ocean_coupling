import numpy as np
import pandas as pd
import sys
import os
import rasterio
sys.path.append('../obs_air-ice-ocean_coupling/scripts/')
import drifter
import proplot as pplt
from metpy.units import units
import metpy.calc as mpcalc

radar_loc = '/Users/dwatkin2/Documents/research/data/mosaic_radar_imagery/'

# get image filenames
files = os.listdir(radar_loc + 'images/')
files = [f for f in files if 'tif' in f]
files.sort()
time = lambda f: pd.to_datetime(f.split('_')[2] + f.split('_')[3].replace('.tif', ''), format='%Y%m%d%H%M%S')
df_im = pd.DataFrame({'file': files}, index=pd.Index([time(f) for f in files], name='datetime'))
# Images are available with 5 min resolution, downsample to reduce number of files created

skip_idx = 3
df_im = df_im.iloc[::skip_idx]
images = {}
for date in df_im.index:
    try:
        images[date] = rasterio.open(radar_loc + 'images/' + df_im.loc[date, 'file'])
    except:
        print(date, 'failed to load')

# read in data from Met City
met_city = pd.read_csv('../data/met_data/metcity.csv', index_col=0, parse_dates=True).loc[
                            slice('2020-01-25 00:00', '2020-02-05 01:00')]
met_city = met_city.sort_index()
met_city = met_city.loc[met_city.index.duplicated(keep='first'),:]
met_city = drifter.compute_velocity(met_city, rotate_uv=True)

from scipy.interpolate import interp1d
met_city_aligned = {}
for var in ['latitude', 'longitude', 'x', 'y', 'wspd_u_mean_10m', 'wspd_v_mean_10m',
            'u', 'v', 'tower_heading']:
    ref = pd.to_datetime('2020-01-20 00:00')
    t = (met_city.index - ref).total_seconds()
    b = met_city[var].values
    t_new = (df_im.index - ref).total_seconds()
    b_new = interp1d(t, b, kind='linear')(t_new)
    
    met_city_aligned[var] = pd.Series(b_new, index=df_im.index)
met_city_aligned = pd.DataFrame(met_city_aligned)

uw = met_city_aligned['wspd_u_mean_10m'].rolling('10min', center=True).mean()
vw = met_city_aligned['wspd_v_mean_10m'].rolling('10min', center=True).mean()
ui = met_city_aligned['u'].rolling('10min', center=True).mean()
vi = met_city_aligned['v'].rolling('10min', center=True).mean()
met_city_aligned['wind_dir'] = mpcalc.wind_direction(uw.values * units('m/s'),
                      vw.values * units('m/s'), convention='to')
met_city_aligned['ice_dir'] = mpcalc.wind_direction(ui.values * units('m/s'),
                      vi.values * units('m/s'), convention='to')
met_city_aligned['wind_speed'] = np.sqrt(uw**2 + vw**2)
met_city_aligned['ice_speed'] = np.sqrt(ui**2 + vi**2)

pplt.rc['title.border']=False
for idx, date in enumerate(images):
    fig, ax = pplt.subplots(width=4)
    im = images[date]
    image = im.read().squeeze()
    ax.imshow(image, cmap='ice', vmin=10,  vmax=110)
    ax.format(ultitle=date.round('1min').strftime('%Y-%m-%d %H:%M'), titlecolor='y')
    
    py, px = im.index(met_city_aligned.loc[date, 'longitude'],
         met_city_aligned.loc[date, 'latitude'])
    ax.quiver(px, py, uw[date]*0.02, vw[date]*0.02, color='cyan', zorder=2, scale=1/2, width=1/150, headwidth=3)
    ax.quiver(px, py, ui[date], vi[date], color='m', zorder=2, scale=1/2, width=1/150, headwidth=3)


    ax.format(ultitle=date.round('1min').strftime('%Y-%m-%d %H:%M') + \
              '\nWind: {w:.1f} m/s\nDrift: {d:.1f} cm/s'.format(
                  w=met_city_aligned.loc[date, 'wind_speed'],
                  d=met_city_aligned.loc[date, 'ice_speed']*100),
              titlecolor='y')
    
    locs = np.linspace(-1500, 1500, 7)
    pixels = locs * 1024/5000 + 512
    
    ax.format(xlocator=pixels,
               xformatter=[str(int(x)) for x in locs],
               ylocator=pixels[::-1],
               yformatter=[str(int(x)) for x in locs][::-1],
                xtickminor=False, ytickminor=False, xrotation=90,
              xlabel='$\Delta X (m)$', ylabel='$\Delta Y (m)$')

    dy = 200
    ax.format(ylim=(1024-dy, dy), xlim=(dy, 1024-dy), title='MOSAiC Sigma6 Ice Radar')
    fig.save('../figures/animations/radar_frames/frame_' + str(idx).zfill(4) + '.png', dpi=200)
    pplt.close(fig)