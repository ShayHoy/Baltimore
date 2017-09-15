"""
Author: Shannon Hoy
Date: Fall 2018

This is a library of functions created to perform geospatial analysis on volunteered geographic hydro data
info file,then parses the data into a geopandas dataframe and exports a geojson file


"""

# IMPORT NECESSARY PACKAGES

import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np



# PARSE FILE ARGUS DATA


def pandas_argus(filename):

    """
      This function parses the information from the header rows of the .arg file and saves it into a 'defaultdict',
      and generates 'skiprow' list for pandas.read_csv()'. It breaks after parsing the header, so the data block will no
      be read into memory.

      returns: parsed header info as defaultdict object, and skipped rows list

    """

    # useful header information that will be saved into a list

    with open(filename) as f:
        header = []
        i = 0
        skip = []
        for line in f:
                line = line.strip()
                if line.startswith('DATA'):
                    skip.append(i)
                    break
                else:
                    skip.append(i)
                    header.append(line)
                i = i+1

    # Create a pandas dataframe with header and footer removed

    argusdata = pd.read_csv(filename, engine='python', header=None, skiprows=skip, skipfooter=2)
    argusdata = pd.DataFrame(argusdata)
    argusdata.columns = ['Date', 'Time', 'Lat', 'Long', 'Speed', 'Depth', 'StaticDraft', 'VesselID']
    return argusdata


def argus_header(filename):
    with open(filename) as f:
        header = []
        i = 0
        skip = []
        for line in f:
            line = line.strip()
            if line.startswith('DATA'):
                skip.append(i)
                break
            else:
                skip.append(i)
                header.append(line)
            i = i + 1
    return header


def simplexy(dataframe):

    x = dataframe['Long']
    y = dataframe['Lat']

    map = Basemap(projection='merc', lat_0=39.30, lon_0=-76.595,
                  resolution='h', area_thresh=0.1,
                  llcrnrlon=-76.7, llcrnrlat=39.18,
                  urcrnrlon=-76.4, urcrnrlat=39.3)

    map.drawcoastlines()
    map.drawcountries()
    map.fillcontinents(color='green')
    map.drawmapboundary()
    map.scatter(x, y)
    map.drawmeridians(np.arange(0, 360, 30))
    map.drawparallels(np.arange(-90, 90, 30))

    plt.show()



