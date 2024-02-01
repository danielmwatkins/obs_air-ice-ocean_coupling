import requests
import pandas as pd
import os
# Where to save the radar imagery
# Total download is approximately 3,000 images, at 1.1 MB each
save_loc = '/Users/dwatkin2/Documents/research/data/mosaic_radar_imagery/images'
# The overview file was downloaded from Pangaea, it contains the filenames
# for the images in the repository and is included in the github repository for convenience
overview_file = '../data/PS122_2_ice_radar.tab'
with open(overview_file) as f:
    lines = f.readlines()
    for idx, line in enumerate(lines):
        if '*/' in line:
            break
    overview = pd.read_table(radar_loc + overview_file, skiprows=idx + 1, header=0)

overview['Date/Time'] = pd.to_datetime(overview['Date/Time'])
overview.rename({'Date/Time': 'datetime'}, axis=1, inplace=True)
overview.set_index('datetime', inplace=True)
overview['datetime_rounded'] = overview.index.round('5min')

# Select just the data from the study period
files = overview.loc[slice('2020-01-25', '2020-02-04'), 'Binary']

downloaded = os.listdir(save_loc)
for idx in range(len(files)):
    if files[idx] not in downloaded:
        image_url = 'https://download.pangaea.de/dataset/929435/files/' + files[idx]
        img_data = requests.get(image_url).content
        savepath = radar_loc + '/images/' + files[idx]
        with open(savepath, 'wb') as handler:
            handler.write(img_data)