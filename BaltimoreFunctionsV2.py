import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import os

fp = '/home/mapper/Documents/Python/Baltimore/BaltimoreData/ArgusData/2014-05-29_ARGUS_Baltimore.arg'

# Read in Data into Pandas DataFrame
baltimore_df = pd.read_csv(fp, skiprows=9, names=['Date', 'Time', 'Latitude', 'Longitude', 'Speed', 'Depth', 'StaticDraft', 'VesselID'])

# Convert from Pandas to GeoPandas
baltimore_geoDF = gpd.GeoDataFrame(baltimore_df)

# Make Geometry Column for GeoDataFrame
baltimore_geoDF['geometry'] = None
baltimore_geoDF['geometry'] = [Point(xy) for xy in zip(baltimore_geoDF.Longitude, baltimore_geoDF.Latitude)]


# Set Coordinate System to WGS84
baltimore_geoDF.crs = {'init': 'epsg:4326'}
print(baltimore_geoDF.crs)

# Groupby Vessel
grouped = baltimore_geoDF.groupby('VesselID')

# Make Individual Ship Shapefiles (points)
outFolder = r"/home/mapper/Documents/Python/Baltimore/BaltimoreData/ArgusShapefiles"

for key, values in grouped:
    name = key.replace(' ', '_')
    name = name.replace('-', '_')
    outName = "%s.shp" % name
    print('Processing: %s' % name)
    outPath = os.path.join(outFolder, outName)
    values.to_file(outPath)
