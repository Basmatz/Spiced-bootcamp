import pandas as pd
import geopandas as gpd
from bokeh.plotting import figure, ColumnDataSource
from bokeh.io import output_notebook, show
from bokeh.models import GeoJSONDataSource, HoverTool

# start by importing the shape files

# note on polar circle shapefile -- it is in a different scale so I can't use lat/lon on it.
# SHAPE_BASE = '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_5/ARPA_polygon/ARPA_polygon.shp'
SHAPE_BASE = '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_5/ne_50m_land/ne_50m_land.shp'
# SHAPE_GRID = '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_5/ne_50m_graticules_5/ne_50m_graticules_5.shp'
# SHAPE_GEOLINES = '/Users/laraehrenhofer/Documents/Coding_Projects/git_repos/logistic-lemongrass-student-code/Week_5/ne_50m_geographic_lines/ne_50m_geographic_lines.shp'

base = gpd.read_file(SHAPE_BASE)

stations = pd.read_csv('arctic_stations.csv')


hover = HoverTool(tooltips = [
    ('Weather Station','@staname'),
    ('Station ID', '@staid'),
    ('(Longitude, Latitude)', '(@sta_x, @sta_y)'),
    ])

# plot base

p = figure(title = 'ARCTIC WEATHER STATIONS',
    plot_height = 600,
    plot_width = 1000,
    tools = [hover]
    )

base_json = base.to_json()

geosource = GeoJSONDataSource(geojson = base_json)

stations_source = ColumnDataSource(data=dict(
    sta_x = stations['LON_dec'],
    sta_y = stations['LAT_dec'],
    staname=stations['STANAME'],
    staid=stations['STAID']
    ))


p.patches('xs',
    'ys',
    source = geosource,
    fill_alpha = 0,
    line_color = 'black',
    line_width = 0.25
    )

# make points for each station
p.circle('sta_x', 'sta_y', size=4, color='red', alpha=1, source = stations_source)

p.tools.append(hover)

show(p)
















#
