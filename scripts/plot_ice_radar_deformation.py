import pandas as pd
import numpy as np
import proplot as pplt
from PIL import Image

mu_def = pd.read_csv('../data/IceRadar_JanFeb2020_deformation.txt', index_col=0, parse_dates=True)
strain_rates = {}
for dn_array in ['DN_1', 'DN_2', 'DN_3', 'DN_4', 'DN_5', 'DN_full']:
    strain_rates[dn_array] = pd.read_csv('../data/strain_rates/' + dn_array + '.csv', index_col=0, parse_dates=True)

imdates = ['2020-01-30 06:00:02',
           '2020-01-30 11:59:56',
           '2020-01-30 19:59:46',
           '2020-02-01 05:54:49',
           '2020-02-01 09:54:53',
           '2020-02-01 12:55:02'
          ]

set_list = ['DN_full']
ts = slice('2020-01-30 01:00', '2020-02-01 23:00')
dates = [pd.to_datetime(x) for x in imdates]
ls = '-'
lw = 0.5
label=''
c = 'k'



#### Figure panel g
fig, axs = pplt.subplots(width=8, height=2, nrows=1, sharey=False)
for abc, date in zip(['a', 'b', 'c', 'd', 'e', 'f'], dates):
    axs[0].axvline(date, color='tab:blue', lw=0.5, zorder=0)
    axs[0].text(date + pd.to_timedelta('30min'), 5.5, abc, color='tab:blue', zorder=4)

for set_name in strain_rates:
    if 'DN' in set_name:
        if set_name == 'DN_full':
            lw=1
            ls='-'
            label='DN buoys'
        else:
            lw=0.5
            label=''
            ls='--'
        axs[0].plot(strain_rates[set_name].divergence.loc[ts] * 1e6, color=c, ls=ls, lw=lw, label=label, marker='', ms=5)

# conversion: units of 10 per minute, so divide by 10 and then divide by 60. Finally multiply by 1e6 so the axis is whole numbers
axs[0].plot(mu_def['Divergence rate (ship radar | 10 min^(-1))'].loc[ts] * 1 / 600 * 1e6, color='tab:green',
            ls=ls, lw=1.2, label='Ice radar')
axs[0].format(ylim=(-4.5, 7.5), ltitle='g. divergence', ylabel='$\\nabla \cdot \mathbf{u}$ (s$^{-1} \\times 10^{-6}$)', xlabel='',
             xrotation=45, xminorlocator=1/12, xgridminor=True)
axs[0].legend(loc='uc', ncols=1)
fig.save('../figures/subplots/matias_radar_strain_rate.jpg', dpi=300)

def merge_images(files, savename):
    """Concatenates images vertically. Only expects two images."""
    images = [Image.open(x) for x in files]
    widths, heights = zip(*(i.size for i in images))    
    total_height = sum(heights)
    max_width = max(widths)
    for idx in range(len(images)):
        im = images[idx]
        if im.size[0] != max_width:
            new_height = int(im.size[1]*(max_width/im.size[0]))
            im = im.resize((max_width, new_height))    
        images[idx] = im
    widths, heights = zip(*(i.size for i in images))    
    total_height = sum(heights)
    max_width = max(widths)    
    
    new_im = Image.new('RGB', (max_width, total_height))
    
    y_offset = 0
    for im in images:
        new_im.paste(im, (0, y_offset))
        y_offset += im.size[1]
    
    new_im.save(savename)

merge_images([
    '../figures/fig11_sigma6_radar_annotations.jpg',
    '../figures/subplots/matias_radar_strain_rate.jpg'],
    '../figures/fig11_ice_radar_with_strain_rates.jpg')