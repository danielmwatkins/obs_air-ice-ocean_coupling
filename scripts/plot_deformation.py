import sys
sys.path.append('../scripts')
import drifter
import pandas as pd
import proplot as pplt
import numpy as np
import os
import pyproj

# Labels are A and B not the same as in Fig 6. A is the second storm and B is the first storm
# Doesn't matter though since A and B aren't in the file names or titles.
dataloc = '../data/interpolated_tracks/'
zoom_plot_dates_A= ['2020-01-31 18:00', '2020-02-01 0:00', '2020-02-01 06:00', '2020-02-01 12:00']
zoom_plot_dates_A = [pd.to_datetime(x) for x in zoom_plot_dates_A]

zoom_plot_dates_B = ['2020-01-30 05:00', '2020-01-30 11:00', '2020-01-30 18:00', '2020-01-31 04:00']
zoom_plot_dates_B = [pd.to_datetime(x) for x in zoom_plot_dates_B]



# These are used for coloring dots on the map
# Smaller groups than the polygons
left = ['2019P128', '2019P184', '2019P182', '2019P127']
right = ['2019P155', '2019P123', '2019P112', '2019P113', '2019P114', '2019P22', '2019P119']
distant = ['2019P156', '2019P157']
l_sites = ['2019T67', '2019T65', '2019S94']
ahead = ['2019P22']
co = ['2019T66']

site_specs = {'2019T67': ('tab:blue', 's', 7),
               '2019T65': ('powder blue', 's', 7),
               '2019S94': ('tab:green', 's', 7),
               '2019T66': ('tab:red', '*', 15)}

buoy_data = {}
for f in os.listdir(dataloc):
    if f[0] != '.':
        dn_id, imei, sensor_id = f.split('.')[0].split('_')
        buoy_data[sensor_id] = pd.read_csv(dataloc + f, parse_dates=True, index_col='datetime')

s_track = pd.read_csv('../data/storm_track.csv', index_col=0, parse_dates=True)
s_track = s_track.loc[slice('2020-01-31 12:00', '2020-02-02 00:00')]
    

array_info = pd.read_csv('../data/array_info.csv')
array_info = {array: group.set_index('buoyID') for array, group in array_info.groupby('array_name')}

array_info['DN_5']['line_style'] = [(1, (4, 1, 1, 1, 1, 1))]*len(array_info['DN_5'])
array_info['l_sites']['color'] = 'tab:blue'
array_info['l_sites']['line_width'] = 1.5

strain_rates = {}
for set_name in array_info:
    buoys = array_info[set_name].index[::-1]
    strain_rates[set_name] = drifter.compute_strain_rate_components(buoys, buoy_data, position_uncertainty=10)
print(strain_rates.keys())

### Deformation plots next    
ts_A = slice('2020-01-30 20:00', '2020-02-02 02:00')
ts_B = slice('2020-01-29 18:00', '2020-02-01 00:00')

# Add another set list and title when I add the extended DN
for set_list, title, ts, dates in zip(
    [['DN_full', 'l_sites', 'DN_1', 'DN_2', 'DN_3', 'DN_4', 'DN_5'],
     ['DN_full', 'l_sites', 'DN_1', 'DN_2', 'DN_3', 'DN_4', 'DN_5']],
    ['fig09a_strainrate_timeseries.jpg',
     'figS2a_strainrate_timeseries.jpg'],
    [ts_A, ts_B],
    [zoom_plot_dates_A,
     zoom_plot_dates_B]):

    fig, axs = pplt.subplots(width=5, height=6, nrows=3, sharey=False)

    for abc, date in zip(['d', 'e', 'f', 'g'], dates):
        for ax in axs:
            ax.axvline(date, color='tab:blue', lw=0.5, zorder=0)

        axs[0].text(date + pd.to_timedelta('30min'), 4, abc, color='tab:blue', zorder=4)
        axs[1].text(date + pd.to_timedelta('30min'), 2.6, abc, color='tab:blue', zorder=4)
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
        
        axs[0].format(ultitle='divergence', ylabel='$\\nabla \cdot \vec u$ (s$^{-1} \\times 10^{-6}$)', ltitle='a',
                     ylim=(-3, 4.5))
        axs[1].format(ultitle='max. shear strain rate', ylabel='$\epsilon_{II}$ (s$^{-1}\\times 10^{-6}$)', ltitle='b',
                     ylim=(0, 2.9))
        axs[2].format(ultitle='vorticity', ylim=(-8.5, 7),
                     ylabel='$\\nabla \\times \vec u$ (s$^{-1}\\times 10^{-6}$)', ltitle='c')
    axs[2].legend(loc='ll', ncols=3, order='F')
    axs.format(xrotation=45, xlabel='', xminorlocator=1/12, xgridminor=True)
    fig.save('../figures/' + title, dpi=300)
    
    
### Snapshot anomalies for part b
cusp_plot_dates = ['2020-01-31 22:00', '2020-01-31 23:00', '2020-02-01 0:00', '2020-02-01 01:00']
cusp_plot_dates = [pd.to_datetime(x) for x in cusp_plot_dates]


era5_dataloc = '../data/era5_regridded/'
buoy_dataloc = '../data/interpolated_tracks/'

# TBD add params: four dates to plot in a separate file, so that multiple figures can reference it
##### Load buoy data #####
buoy_data = {}
metadataloc = '../data/adc_dn_tracks/'
metadata = pd.read_csv(metadataloc + 'DN_buoy_list_v2.csv')
metadata['filename'] = ['_'.join([x, str(y), z]) for 
                        x, y, z in zip(metadata['DN Station ID'],
                                       metadata['IMEI'],
                                       metadata['Sensor ID'])]
metadata.set_index('Sensor ID', inplace=True)

files = os.listdir(buoy_dataloc)
files = [f for f in files if f[0] not in ['.', 'm']]
buoy_data = {f.split('_')[-1].replace('.csv', ''): pd.read_csv(buoy_dataloc + f,
            index_col=0, parse_dates=True) for f in files}

for buoy in buoy_data:
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

# Colors for buoy groups
west_buoys = ['2019P128', '2019P184', '2019P182', '2019P127']
se_buoys = ['2019P155', '2019P123', '2019P112', '2019P113', '2019P114', '2019P22', '2019P119']
far_se_buoys = ['2019P156', '2019P157']
l_sites = ['2019T67', '2019T65', '2019S94']
l_colors = {'2019T67': 'tab:blue',
            '2019T65': 'powder blue',
            '2019S94': 'tab:green'}

# pplt.rc['title.bbox'] = True
# pplt.rc['title.bboxalpha'] = 1
pplt.rc['xtick.major.width'] = 0
pplt.rc['ytick.major.width'] = 0


plot_winds = False
plot_anomalies = True

for dates, title in zip([zoom_plot_dates_A, zoom_plot_dates_B],
                        ['../figures/fig09b_snapshot_velocity_anomaly_dn.jpg',
                         '../figures/figS2b_snapshot_velocity_anomaly_dn.jpg']):


    fig, axs = pplt.subplots(height=6, nrows=2, ncols=2, share=True, spany=False, spanx=False)
    for date, ax in zip(dates, axs):
        x_dn = df_x.loc[date, co_buoy]*1e-3
        y_dn = df_y.loc[date, co_buoy]*1e-3

        ax.format(title=date.strftime('%Y-%m-%d %H:%M'), ylabel='Y (km)', xlabel='X (km)',
             ylim=(-55, 55), xlim=(-55, 45),
              xticks=np.arange(-40, 41, 20), xtickminor=False, xrotation=90,
             yticks=np.arange(-40, 41, 20), ytickminor=False)
        for buoy in buoy_data:
            if date in buoy_data[buoy].index:
                z = 4
                m = 'o'
                if buoy in west_buoys:
                    c = 'lilac'
                elif buoy in se_buoys:
                    c = 'gold'
                elif buoy in far_se_buoys:
                    c = 'orange'
                elif buoy in l_sites:
                    c = l_colors[buoy]
                    z = 5
                    m = 'o'
                else:
                    c='w'
                if buoy == '2019P22':
                    c = 'gray'
                ax.plot(buoy_data[buoy].loc[date, 'x_stere']/1e3 - x_dn,
                        buoy_data[buoy].loc[date, 'y_stere']/1e3 - y_dn,
                        edgecolor='k', edgewidth=0.5, marker=m, facecolor=c, zorder=z)

        buoy_set = [buoy for buoy in buoy_data]

        df_ua = df_u.loc[date, buoy_set] - df_u.loc[date, co_buoy]
        df_va = df_v.loc[date, buoy_set] - df_v.loc[date, co_buoy]
        df_u_mean = df_u.loc[date, dn_buoys].mean()
        df_v_mean = df_v.loc[date, dn_buoys].mean()
        ax.quiver(df_x.loc[date, buoy_set]/1e3  - x_dn,
              df_y.loc[date, buoy_set]/1e3 - y_dn,
              df_ua*100,
              df_va*100,
              scale=90, headwidth=4, c = 'k', zorder=6, width=1/250)
        
        ax.quiver(0, 0, df_u_mean*100, df_v_mean*100,
                  scale=90, headwidth=4, c='tab:red', zorder=6, width=1/250)
        v = np.sqrt(df_u_mean**2 + df_v_mean**2)*100
        ax.text(10, -50, '$\overline{U_{ice}}$: ' + str(np.round(v, 1)) + ' cm/s',
                c='tab:red')

    for ax, label in zip(axs, ['d','e','f','g']):
        ax.format(ltitle=label)


    l = []
    h = []
    for ax, date in zip(axs, dates):
    # date = zoom_plot_dates[0]
        for set_name in ['DN_full', 'DN_1', 'DN_2', 'DN_3',
                         'DN_4', 'DN_5', 'l_sites']:
            buoy_set = list(array_info[set_name].index)
            ls = array_info[set_name].line_style.values[0]
            c = array_info[set_name].color.values[0]
            lw = array_info[set_name].line_width.values[0]

            x_dn = df_x.loc[date, co_buoy]*1e-3
            y_dn = df_y.loc[date, co_buoy]*1e-3

            zorder = 3
            if set_name in ['DN_full', 'DN_5', 'l_sites']:
                zorder=2

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


    # ax.legend(h, l, loc='ll', ncols=1)

    fig.format(xreverse=False, yreverse=False)
    fig.save(title, dpi=300)

    
    
"""Based on this stackoverflow response: https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python"""
import sys
from PIL import Image

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
    
merge_images(['../figures/fig09a_strainrate_timeseries.jpg',
              '../figures/fig09b_snapshot_velocity_anomaly_dn.jpg'],
             '../figures/fig09_deformation.jpg')

merge_images(['../figures/figS2a_strainrate_timeseries.jpg',
              '../figures/figS2b_snapshot_velocity_anomaly_dn.jpg'],
             '../figures/figS2_deformation.jpg')
    