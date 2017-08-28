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

data = pd.read_csv(fn, header=None, skiprows=skiprows)

print(type(data))
print(header)
print(data.tail(n=10))

# plot overall map

map = Basemap(projection='merc', llcrnrlat=38.9, llcrnrlon=-77, urcrnrlat=39.4, urcrnrlon=-76, lat_ts=39.2)
map.bluemarble()
plt.show()





















