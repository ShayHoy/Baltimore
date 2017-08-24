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

from collections import defaultdict
import io
import re
import pandas as pd
import pprint as pp

# PARSE FILE

fn = r"/home/mapper/Documents/Python/Baltimore/BaltimoreData/ArgusData/2014-05-29_ARGUS_Baltimore.arg"


def parse_header(filename):

    """
      This function parses the information from the header rows of the .arg file and saves it into a 'defaultdict',
      and generates 'skiprow' list for pandas.read_csv()'. It breaks after parsing the header, so the data block will not
      be read into memory.

      returns: parsed header info as defaultdict object, and skipped rows list

    """





Data = pd.read_csv('/home/mapper/Documents/Python/Baltimore/BaltimoreData/ArgusData/2014-05-29_ARGUS_Baltimore.csv', header=[0,1])



