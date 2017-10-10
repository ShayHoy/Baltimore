import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString
import os
import folium as fo

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
    outName = "%s_POINTS.shp" % name
    outPath = os.path.join(outFolder, outName)
    if not os.path.exists(outPath):
        values.to_file(outPath)
        print('Processed: %s' % name)

# Turn Points into Lines
# Aggregate these points with the GroupBy
# Aggregate these points with the GroupBy
baltimore_group = baltimore_geoDF.groupby(['VesselID'])['geometry'].apply(lambda x: LineString(x.tolist()))
baltimore_group = gpd.GeoDataFrame(baltimore_group, geometry='geometry')

# Plot Lines in Folium
map = fo.Map(location=[39.2858, -76.6131], tiles='cartodbdark_matter')
map.save('/home/mapper/Documents/Python/Baltimore/Maps/test.html')

