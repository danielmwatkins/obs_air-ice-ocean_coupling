import pandas as pd
import numpy as np
import proplot as pplt
import os
import sys
sys.path.append('../scripts/')
import drifter

dataloc = '../data/interpolated_tracks/'
files = os.listdir(dataloc)
files = [f for f in files if f != '.DS_Store']
buoy_data = {}
for f in files:
    buoy_data[f.split('.')[0].split('_')[-1]] = pd.read_csv(dataloc + f, parse_dates = True, index_col=0)
    
array_info = pd.read_csv('../data/array_info.csv')
array_info = {array: group.set_index('buoyID') for array, group in array_info.groupby('array_name')}

storm_track = pd.read_csv('../data/storm_track.csv', parse_dates=True, index_col=0)

# save this list
buoy_subset = os.listdir('/Users/dwatkin2/Documents/research/packages/buoy_processing/data/subset_by_month/2020-02/')
buoy_subset = [f.replace('.csv', '') for f in buoy_subset]
buoy_subset = [f for f in buoy_subset if f in buoy_data]

DN = []
date0 = pd.to_datetime('2020-02-01 00:00')
x0 = buoy_data['2019T66'].loc[date0, 'x_stere']
y0 = buoy_data['2019T66'].loc[date0, 'y_stere']

for buoy in buoy_data:
    if date0 in buoy_data[buoy].index:
        xs = np.round(buoy_data[buoy].loc[date0, 'x_stere']  - x0, -2)/1e3
        ys = np.round(buoy_data[buoy].loc[date0, 'y_stere']  - y0, -2)/1e3
        if np.sqrt(xs**2 + ys**2) < 65:
            DN.append(buoy)

check_A = slice('2020-01-30 12:00', '2020-01-31 12:00')
check_B = slice('2020-01-31 12:00', '2020-02-01 12:00')

speed_min_a = {}
speed_min_b = {}
xa = {}
ya = {}
xb = {}
yb = {}
for buoy in DN:
    
    speed_min_a[buoy] = buoy_data[buoy].loc[check_A].speed.idxmin()
    xa[buoy] = buoy_data[buoy].loc[speed_min_a[buoy], 'x_stere']
    ya[buoy] = buoy_data[buoy].loc[speed_min_a[buoy], 'y_stere']
    speed_min_b[buoy] = buoy_data[buoy].loc[check_B].speed.idxmin()
    xb[buoy] = buoy_data[buoy].loc[speed_min_b[buoy], 'x_stere']
    yb[buoy] = buoy_data[buoy].loc[speed_min_b[buoy], 'y_stere']

speed_min = pd.DataFrame({'time_a': speed_min_a,
                          'x_stere_a': xa,
                          'y_stere_a': ya,
                          'offset_a': (pd.Series(speed_min_a) - \
                                       pd.to_datetime('2020-01-31 00:00')).dt.total_seconds()/3600,
                          'time_b': speed_min_b,
                          'x_stere_b': xb,
                          'y_stere_b': yb,
                          'offset_b': (pd.Series(speed_min_b) - \
                                       pd.to_datetime('2020-02-01 00:00')).dt.total_seconds()/3600})
date1 = '2020-01-31 00:00'
date2 = '2020-02-02 00:00'
date0 = '2020-02-01 00:00'
ts = slice(date1, date2)
x0 = buoy_data['2019T66'].loc[date0, 'x_stere']
y0 = buoy_data['2019T66'].loc[date0, 'y_stere']

plot_buoys = {'DN': buoy_subset,
              'left': ['2019P127', '2019P128', '2019P184', '2019P182'],
              'right': ['2019P123', '2019P112', '2019P114',
                        '2019P113', '2019P155', '2019P119', '2019P155'],
              'distant': ['2019P157', '2019P156']}

centers = {'left': (-130e3, 50e3),
           'right': (47e3, -85e3),
           'distant': (85e3, -400e3),
           'DN': (0, 0)}

fig, axs = pplt.subplots(ncols=2, nrows=2, share=False, aspect=1)
for ax, setname, color in zip(axs, ['left', 'DN', 'right', 'distant'],
                              ['lilac', 'gray', 'goldenrod', 'orange']):
    ax.plot((storm_track.loc[ts, 'x_stere'] - x0)/1e3,
            (storm_track.loc[ts, 'y_stere'] - y0)/1e3, lw=0.5, color='gray', marker='^', facecolor='w')
    buoy_list = plot_buoys[setname]

    for r in [50, 100, 400]:
        nper = 4e-1
        theta = np.linspace(0, 2*np.pi, int(2*np.pi*r*nper))

        x = r*np.cos(theta)
        y = r*np.sin(theta)
        ax.plot(x, y, lw=0.5, color='gray')
   
    for buoy in buoy_data:
        if buoy in buoy_list:
            df = buoy_data[buoy]
            ax.plot((df.x_stere.loc[ts] - x0)/1e3,
                        (df.y_stere.loc[ts]-y0)/1e3, zorder=1,
                        color='k', lw=0.5)
            if date1 in buoy_data[buoy].index:
                ax.plot((df.x_stere.loc[date1] - x0)/1e3,
                        (df.y_stere.loc[date1]-y0)/1e3,
                        facecolor=color, lw=0, marker='s', ms=3, edgecolor='k', ew=0.5, zorder=3)
                    
            for date in pd.date_range(pd.to_datetime(date1), freq='6H', periods=7):
                if date in df.index:
                    ax.plot((df.x_stere.loc[date] - x0)/1e3,
                        (df.y_stere.loc[date]-y0)/1e3,
                        facecolor='k', lw=0, marker='.', ms=3, edgecolor='k', ew=0.5, zorder=2)

        elif setname == 'DN':
            if date0 in buoy_data[buoy].index:
                ax.plot((buoy_data[buoy].loc[date0, 'x_stere'] - x0)/1e3,
                        (buoy_data[buoy].loc[date0, 'y_stere'] - y0)/1e3, color='gray',
                        m='.', ms=2, zorder=0)
            
    dx = 60
    if setname == 'distant':
        dx = 60
    title = setname
    if setname == 'DN':
        title = 'Distributed Network'
    ax.format(xreverse=False, yreverse=False,
              ultitle=title.title(), ylim=(centers[setname][1]/1e3 - dx, centers[setname][1]/1e3 + dx),
              xlim=(centers[setname][0]/1e3 - dx, centers[setname][0]/1e3 + dx))

c = axs[1].scatter((speed_min['x_stere_b'] - x0)/1e3, (speed_min['y_stere_b']-y0)/1e3, marker='o', ms=20,
           vmin=-2, vmax=2, N=9, c=speed_min['offset_b'], cmap='bwr', zorder=3, edgecolor='k', ew=0.5)

l_co_sites = {'L1': '2019T67', # L1 / T67 / asfs 40
           'L2': '2019T65', # L2 / T65 / asfs 30
           'L3': '2019S94', # L3 / S94 / asfs 50
           'Met City': '2019T66'}
lsites = [l_co_sites['L1'], l_co_sites['L2'], l_co_sites['L3']]

axs[1].scatter((speed_min.loc[lsites, 'x_stere_b'] - x0)/1e3, (speed_min.loc[lsites, 'y_stere_b']-y0)/1e3, marker='s', ms=40,
           vmin=-2, vmax=2, N=9, c=speed_min.loc[lsites, 'offset_b'], cmap='bwr', zorder=4, edgecolor='k', ew=0.5)
axs[1].scatter((speed_min.loc['2019T66', 'x_stere_b'] - x0)/1e3,
               (speed_min.loc['2019T66', 'y_stere_b'] - y0)/1e3,
               marker='*', ms=150,
           vmin=-2, vmax=2, N=9, c=speed_min.loc['2019T66', 'offset_b'], cmap='bwr', zorder=5, edgecolor='k', ew=0.5)

axs[1].text(55*np.cos(np.pi/4), 55*np.sin(np.pi/4), str(50) + ' km', color='gray') # DN
axs[3].text(365*np.cos(np.deg2rad(-75)), 415*np.sin(np.deg2rad(-75)), str(400) + ' km', color='gray') # Distant
axs[0].text(125*np.cos(np.deg2rad(160)), 125*np.sin(np.deg2rad(160)), str(100) + ' km', color='gray') # Left

axs[2].text(55*np.cos(np.deg2rad(-45)), 55*np.sin(np.deg2rad(-45)), str(50) + ' km', color='gray') # Right
axs[2].text(105*np.cos(np.deg2rad(-45)), 105*np.sin(np.deg2rad(-45)), str(100) + ' km', color='gray') # Right
axs[1].colorbar(c, label='Time since Feb 1 00 UTC (Hours)') 
axs.format(ylabel='Distance from CO, y-direction (km)', xlabel='Distance from CO, x-direction (km)',
           xlocator=20, ylocator=20, xtickminor=False, ytickminor=False, abc=True)


# legends
h = [ax.plot([],[], c=c, m=m, ms=ms, ec='k', ew=0.5, lw=0) for c, m, ms in zip(['k', 'gray'], ['.', 's'], [5, 3])]
l = ['6-hourly positions', 'Initial position']
axs[-1].legend(h, l, loc='ll', ncols=1)

h = [ax.plot([],[], c='w', m='^', ec='gray', ew=0.5, lw=1)]
l = ['Storm track (hourly)']
axs[0].legend(h, l, loc='ur', ncols=1)

h = [ax.plot([],[], c='w', m=m, ms=ms, ec='k', ew=0.5, lw=0)
     for m, ms in zip([ '*', 's', 'o'], [15, 5, 5])]
l = ['CO', 'L-sites', 'P-sites']
axs[1].legend(h, l, loc='lr', ncols=1)


fig.save('../figures/fig07_trajectories_01-31_to_02-02.jpg', dpi=300)