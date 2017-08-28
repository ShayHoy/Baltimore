"""
Author: Shannon Hoy, based on script by ('MaxU on stackoverflow:
        https://stackoverflow.com/questions/36671176/reading-a-complicated-csv-file-with-python)
Date: Fall 2018

This function takes a V1.0 Argus data file (.arg) and stores the header information into an
info file,then parses the data into a geopandas dataframe and exports a geojson file

Argus Data Format:
   Header Info:
      SURVICE PROPRIETARY
      <!-- ARGUS -->
      FORMAT
      DATUM
      CORRECTIONS
      FILTERS
      HEADER
      HEADERUNITS
      DATA
  Data begins after "DATA" indicator. The data format is:
      YYYY-MM-DD,HH:MM:SS,LAT,LON,SPEED,DEPTH(in feet),DRAFT,ID - NAME
      with ID being three hex digits and NAME being a text string describing the ship.

Output Data Format:


"""

# IMPORT NECESSARY PACKAGES

import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np


# PARSE FILE

fn = r"/home/mapper/Documents/Python/Baltimore/BaltimoreData/ArgusData/2014-05-29_ARGUS_Baltimore.arg"


def parse_header(filename):

    """
      This function parses the information from the header rows of the .arg file and saves it into a 'defaultdict',
      and generates 'skiprow' list for pandas.read_csv()'. It breaks after parsing the header, so the data block will not
      be read into memory.

      returns: parsed header info as defaultdict object, and skipped rows list

    """

    # useful header information that will be saved into a list


    with open(fn) as f:
        header = []
        i = 0
        skiprows = []
        for line in f:
                line = line.strip()
                if line.startswith('DATA'):
                    skiprows.append(i)
                    break
                else:
                    skiprows.append(i)
                    header.append(line)
                i = i+1
        return header, skiprows


header, skiprows = parse_header(fn)

# parses data block and skips the header

ArgusData = pd.read_csv(fn, header=None, skiprows=skiprows)
ArgusData = pd.DataFrame(ArgusData)
ArgusData.columns=['Date', 'Time', 'Lat', 'Long', 'Speed', 'Depth', 'StaticDraft', 'VesselID']
print(type(ArgusData))
print(header)
print(ArgusData.head(n=10))  # plot overall map

test = ArgusData.plot(x='Long', y='Lat')
plt.show(test)

#   PLOT NAUTICAL CHART
# def make_map(llcrnrlon=None, urcrnrlon=None,
#              llcrnrlat=None, urcrnrlat=None,
#              img=None, figsize=(10, 10), resolution='f'):
#     m = Basemap(llcrnrlon=llcrnrlon, urcrnrlon=urcrnrlon,
#                 llcrnrlat=llcrnrlat, urcrnrlat=urcrnrlat,
#                 projection='merc', resolution=resolution,
#                 lat_ts=(llcrnrlat+urcrnrlat) / 2.)    #only works for northern hemisphere
#     fig, ax = plt.subplots(figsize=figsize, facecolor='none')
#     m.ax = ax
#     if img:
#         image = plt.imread(img)
#         m.imshow(image, origin='upper', alpha=0.75)
#     meridians = np.linspace(llcrnrlon, urcrnrlon, 4)
#     parallels = np.linspace(llcrnrlat, urcrnrlat, 4)
#     kw = dict(linewidth=0)
#     m.drawparallels(parallels, labels=[1, 0, 0, 0], **kw)
#     m.drawmeridians(meridians, labels=[0, 0, 0, 1], **kw)
#     return fig, m
#
#
# llcrnrlon=-(76 + 38/60)
# llcrnrlat=(39 + 12/60)
# urcrnrlon=-(76 + 28/60)
# urcrnrlat=(39 + 17/60)
#
# chart = '/home/mapper/Documents/Python/Baltimore/BaltimoreData/ArgusData/12281.png'
# fig, m = make_map(llcrnrlon, urcrnrlon, llcrnrlat, urcrnrlat, img=chart, resolution='c')
