import folium as fo
import flask
from flask import Flask
app = Flask(__name__)

map = fo.Map(location=[39.2858, -76.6131], tiles='cartodbdark_matter')
map.save('/home/mapper/Documents/Python/Baltimore/Maps/test.html')


@app.route('/')
def show_map():
    return flask.send_file('/home/mapper/Documents/Python/Baltimore/Maps/test.html')


