import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

# API keys and datasets
mapbox_access_token = 'pk.eyJ1IjoiZ3BzaW5naDEyIiwiYSI6ImNrMzNhanQ2ZjBqODMzaW1tbHRxNHBqa20ifQ.ewLqQWO3g2TNM-8NpFhcxw'
FDNYVL_DF = pd.read_csv("https://raw.githubusercontent.com/gpsingh12/DATA608/master/Final-Project/fdny_vio.csv")
FDNYVL_DF['YEAR'] = pd.DatetimeIndex(FDNYVL_DF['VIO_DATE']).year
# Selecting only required columns
FDNYVL_Selected_DF = FDNYVL_DF[['BOROUGH', 'LATITUDE', 'LONGITUDE', 'ACCT_NUM', 'ACCT_OWNER', 'POSTCODE', 'YEAR']]
# drop null values
map_data = FDNYVL_Selected_DF.dropna()
boroughDF = pd.DataFrame(
    map_data.groupby(['BOROUGH']).size().sort_values(ascending=False).reset_index(name='Violations'))
boroughYearDF = pd.DataFrame(
    map_data.groupby(['BOROUGH', 'YEAR']).size().sort_values(ascending=False).reset_index(name='Violations'))
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
layout_year = dict(
    autosize=True,
    height=500,
    font=dict(color="#ffffff"),
    titlefont=dict(color="#ffffff", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#E0E0E0',
    paper_bgcolor='#262b3d',
    legend=dict(font=dict(size=10), orientation='h'),
    title='FDNY VIOLATIONS by YEAR',

    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="satellite-streets",
        center=dict(
            lon=-73.91251,
            lat=40.7342
        ),
        zoom=9,
    )
)

layout_borough = dict(
    autosize=True,
    height=500,
    font=dict(color="#ffffff"),
    titlefont=dict(color="#ffffff", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#E0E0E0',
    paper_bgcolor='#262b3d',
    legend=dict(font=dict(size=10), orientation='h'),
    title='FDNY VIOLATIONS by BOROUGH'
)
layout_map = dict(
    autosize=True,
    height=500,
    font=dict(color="#ffffff"),
    titlefont=dict(color="#ffffff", size='14'),
    margin=dict(
        l=300,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#CCFFCC',
    paper_bgcolor='#262b3d',
    legend=dict(font=dict(size=10), orientation='h'),
    title='FDNY OPEN VIOLATIONS',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="open-street-map",
        center=dict(
            lon=-73.948776,
            lat=40.676736
        ),
        zoom=9,
    )
)


app.layout = html.Div([
    html.Div([html.H2('FIRE DEPARTMENT NEW YORK CITY OPEN VIOLATIONS',
                      style={'color': '#ffffff', 'fontSize': 30}),
              html.Label("Select a BOROUGH"),
              dcc.RadioItems(
                  options=[
                      {"label": "BRONX", "value": 'BX'},
                      {"label": "BROOKLYN", "value": 'BK'},
                      {"label": "MANHATTAN", "value": 'MN'},
                      {"label": "QUEENS", "value": 'QN'},
                      {"label": "STATEN ISLAND", "value": 'SI'}
                  ],
                  value='BX',
                  id="boroughItems",
                  style={"max-width": "800px", "display": "flex", 'align': 'left', 'backgroundColor': "#262b3d"})
              ],
             style={'backgroundColor': '#262b3d', 'color': '#ffffff'}),
    html.Div([
        dcc.Dropdown(
            id='zipDropdown',
            options=[{'label': i, 'value': i} for i in map_data.POSTCODE.sort_values().unique()],
            value=0,
            placeholder='Select a ZIP Code',
            style={'width': '50%', 'backgroundColor': "#262b3d", 'color': 'green'}
        )
    ], style={'backgroundColor': '#262b3d', 'color': '#ffffff'}),
    html.Div([
        dcc.Graph(id="map", figure={
            'layout': {
                'height': 1000
            }}),
    ], style={'width': '60%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id="bar-year"),
        dcc.Graph(id='bar-borough'),
    ], style={'width': '40%', 'align': 'right', 'display': 'inline-block'}),
    html.Div([html.H1('FDNY OPEN VIOLATIONS DENSITY', style={'color': '#ffffff', 'fontSize': 30, 'backgroundColor': "#262b3d"})]),
    
    html.Div([
    dcc.Graph( id="output-graph2"),
        ], style={'width': '95%',  'display': 'inline-block'}),
    html.Div([
    dcc.Slider(
        id='year-slider',
        min=min(boroughYearDF.YEAR) ,
        max=max(boroughYearDF.YEAR),
        step=1,
        value=min(boroughYearDF.YEAR),
        vertical='True',
        tooltip = { 'always_visible': True }
    )
],
    
    style={'width': '10%', 'align': 'right', 'display': 'inline-block', 'width':'50px', 'height':'450px'})
])

################################################################

#fig = go.Figure(go.Densitymapbox(lat=map_data['LATITUDE'], lon=map_data['LONGITUDE'],  radius=3))

#fig.update_layout(margin={"r":1,"t":0,"l":0,"b":0})
###########################################################################
@app.callback(dash.dependencies.Output('output-graph2', 'figure'),
              [dash.dependencies.Input('year-slider', 'value')])


def update_value(value):
    DF=map_data[map_data.YEAR > value]
    
    fig = go.Figure(go.Densitymapbox(lat=DF['LATITUDE'], lon=DF['LONGITUDE'],  radius=3))
    fig.update_layout(mapbox_style="stamen-terrain",mapbox_center_lon=-74.013026,mapbox_center_lat=40.711085,mapbox_zoom=9)
    fig.update_layout(margin={"r":1,"t":0,"l":0,"b":0})
    
    return fig

#########################################################################

@app.callback(dash.dependencies.Output('map', 'figure'),
              [
                  dash.dependencies.Input('zipDropdown', 'value'),
                  dash.dependencies.Input('boroughItems', 'value')
              ])
def update_value(ZipCode, Borough):
    graphData = map_data[map_data['BOROUGH'] == Borough]
    graphData = graphData[graphData['POSTCODE'] == ZipCode]
    if Borough == 'SI':
        cen_lat = 40.580231
        cen_lon = -74.163300 
        
    
    elif Borough == 'BK':
        cen_lat = 40.676345
        cen_lon = -73.946373
     
    elif Borough == 'BX':
        cen_lat = 40.859169
        cen_lon = -73.857759
       
    elif Borough == 'MN':
        cen_lat = 40.711085
        cen_lon = -74.013026
    elif Borough == 'QN':
        cen_lat = 40.729031
        cen_lon = -73.811462
       
    else:
        cen_lat = 40.711085
        cen_lon = -74.013026

    return ({
        'data': [{
            'lat': graphData.LATITUDE,
            'lon': graphData.LONGITUDE,
            'type': 'scattermapbox',
            'selectedpoints': 0,
            'selected': {
                'marker': {'color': '#85144b'}
            }
        }],
        'layout': {
            'mapbox': {
                'center': {
                    'lat': cen_lat,
                    'lon': cen_lon
                },
                'zoom': 9,
                'style': 'open-street-map',
                'accesstoken': 'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2oyY2M4YW55MDF1YjMzbzhmemIzb290NiJ9.sT6pncHLXLgytVEj21q43A'
            },
            'margin': {'l': 0, 'r': 0, 't': 0, 'b': 0}
        }
    }
    )

@app.callback(dash.dependencies.Output('bar-borough', 'figure'),
              [dash.dependencies.Input('boroughItems', 'value')])
def update_graph_a(value):
    # prepare figure_a from value
    graphData = boroughYearDF[boroughYearDF['BOROUGH'] == value]
    return ({'data': [
        {'x': graphData.YEAR, 'y': graphData.Violations, 'type': 'bar'}
    ],
        'layout': layout_year
    }
    )


@app.callback(dash.dependencies.Output('bar-year', 'figure'),
              [dash.dependencies.Input('zipDropdown', 'value')])
def update_graph_b(value):
    return ({'data': [
        {'x': boroughDF.BOROUGH, 'y': boroughDF.Violations, 'type': 'bar'}
    ],
        'layout': layout_borough
    }
    )


@app.callback(dash.dependencies.Output('zipDropdown', 'options'),
              [dash.dependencies.Input('boroughItems', 'value')])
def update_zip_dropdown(borough):
    # prepare figure_a from value
    zipDF = map_data[map_data['BOROUGH'] == borough]
    
    options = [{'label': int(opt), 'value': int(opt)} for opt in zips]
    return (options)


if __name__ == '__main__':
    app.run_server()
