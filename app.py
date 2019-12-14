import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table  as dt
import pandas as pd

from plotly import graph_objs as go
from plotly.graph_objs import *
from dash.dependencies import Input, Output, State 


app = dash.Dash(__name__)
server = app.server
app.title = 'FDNY VIOLATIONS'




# API keys and datasets
mapbox_access_token = 'pk.eyJ1IjoiZ3BzaW5naDEyIiwiYSI6ImNrMzNhanQ2ZjBqODMzaW1tbHRxNHBqa20ifQ.ewLqQWO3g2TNM-8NpFhcxw'
df = pd.read_csv("https://raw.githubusercontent.com/gpsingh12/DATA608/master/Final-Project/fdny_vio.csv")
#df = pd.read_csv("C:/Users/Gurpreet/Documents/DATA608/fdny_vio.csv")
df['YEAR'] = pd.DatetimeIndex(df['VIO_DATE']).year
# Selecting only required columns
df1 = df[['BOROUGH', 'LATITUDE', 'LONGITUDE', 'ACCT_NUM', 'ACCT_OWNER', 'POSTCODE', 'YEAR']]
map_data=df1.dropna()
bor = pd.DataFrame(map_data.groupby(['BOROUGH']).size().sort_values(ascending=False).reset_index(name='Violations'))
bor_yr = pd.DataFrame(map_data.groupby(['BOROUGH', 'YEAR']).size().sort_values(ascending=False).reset_index(name='Violations'))


#drop null values



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

layout_bar1 = dict(
    autosize=True,
    height=250,
    font=dict(color="#ffffff"),
    titlefont=dict(color="#ffffff", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#262b3d',
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
        zoom=10,
    )
)

layout_bar2 = dict(
    autosize=True,
    height=250,
    font=dict(color="#ffffff"),
    titlefont=dict(color="#ffffff", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#262b3d',
    paper_bgcolor='#262b3d',
    legend=dict(font=dict(size=10), orientation='h'),
    title='FDNY VIOLATIONS by BOROUGH',
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


layout_map = dict(
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
    plot_bgcolor='#262b3d',
    paper_bgcolor='#262b3d',
    legend=dict(font=dict(size=10), orientation='h'),
    title='FDNY OPEN VIOLATIONS',
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



app.layout = html.Div([
    html.Div([html.H2('FIRE DEPARTMENT NEW YORK CITY OPEN VIOLATIONS',
                      style={'color': '#ffffff', 'fontSize': 30}),
    html.Label("Select a BOROUGH")],
             style={'backgroundColor' : '#262b3d', 'color':'#ffffff'}),
    html.Div([
        dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in map_data.BOROUGH.unique()],
        value='BX',
        style={'width':'50%', 'backgroundColor' : "#ffffff", 'color':'red'}
    )
    ]),
    html.Div([
    dcc.Graph( id="output-graph"),
        ], style={'width': '60%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id="bar-graph"),
        dcc.Graph(id='bar2-graph'),
        ],style={'width': '40%', 'align': 'right', 'display': 'inline-block'}),
])

@app.callback(dash.dependencies.Output('output-graph', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])


def update_value(value):
    test = map_data[map_data['BOROUGH']==value]

    return({'data': [
        {'lat': test.LATITUDE, 'lon': test.LONGITUDE, 'type': 'scattermapbox',
        'hoverinfo': 'text',
        'hovertext': [["ACCT_OWNER: {} <br>ACCT_NUM: {} <br>".format(i,j,)]
                                for i,j in zip(test['ACCT_OWNER'], test['ACCT_NUM'])]},
        
       ],
        'layout': layout_map
        }
    )


@app.callback(dash.dependencies.Output('bar-graph', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])

def update_graph_a(value):
    # prepare figure_a from value
    test1 =bor_yr[bor_yr['BOROUGH']==value]
#    test1 = test1.nlargest(20,'Violations')

    return({'data': [
        {'x': test1.YEAR, 'y': test1.Violations, 'type': 'bar'}
        ],
        'layout': layout_bar1
        }
    )

@app.callback(dash.dependencies.Output('bar2-graph', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])

def update_graph_b(value):
    
    return({'data': [
        {'x': bor.BOROUGH, 'y': bor.Violations, 'type': 'bar'}
        ],
        'layout': layout_bar2
        }
    )


if __name__ == '__main__':
    app.run_server(debug=True)