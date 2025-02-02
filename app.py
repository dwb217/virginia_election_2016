######### Import your libraries #######
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import *

###### Import a dataframe #######
df = pd.read_pickle('virginia_totals.pkl')
options_list=list(df['jurisdiction'].value_counts().sort_index().index)

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='VA 2016'

####### Layout of the app ########
app.layout = html.Div([
    html.H3('2016 Presidential Election: Vote Totals by jurisdiction'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in options_list],
        value=options_list[0]
    ),
    html.Br(),
    dcc.Graph(id='display-value'),
    html.Br(),
    html.A('Code on Github', href='https://github.com/austinlasseter/virginia_election_2016'),
    html.Br(),
    html.A('Data Source', href='https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/LYWX3D')
])


######### Interactive callbacks go here #########


@app.callback(dash.dependencies.Output('display-map', 'figure'),
              [dash.dependencies.Input('dropdown', 'value')])
def juris_highlighter(juris_name):
    df['selected']=np.where(df['jurisdiction']==juris_name, 1, 0)
    fig = go.Figure(go.Choroplethmapbox(geojson=counties,
                                        locations=df['FIPS'],
                                        z=df['selected'],
                                        # colorscale=['blues'],
                                        text=df['jurisdiction'],
                                        hoverinfo='text',
                                        zmin=0,
                                        zmax=1,
                                        marker_line_width=.5
                                        ))
    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=5.8,
                      mapbox_center = {"lat": 38.0293, "lon": -79.4428})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

######### Run the app #########
if __name__ == '__main__':
    app.run_server(debug=True)
