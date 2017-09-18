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
import matplotlib.pylab as pylab
from geopandas import GeoDataFrame
from shapely.geometry import Point
import numpy as np
import time
from scipy import ndimage



# PARSE FILE ARGUS DATA

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
    argusdata[['Long', 'Lat']] = argusdata[['Long', 'Lat']].astype(float)

    return argusdata


def geopandas_argus(pandas_df):

    """
      Creates a GeoDataFrame from a pandas dataframe

    """

    geometry = [Point(xy) for xy in zip(pandas_df.Long, pandas_df.Lat)]
    pandas_df = pandas_df.drop(['Long', 'Lat'], axis=1)
    crs = {'init': 'epsg:4326'}
    geo_df = GeoDataFrame(pandas_df, crs=crs, geometry=geometry)
    return geo_df




# def simplexy(dataframe):
#
#     map = Basemap(projection='merc', lat_0=39.30, lon_0=-76.595,
#                   resolution='h', area_thresh=0.1,
#                   llcrnrlon=-76.7, llcrnrlat=39.18,
#                   urcrnrlon=-76.4, urcrnrlat=39.3)
#
#     map.drawcoastlines()
#     map.drawcountries()
#     map.fillcontinents(color='green')
#     map.drawmapboundary()
#     map.drawmeridians(np.arange(0, 360, 30))
#     map.drawparallels(np.arange(-90, 90, 30))
#     map_points = pd.Series([Point(map(mapped_x, mapped_y)) for mapped_x, mapped_y in zip(argusdata['Long'], argusdata['Lat'])])
#     map.scatter(
#         [geom.x for geom in map_points],
#         [geom.y for geom in map_points],
#         5, marker='o', lw=.25,
#         facecolor='#33ccff', edgecolor='w',
#         alpha=0.9, antialiased=True,
#         label='Blue Plaque Locations', zorder=3)
#
#     plt.title('Argus Data From Baltimore Harbor')
#     plt.show()

def simplexy(dataframe):
    start = time.time()
    dataframe.plot(color='green', markersize=1)
    end = time.time()
    print(end-start)


def simple_heatmap(dataframe, bins=(100, 100), smoothing=1.3, cmap='jet'):

    start = time.clock()

    def getx(pt):
        return pt.coords[0][0]

    def gety(pt):
        return pt.coords[0][1]

    x = list(dataframe.geometry.apply(getx))
    y = list(dataframe.geometry.apply(gety))
    heatmap, xedges, yedges = np.histogram2d(y, x, bins=bins)
    extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]

    logheatmap = np.log(heatmap)
    logheatmap[np.isneginf(logheatmap)] = 0
    logheatmap = ndimage.filters.gaussian_filter(logheatmap, smoothing, mode='nearest')

    plt.imshow(logheatmap, cmap=cmap, extent=extent)
    plt.colorbar()
    plt.gca().invert_yxis()
    plt.show()

    print(time.clock(), "seconds process time")




