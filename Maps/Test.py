import folium as fo
from flask import Flask
import flask
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from folium import plugins

app = Flask(__name__)

map = fo.Map(location=[39.2858, -76.6131], tiles='cartodbdark_matter')
map.save('/home/mapper/Documents/Python/Baltimore/Maps/test.html')


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

argus_data = pandas_argus('/home/mapper/Documents/Python/Baltimore/BaltimoreData/ArgusData/2014-05-29_ARGUS_Baltimore.arg')


def geopandas_argus(pandas_df):

    """
      Creates a GeoDataFrame from a pandas dataframe

    """

    geometry = [Point(xy) for xy in zip(pandas_df.Long, pandas_df.Lat)]
    pandas_df = pandas_df.drop(['Long', 'Lat'], axis=1)
    crs = {'init': 'epsg:4326'}
    geo_df = GeoDataFrame(pandas_df, crs=crs, geometry=geometry)
    return geo_df

geo_argus = geopandas_argus(argus_data)


matrix = argus_data[['Lat', 'Long']].as_matrix()
map.add_children(plugins.HeatMap(matrix, radius=10))
map.save('/home/mapper/Documents/Python/Baltimore/Maps/test.html')


