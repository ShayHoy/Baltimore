# Author: Shannon Hoy
# Date: Fall 2018

# This function takes a V1.0 Argus data file (.arg) and stores the header information into an
# info file,then parses the data into a geopandas dataframe and exports a geojson file
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Argus Data Format:
#    Header Info:
#       SURVICE PROPRIETARY
#       <!-- ARGUS -->
#       FORMAT
#       DATUM
#       CORRECTIONS
#       FILTERS
#       HEADER
#       HEADERUNITS
#       DATA
#   Data begins after "DATA" indicator. The data format is:
#       YYYY-MM-DD,HH:MM:SS,LAT,LON,SPEED,DEPTH(in feet),DRAFT,ID - NAME
#       with ID being three hex digits and NAME being a text string describing the ship.
#
#
# Output Data Format:


# IMPORT NECESSARY PACKAGES

from collections import defaultdict
import io
import re
import pandas as pd
import pprint as pp

# PARSE FILE

fn = r""




Data = pd.read_csv('/home/mapper/Documents/Python/Baltimore/BaltimoreData/ArgusData/2014-05-29_ARGUS_Baltimore.csv', header=[0,1])



