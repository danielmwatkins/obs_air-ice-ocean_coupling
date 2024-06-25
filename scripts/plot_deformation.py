import sys
sys.path.append('../scripts')
import drifter
import pandas as pd
import proplot as pplt
import numpy as np
import os
import pyproj
import xarray as xr
import sys
from PIL import Image
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from metpy.plots import ColdFront, WarmFront

pplt.rc['xtick.major.width'] = 0
pplt.rc['ytick.major.width'] = 0


# Labels are A and B not the same as in Fig 6. A is the second storm and B is the first storm
# Doesn't matter though since A and B aren't in the file names or titles.
dataloc = '../data/interpolated_tracks/'
era5_dataloc = '../data/era5_regridded/'
ts_C1 = slice('2020-01-27 18:00', '2020-02-01 00:00')
ts_C2 = slice('2020-01-30 20:00', '2020-02-02 02:00')

zoom_plot_dates_C1 = [pd.to_datetime(x) for x in ['2020-01-29 23:00','2020-01-30 05:00', '2020-01-30 11:00', '2020-01-30 18:00']]

zoom_plot_dates_C2 = [pd.to_datetime(x) for x in ['2020-01-31 18:00', '2020-02-01 0:00', '2020-02-01 06:00', '2020-02-01 12:00']]
zoom_plot_dates_C2_large = [pd.to_datetime(x) for x in ['2020-01-31 18:00', '2020-02-01 0:00', '2020-02-01 06:00', '2020-02-01 12:00']]

# These are used for coloring dots on the map
# Smaller groups than the polygons
# Could make a single reference CSV table that has the plot colors and markers for use throughout
left = ['2019P128', '2019P184', '2019P182', '2019P127']
right = ['2019P155', '2019P123', '2019P112', '2019P113', '2019P114', '2019P119']
distant = ['2019P156', '2019P157']
l_sites = ['2019T67', '2019T65', '2019S94']
ahead = ['2019P22']
co = ['2019T66']

site_specs = {'2019T67': ('tab:blue', 's', 7),
               '2019T65': ('powder blue', 's', 7),
               '2019S94': ('tab:green', 's', 7),
               '2019T66': ('tab:red', '*', 15)}


s_track = pd.read_csv('../data/storm_track.csv', index_col=0, parse_dates=True)
s_track = s_track.loc[slice('2020-01-31 12:00', '2020-02-02 00:00')]

# Manual front identification
# Units are km from storm center
sfc_cold_front = pd.read_csv('../data/sfc_cold_front_positions.csv', index_col=0)
sfc_cold_front = {date: group for date, group in sfc_cold_front.groupby('date')}

ele_cold_front = pd.read_csv('../data/ele_cold_front_positions.csv', index_col=0)
ele_cold_front = {date: group for date, group in ele_cold_front.groupby('date')}

warm_front = pd.read_csv('../data/warm_front_positions.csv', index_col=0)
warm_front = {date: group for date, group in warm_front.groupby('date')}

# Front position is relative to storm position - add s_track to be in stereographic
for date in sfc_cold_front:
    sfc_cold_front[date]['x'] = sfc_cold_front[date]['x'] + s_track.loc[date, 'x_stere']/1e3
    sfc_cold_front[date]['y'] = sfc_cold_front[date]['y'] + s_track.loc[date, 'y_stere']/1e3
for date in ele_cold_front:
    ele_cold_front[date]['x'] = ele_cold_front[date]['x'] + s_track.loc[date, 'x_stere']/1e3
    ele_cold_front[date]['y'] = ele_cold_front[date]['y'] + s_track.loc[date, 'y_stere']/1e3
for date in warm_front:
    warm_front[date]['x'] = warm_front[date]['x'] + s_track.loc[date, 'x_stere']/1e3
    warm_front[date]['y'] = warm_front[date]['y'] + s_track.loc[date, 'y_stere']/1e3
    

array_info = pd.read_csv('../data/array_info.csv')
array_info = {array: group.set_index('buoyID') for array, group in array_info.groupby('array_name')}

array_info['DN_5']['line_style'] = [(1, (4, 1, 1, 1, 1, 1))]*len(array_info['DN_5'])
array_info['l_sites']['color'] = 'tab:blue'
array_info['l_sites']['line_width'] = 1.5

#### Load buoy data #####
buoy_data = {}
for f in os.listdir(dataloc):
    if f[0] != '.':
        dn_id, imei, buoy = f.split('.')[0].split('_')
        buoy_data[buoy] = pd.read_csv(dataloc + f, parse_dates=True, index_col='datetime')

    # Does this get used?
    buoy_df = buoy_data[buoy].loc[:, ['latitude', 'longitude', 'x_stere', 'y_stere']]
    buoy_df['x'] = buoy_df['x_stere']
    buoy_df['y'] = buoy_df['y_stere']
    buoy_df = drifter.compute_velocity(buoy_df, rotate_uv=True, method='centered', date_index=True)
    buoy_data[buoy]['u'] = buoy_df['u']
    buoy_data[buoy]['v'] = buoy_df['v']
    buoy_df = drifter.compute_velocity(buoy_df, rotate_uv=False, method='centered', date_index=True)
    buoy_data[buoy]['u_stere'] = buoy_df['u']
    buoy_data[buoy]['v_stere'] = buoy_df['v']
    
co_buoy = '2019T66'
df_lon = pd.DataFrame({buoy: buoy_data[buoy]['longitude'] for buoy in buoy_data})
df_lat = pd.DataFrame({buoy: buoy_data[buoy]['latitude'] for buoy in buoy_data})
df_x = pd.DataFrame({buoy: buoy_data[buoy]['x_stere'] for buoy in buoy_data})
df_y = pd.DataFrame({buoy: buoy_data[buoy]['y_stere'] for buoy in buoy_data})
df_u = pd.DataFrame({buoy: buoy_data[buoy]['u_stere'] for buoy in buoy_data})
df_v = pd.DataFrame({buoy: buoy_data[buoy]['v_stere'] for buoy in buoy_data})
date = '2020-02-01 00:00'
dist = np.sqrt((df_x.loc[date] - df_x.loc[date, co_buoy])**2 + 
               (df_y.loc[date] - df_y.loc[date, co_buoy])**2)
dn_buoys = list(dist[dist <= 60e3].index)

for buoy in buoy_data:
    if buoy in left:
        site_specs[buoy] = ('lilac', 'o', 5)
    elif buoy in right:
        site_specs[buoy] = ('gold', 'o', 5)
    elif buoy in distant:
        site_specs[buoy] = ('tab:orange', 'o', 5)
    elif buoy == '2019P22':
        site_specs[buoy] = ('gray', 'o', 5)
    elif buoy in array_info['l_sites'].index:
        pass
    else:
        site_specs[buoy] = ('white', 'o', 5)

##### Load ERA5 data #####
variables = ['msl', 'u10', 'v10', 'u_950', 'v_950']
savename = '2020-01-25_2020-02-05'

era5_data = {var: xr.open_dataset(era5_dataloc + 'era5_' + var + '_regridded_' + savename + '.nc') for var in variables}
era5_data['950_wind_speed'] = xr.Dataset({'wind_speed': 
                            np.sqrt(era5_data['u_950']['u_950']**2 + era5_data['v_950']['v_950']**2)})


# Rotate U and V (could move this into the regridding section)
u = era5_data['u10']['u10']
v = era5_data['v10']['v10']
lon = u['longitude'] - 90 # NSIDC xstere is rotated
lat = v['latitude']
ustere = u * np.cos(np.deg2rad(lon)) - v * np.sin(np.deg2rad(lon))    
vstere = u * np.sin(np.deg2rad(lon)) + v * np.cos(np.deg2rad(lon))
era5_data['u_stere'] = xr.Dataset({'u_stere': ustere})
era5_data['v_stere'] = xr.Dataset({'v_stere': vstere})
era5_data['wind_speed'] = xr.Dataset({'wind_speed': 
                            np.sqrt(ustere**2 + vstere**2)})

#### Compute deformation ####
strain_rates = {}
for set_name in array_info:
    buoys = array_info[set_name].index[::-1]
    strain_rates[set_name] = drifter.compute_strain_rate_components(buoys, buoy_data, position_uncertainty=10)
    strain_rates[set_name].to_csv('../data/strain_rates/' + set_name + '.csv')
"""Based on this stackoverflow response: https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python"""
def merge_images(files, savename):
    """Concatenates images horizontally"""
    images = [Image.open(x) for x in files]
    widths, heights = zip(*(i.size for i in images))
    
    total_width = sum(widths)
    max_height = max(heights)
    
    new_im = Image.new('RGB', (total_width, max_height))
    
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]
    
    new_im.save(savename)


#### Plot groups ######
# Each case to plot includes 
cases = {'C1_DN': {'polygons': ['DN_full', 'l_sites', 'DN_1', 'DN_2', 'DN_3', 'DN_4', 'DN_5'],
                   'fignumber': 'S1',
                   'suffix': 'C1_dn',
                   'time_slice': ts_C1,
                   'zoom_times': zoom_plot_dates_C1,
                   'plot_winds': False,
                   'ylim': (-55, 55), 
                   'xlim': (-55, 55)
                  },
         'C2_DN': {'polygons': ['DN_full', 'l_sites', 'DN_1', 'DN_2', 'DN_3', 'DN_4', 'DN_5'],
                   'fignumber': '10',
                   'suffix': 'C2_dn',
                   'time_slice': ts_C2,
                   'zoom_times': zoom_plot_dates_C2,
                   'plot_winds': False,
                   'ylim': (-55, 55), 
                   'xlim': (-55, 55)                   
                  },
         'C1_large': {'polygons': ['DN_full', 'left', 'right', 'l_sites'],
                    'fignumber': 'S2',
                    'suffix': 'C1_large',
                    'time_slice': ts_C1,
                    'zoom_times': zoom_plot_dates_C1,
                    'plot_winds': True,
                    'ylim': (-250, 250), 
                    'xlim': (-250, 250)
                   },
         'C2_large': {'polygons': ['DN_full', 'left', 'right', 'l_sites'],
                   'fignumber': '09',
                   'suffix': 'C2_large',
                   'time_slice': ts_C2,
                   'zoom_times': zoom_plot_dates_C2_large,
                   'plot_winds': True,
                   'ylim': (-250, 250), 
                   'xlim': (-250, 250)                      
                  }
        }

# xlim/ylim
# tick spacing

for case in cases:
    set_list = cases[case]['polygons']
    title1 = 'fig' + cases[case]['fignumber'] + 'a_strainrate_timeseries_' + cases[case]['suffix'] + '.jpg'
    ts = cases[case]['time_slice']
    dates = cases[case]['zoom_times']
    plot_winds = cases[case]['plot_winds']

    #### Figure part a
    fig, axs = pplt.subplots(width=5, height=6, nrows=3, sharey=False)

    for abc, date in zip(['d', 'e', 'f', 'g'], dates):
        for ax in axs:
            ax.axvline(date, color='tab:blue', lw=0.5, zorder=0)

        axs[0].text(date + pd.to_timedelta('30min'), 4, abc, color='tab:blue', zorder=4)
        axs[1].text(date + pd.to_timedelta('30min'), 3.6, abc, color='tab:blue', zorder=4)
        axs[2].text(date + pd.to_timedelta('30min'), 5.5, abc, color='tab:blue', zorder=4)


    for set_name in set_list:
        buoy_set = list(array_info[set_name].index)
        ls = array_info[set_name].line_style.values[0]
        c = array_info[set_name].color.values[0]
        lw = array_info[set_name].line_width.values[0]

        label = set_name.replace('_', ' ').title()
        if "Dn" in label:
            label = label.replace('n', 'N')

        print(set_name, np.round(strain_rates[set_name].area.loc[ts].mean()**0.5/1e3), 'km')
        axs[0].plot(strain_rates[set_name].divergence.loc[ts] * 1e6, color=c, ls=ls, lw=lw, label=label)
        axs[1].plot(strain_rates[set_name].maximum_shear_strain_rate.loc[ts]* 1e6, ls=ls, color=c, lw=lw, label=label)    
        axs[2].plot(strain_rates[set_name].vorticity.loc[ts]* 1e6, color=c, ls=ls, lw=lw, label=label)        
        axs[0].axhline(0, color='k', lw=0.5) 
        axs[2].axhline(0, color='k', lw=0.5)
        
        axs[0].format(ultitle='divergence', ylabel='$\\nabla \cdot \mathbf{u}$ (s$^{-1} \\times 10^{-6}$)', ltitle='a',
                     ylim=(-3, 4.5))
        axs[1].format(ultitle='max. shear strain rate', ylabel='$\epsilon_{II}$ (s$^{-1}\\times 10^{-6}$)', ltitle='b',
                     ylim=(0, 3.9))
        axs[2].format(ultitle='vorticity', ylim=(-8.5, 7),
                     ylabel='$\\nabla \\times \mathbf{u}$ (s$^{-1}\\times 10^{-6}$)', ltitle='c')
    axs[2].legend(loc='ll', ncols=3, order='F')
    axs.format(xrotation=45, xlabel='', xminorlocator=1/12, xgridminor=True)
    fig.save('../figures/subplots/' + title1, dpi=300)
    pplt.close(fig)

    title2 = 'fig' + cases[case]['fignumber'] + 'b_velocity_snapshot_' + cases[case]['suffix'] + '.jpg'
    fig, axs = pplt.subplots(height=6, nrows=2, ncols=2, share=True, spany=False, spanx=False)
    for date, ax in zip(dates, axs):
        x_dn = df_x.loc[date, co_buoy]*1e-3
        y_dn = df_y.loc[date, co_buoy]*1e-3

        for buoy in buoy_data:
            c, m, ms = site_specs[buoy]
            z = 3
            for polygon in cases[case]['polygons']:
                if buoy in array_info[polygon].index:
                    z = 5
                    break
                    
            if buoy in array_info['l_sites'].index:
                z = 4
             
            if date in buoy_data[buoy].index:
                ax.plot(buoy_data[buoy].loc[date, 'x_stere']/1e3 - x_dn,
                        buoy_data[buoy].loc[date, 'y_stere']/1e3 - y_dn,
                        edgecolor='k', edgewidth=0.5, marker=m, facecolor=c, zorder=z, markersize=ms)

        if plot_winds:
            # Copy over the plotting from the velocity time series
            # TBD: add the scale arrow
            
            X = era5_data['msl']['x_stere'].data*1e-3
            Y = era5_data['msl']['y_stere'].data*1e-3
            idx_skip = 2
            local_xu = ((X - x_dn)[::idx_skip, ::idx_skip])
            local_yv = ((Y - y_dn)[::idx_skip, ::idx_skip])
        
            local_x = (X - x_dn)
            local_y = (Y - y_dn)
        
            ax.contour(local_x, local_y, era5_data['msl'].sel(time=date)['msl']/100, color='k',
                        levels=np.arange(972, 1020, 4), lw=1, labels=True, zorder=2, labels_kw = {'inline_spacing': -10})

            wind_color = 'indigo'
            ax.contour(local_x, local_y, era5_data['950_wind_speed'].sel(time=date)['wind_speed'],
                       color=[wind_color], ls='--', levels=[16], zorder=4, labels=False, lw=2.5)
            ax.contour(local_x, local_y, era5_data['950_wind_speed'].sel(time=date)['wind_speed'],
                       color=[wind_color], levels=[20], zorder=4, labels=False, lw=2.5)
 
             
            ax.quiver(local_xu, local_yv,
                      era5_data['u_stere'].sel(time=date)['u_stere'][::idx_skip, ::idx_skip],
                      era5_data['v_stere'].sel(time=date)['v_stere'][::idx_skip, ::idx_skip],
                      scale=300, width=1/400, headwidth=4, color='tab:blue')
        
        
            # add buoy velocity quiver here
            plot_buoys = []
            for polygon in cases[case]['polygons']:
                for buoy in buoy_data: 
                    if buoy in array_info[polygon].index:
                        plot_buoys.append(buoy)
#            print(plot_buoys)
	     
            ax.quiver(df_x.loc[date, plot_buoys]/1e3  - x_dn,
                  df_y.loc[date, plot_buoys]/1e3 - y_dn,
                  df_u.loc[date, plot_buoys]*100,
                  df_v.loc[date, plot_buoys]*100,
                  scale=300, headwidth=4, c = 'k', zorder=6, width=1/250)        

            for color, ls, front in zip(['b', 'b', 'r'], ['-', '--', '-'],
                        [sfc_cold_front, ele_cold_front, warm_front]):
                for ax, date in zip(axs, front):
                    x_dn = df_x.loc[date, co_buoy]*1e-3
                    y_dn = df_y.loc[date, co_buoy]*1e-3
                    if len(front[date]['x']) == len(front[date]['y']):
                        if color=='b':
                            ax.plot(front[date]['x'].values - x_dn,
                                front[date]['y'].values - y_dn, color=color,
                                ls=ls, marker='', path_effects=[ColdFront(size=3, spacing=4, flip=True)])                      
                        else:
                            ax.plot(front[date]['x'].values - x_dn,
                                front[date]['y'].values - y_dn, color=color,
                                ls=ls, path_effects=[WarmFront(size=3, spacing=4, flip=False)])
            

        else:
            # Plot velocity anomalies for all buoys
            df_ua = df_u.loc[date, :] - df_u.loc[date, co_buoy]
            df_va = df_v.loc[date, :] - df_v.loc[date, co_buoy]
            df_u_mean = df_u.loc[date, dn_buoys].mean()
            df_v_mean = df_v.loc[date, dn_buoys].mean()
            ax.quiver(df_x.loc[date, :]/1e3  - x_dn,
                  df_y.loc[date, :]/1e3 - y_dn,
                  df_ua*100,
                  df_va*100,
                  scale=90, headwidth=4, c = 'k', zorder=6, width=1/250)
            
            ax.quiver(0, 0, df_u_mean*100, df_v_mean*100,
                      scale=90, headwidth=4, c='tab:red', zorder=6, width=1/250)
            v = np.sqrt(df_u_mean**2 + df_v_mean**2)*100
            ####### Adjust position to make sense based on xlim and ylim
            ax.text(10, -50, '$\overline{U_{ice}}$: ' + str(np.round(v, 1)) + ' cm/s',
                    c='tab:red')

    for ax, label in zip(axs, ['d','e','f','g']):
        ax.format(ltitle=label)


    l = []
    h = []
    for ax, date in zip(axs, dates):
        for set_name in set_list:
            buoy_set = list(array_info[set_name].index)
            ls = array_info[set_name].line_style.values[0]
            c = array_info[set_name].color.values[0]
            lw = array_info[set_name].line_width.values[0]

            x_dn = df_x.loc[date, co_buoy]*1e-3
            y_dn = df_y.loc[date, co_buoy]*1e-3

            zorder = 4
            # if set_name in ['DN_full', 'DN_5', 'l_sites']:
            #     zorder=2

            if set_name != 'DN_full':
                h.append(ax.plot((df_x.loc[date, buoy_set + [buoy_set[0]]])*1e-3 - x_dn,
                    (df_y.loc[date, buoy_set + [buoy_set[0]]])*1e-3 - y_dn,
                        label='', marker='', lw=lw, zorder=zorder,
                     color=c, ls=ls))
                l.append(set_name)
            else:
                ax.plot((df_x.loc[date, buoy_set + [buoy_set[0]]])*1e-3 - x_dn,
                    (df_y.loc[date, buoy_set + [buoy_set[0]]])*1e-3 - y_dn,
                        label='', marker='', lw=lw, zorder=zorder,
                     color=c, ls=ls)

        ax.format(title=date.strftime('%Y-%m-%d %H:%M'), ylabel='Y (km)', xlabel='X (km)',
                     
                      ylim=cases[case]['ylim'],
                  xlim=cases[case]['xlim'],
                      # xticks=np.arange(-40, 41, 20),
                  # xticks = np.arange(xymin, xymax, 20),
                  # yticks = np.arange(xymin, xymax, 20),
                  xtickminor=False, xrotation=90,
                     # yticks=np.arange(-40, 41, 20)
                  ytickminor=False)
    if plot_winds:
        ax.quiver(45,
              -210,
              20,
              0,
              scale=300, headwidth=4, c = 'tab:blue', zorder=6, width=1/250)
        ax.quiver(45,
              -230,
              20,
              0,
              scale=300, headwidth=4, c = 'k', zorder=6, width=1/250)
        
       
        
        ax.text(90, -220, '20 m/s wind', c='tab:blue', zorder=6)
        ax.text(90, -240, '20 cm/s ice', c='k', zorder=6)
        rec = Rectangle((35, -250), 250-35, 60, ) 
        pc = PatchCollection([rec], facecolor='w', alpha=1,
                             edgecolor='k', zorder=5)
        ax.add_collection(pc)

        # Generate legend manually for finer control
        h, l = [], []
        for c, ls, label in zip(['k', wind_color, wind_color],
                            ['-', '--', '-'],
                            ['SLP (hPa)', '16 m/s wind', '20 m/s wind']):
            if label == 'SLP (hPa)':
                lw = 1
            else:
                lw = 2
            h.append(ax.plot([],[],color=c,  ls=ls, lw=lw))
            l.append(label)        
        axs[0].legend(h, l, loc='ur', ncols=1)
        
    fig.format(xreverse=False, yreverse=False)
    fig.save('../figures/subplots/' + title2, dpi=300)

    merge_images(['../figures/subplots/' + title1,
              '../figures/subplots/' + title2],
             '../figures/fig' + cases[case]['fignumber'] + '_deformation.jpg')
