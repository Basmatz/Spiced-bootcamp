import pandas as pd
import geopandas as gpd
from bokeh.plotting import figure
from bokeh.io import output_notebook, show
from bokeh.models import GeoJSONDataSource

# start by importing the shape files


SHAPE_BASE = '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_5/ne_50m_land/ne_50m_land.shp'
# SHAPE_GRID = '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_5/ne_50m_graticules_5/ne_50m_graticules_5.shp'
# SHAPE_GEOLINES = '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_5/ne_50m_geographic_lines/ne_50m_geographic_lines.shp'

base = gpd.read_file(SHAPE_BASE)

stations = pd.read_csv('arctic_stations.csv')

stations_x = stations['LON_dec'].to_list()
stations_y = stations['LAT_dec'].to_list()

# plot base

p = figure(title = 'blank',
    plot_height = 600,
    plot_width = 1000,
    )

base_json = base.to_json()

geosource = GeoJSONDataSource(geojson = base_json)

p.patches('xs',
    'ys',
    source = geosource,
    fill_alpha = 0,
    line_color = 'black',
    line_width = 0.25
    )

# make points for each station
p.circle(stations_x, stations_y, size=4, color='red', alpha=1)

show(p)
















#
