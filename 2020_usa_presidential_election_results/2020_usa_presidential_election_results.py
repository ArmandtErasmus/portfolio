# import necessary libraries
import plotly.express as px
import numpy as np
import pandas as pd
import json
import plotly.io as pio
import plotly.graph_objects as go
pio.renderers.default = 'iframe' # can change this to browser too

# import data
us_states_map = json.load(open('us-states.json', 'r'))
state_results = pd.read_html('https://en.wikipedia.org/wiki/2020_United_States_presidential_election')[29]

# create a subset of the data
trump_biden = state_results.iloc[list(range(0, 8)) + list(range(9, 20)) + list(range(22, 30)) + list(range(33, 56)), [0,1,2,3,4,5,6]]
trump_biden.reset_index(drop=True, inplace=True)

# create a dictionary that contains state names as keys and state name abbreviations as values
states_id_map = {}

for feature in us_states_map['features']:
    states_id_map[feature['properties']['name']] = feature['id']
    
trump_biden['id'] = trump_biden.index.map(lambda x: states_id_map[list(states_id_map.keys())[x]])

# create a new dataframe that contains state abbreviations and electoral votes for each party
data_for_map = pd.DataFrame({
    'id': trump_biden['id'],
    'Biden/HarrisDemocratic_EV': trump_biden['Biden/HarrisDemocratic']['EV'],
    'Trump/PenceRepublican_EV': trump_biden['Trump/PenceRepublican']['EV']
})

# create a cloropleth map for the democratic party
trace_biden = go.Choropleth(
    locations=data_for_map['id'],
    z=data_for_map['Biden/HarrisDemocratic_EV'],
    locationmode='USA-states',
    colorscale=[[0, 'rgb(118, 171, 219)'], [1, 'rgb(73, 150, 222)']],
    colorbar_title='Democratic'
)

# create a cloropleth map for the republican party
trace_trump = go.Choropleth(
    locations=data_for_map['id'],
    z=data_for_map['Trump/PenceRepublican_EV'],
    locationmode='USA-states',
    colorscale=[[0, 'rgb(250, 100, 103)'], [1, 'rgb(222, 58, 60)']],
    colorbar_title='Republican',
    colorbar=dict(
        x=1.2
    )
)

# create an informational layout
layout = go.Layout(
    title='2020 United States Presidential Election Results',
    geo=dict(
        scope='usa',
        center={'lat': 39.0902, 'lon': -97.7129},
    )
)

# create the final map
fig = go.Figure(data=[trace_biden, trace_trump], layout=layout)

# add state abbreviations
fig.add_scattergeo(
    locations=data_for_map['id'],
    locationmode='USA-states',
    text=data_for_map['id'],
    mode='text',
    textfont=dict(
        color='white',
    ))

# show the map
fig.show()