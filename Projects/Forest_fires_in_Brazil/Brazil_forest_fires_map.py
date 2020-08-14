#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import geopandas as gpd

from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource
from bokeh.palettes import brewer
from bokeh.models import LinearColorMapper, ColorBar, Slider, HoverTool
from bokeh.layouts import widgetbox, column
from bokeh.io import curdoc

from bokeh.io import output_notebook, show


# In[10]:


brazil = gpd.read_file('brazil_geo.json')[['name', 'geometry']]


# In[12]:


df= pd.read_csv('forest_fires_amazon.csv' ,  encoding="cp1252") 


# In[14]:


df['state'].unique()


# In[15]:


brazil['name'].unique()


# In[16]:


df.replace({'Amapa':'Amapá' ,'Ceara':'Ceará' ,'Espirito Santo':'Espírito Santo', 'Goias':'Goiás','Maranhao':'Maranhão', 'Paraiba':'Paraíba','Piau':'Piauí', 'Rondonia':'Rondônia', 'Sao Paulo':'São Paulo', 'Rio':'Rio Grande do Norte'} , inplace=True)


# In[17]:


df =df.groupby(['state', 'year'])[['number']].sum().reset_index()


# In[19]:


gdf= pd.merge(left=brazil, right =df, left_on= 'name', right_on = 'state')


# In[20]:


gdf


# In[24]:


def get_geojson(yr):
    """Input a year (int) and return corresponding slice of the GeoDataFrame, converted to GeoJSON"""
    
    gdf_year = gdf[gdf['year'] == yr]
    json_data = gdf_year.to_json()
    return json_data


# In[25]:


geosource = GeoJSONDataSource(geojson = get_geojson(2006))


# In[26]:


slider = Slider(title = 'Year', start = 1998, end = 2016, step = 1, value = 1998)


# In[27]:


hover = HoverTool(tooltips = [ ('state','@state'), ('number', '@number')])


# In[39]:


p = figure(title = 'Sum. monthly number of fires for Year 2006',
           plot_height = 1200,
           plot_width = 900 )

p.tools.append(hover)


# In[40]:


palette = brewer['OrRd'][9]


# In[41]:


color_mapper = LinearColorMapper(palette = palette, low = -3, high = 3, nan_color = '#d9d9d9')


# In[42]:


color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=500, height=20, border_line_color=None,
                     location = (0,0), orientation = 'horizontal')


# In[43]:


p.patches('xs', 'ys', source = geosource, fill_color = {'field' :'number', 'transform':color_mapper},
          line_color = 'black', line_width = 0.25)


# In[44]:


p.add_layout(color_bar, 'below')


# In[45]:


def update_plot(attr, old, new):
    """Change properties / attributes of the datasource and title depending on slider value / position."""
    yr = slider.value
    new_data = get_geojson(yr)
    geosource.geojson = new_data
    p.title.text = f'Sum. monthly number of fires for Year {yr}'


# In[46]:


slider.on_change('value', update_plot)


# In[47]:


curdoc().add_root(column(p,widgetbox(slider)))


# In[48]:


output_notebook()


# In[49]:


show(column(p,widgetbox(slider)))


# In[ ]:





# In[ ]:





# In[ ]:




