# Fuse CWatM Bhima Climate
# PB 30/11/22

import dash

from dash import dcc,html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

import numpy as np
import json

import pandas as pd
import xarray as xr
from collections import OrderedDict

import datetime
import time

#from itertools import product
#from plotly.subplots import make_subplots
#import plotly.offline as offline
#from ipywidgets import HBox, VBox, Button, widgets

#import warnings
#warnings.filterwarnings('ignore')

#-----------------------------------------------

# Initialize app

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SPACELAB])
server = app.server
mapbox_access_token = 'pk.eyJ1IjoiYnVwZSIsImEiOiJjanc3ZnpmMDEwYm1vNDNsbW15bXh3Y2RlIn0.DFOGHx9u2JThJKBQo1zDMQ'
mapbox_style = "mapbox://styles/bupe/cjw7g6cax0hem1cqy9vc9vln4"
colorapp = {"background": "#ffffff", "text": "#082255", "text2": "#082255"}

# ------------------------------------
downloadclick = [None]
compare_years = 30

#--------------------------------------

def createscatter(yy):

    xx = np.arange(1990,2056)
    colors1 = ['lightslategray',] * len(xx)

    scale = [[22,32],[0,140],[0,100],[0,4000],[0,366],[0,80],[0,30],[0,10]]

    # linear trend
    #yy = yyy[0,0,0,:,40]

    #print (xx.shape,yy.shape)
    m,b =np.polyfit(xx,yy,1)
    m1 = yy[:30].mean()
    m2 = yy[35:67].mean()
    m11 = [m1]*30
    m22 = [m2]*31

    #colorbar = np.where(yy > m1,"darkred","lightslategray")
    #colorbar = np.where(yy > m1+1.,"crimson",colorbar).tolist()

    data2a = go.Bar(name='avg. Temp [°C]', x=xx, y=yy, hovertemplate='%{x}<br>%{y:.1f}')
    #data2b = go.Scatter(x=xx,y= xx*m+b, name ="Trend")

    data2b = go.Scatter(x=xx[0:30],y=m11,
                       customdata=[2.444],
                       name ="Average 1990-2020: "+ f'{m1:.2f}'+ '°C',
                       marker_color ="black",
                       hovertemplate='%{x}<br>%{y:.1f}')
    data2c = go.Scatter(x=xx[35:67],y=m22,
                       customdata=[2.444],
                       name ="Average 2025-2055: "+ f'{m2:.2f}'+ '°C',
                       marker_color ="black",
                       hovertemplate='%{x}<br>%{y:.1f}')

    #data2c = go.Scatter(x=xx[:30],y= xx[:30]*0+m1, name="Mean")
    #data2d = go.Scatter(x=xx[124-compare_years:124],y= xx[39-compare_years:39]*0+m2, marker_color ="black", name="Mean period", mode='lines')

    q1 = np.mean(yy[0:30],axis=0)
    q2 = np.mean(yy[35:67],axis=0)
    colorbar = np.where(yy > q1,"darkred","lightslategray")
    data2a.marker.color = colorbar

    layout2 = dict(title = 'Station x')
    #data2a.marker.color=colorbar
    data = go.Figure(data=[data2a,data2b,data2c],layout=layout2)
    fig = go.Figure(data=[data2a, data2b, data2c], layout=layout2)
    #fig2.update_yaxes(range=[yy.min(), yy.max()])
    fig.update_yaxes(range=scale[0])

    fig.update_layout(
        plot_bgcolor=colorapp["background"],
        paper_bgcolor=colorapp["background"],
        height = 422,
        width = 500,
        legend=dict(x=0, y=1.0),
    )

    return fig

# -------------------------------------------------

input_rcp = "jub_allvar3.npy"
input_json = "ub_district1.json"
input_csv = "upper_bhima.csv"

ub = pd.read_csv(input_csv, index_col=0)
# make numpy array for hover text
ub1 = np.array(ub)
ub1[0:43] = ub1[1:44]

districts = ub['name_3'].values.tolist()
districts[0:43] = districts[1:44]

with open(input_json) as f:
    ub_districts = json.load(f)

zz = ub.t1.to_numpy()
no_district = len(zz)
#-------------------------------------------

rcp = ["RCP 4.5", "RCP 8.5"]
gcm = ["All","GFDL-ESM2M","MIROC5_ISIMIP", "MPI_REMO2009_ISIMIP3"]
analysis = ["Avg.Temperature","Tmax Days ≥38°C","Tmax Days ≥40°C","Avg. Precipitation","P daily <0.01mm","P daily ≥20mm","P daily ≥50mm","P daily ≥100mm"]
scale = [[22,32],[0,140],[0,100],[0,4000],[0,366],[0,80],[0,30],[0,10]]


# variable + analysis,gcm, rcp,year, district)
# (4,3,2,2056 - 1990, 44))
yyy = np.load(input_rcp)
yyy[:,:,:,:,0:43] = yyy[:,:,:,:,1:44]

hovertext = '<b>District: </b> %{customdata[1]}<br><b>Tehsil:   </b> %{customdata[2]}'
hovertext += '<extra><b>1990-2020</b>: %{customdata[4]:.1f}<br><b>2025-2055</b>: %{customdata[5]:.1f}<br><b>Difference</b>: %{customdata[6]:.1f}</extra>'

yy = yyy[0,0,0,:,:]
q1 = np.mean(yy[0:30,:],axis=0)
q2 = np.mean(yy[36:66,:],axis=0)
qdiff = q2 - q1

ub1[:,4] = q1
ub1[:,5] = q2
ub1[:,6] = qdiff


#---------------------------------------------------------

GCMS = ["All","GFDL","MIROC5","MPI"]
RCPS = ["RCP45","RCP85"]
GCMindex1 = [0]

figtype = ["avgTemp","Temp38","Temp40","avgP","P001","P020","P050","P100"]
periode = [" 1990-2020"," 2025-2055"]

unit = ['°C','days','days','mm','days','days','days','days']
trigger = [0,0,0,0,0]


# -------------------------------------------------------

yy = yyy[0,0,0,:,40]
fig = createscatter(yy)

ii=1
#---------------------------------------------------------

# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------

nav_item = dbc.NavItem(dbc.NavLink("Link", href="#"))

logo = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                children=[
                    dbc.Row(
                        [
                            dbc.Col(html.Img(id="logo", src=app.get_asset_url("iiasa_logo.png"), height="60"),md=8),
                            dbc.Col(html.Hr(),md=2),
                            dbc.Col(dbc.NavbarBrand("FUSE Bhima Climate Dashboard", className="ml-1"),md=2),
                        ],
                        align="center"
                    ),
                ],
                href="https://fuse.stanford.edu/",
            ),

            dbc.NavbarToggler(id="navbar-toggler1"),
            dbc.Collapse(
                #dbc.Nav(
                #    [nav_item, dropdown], className="ml-auto", navbar=True
                #),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    #color="primary",
    color="primary",
    dark=True,
    className="mb-5",
    #fixed = "top",
    #sticky = "top",
)

jumbotron = dbc.Container(
    [
        dcc.Markdown('''
                    ##### Info
                    
                    **FUSE: Belmont Forum Collaborative Research: Food-water-energy for Urban Sustainable Environments**
                    
                    [FUSE (Food-water-energy for Urban Sustainable Environments)](https://fuse.stanford.edu/) is a transdisciplinary 3-year research project (2018-2021) involving the Food-Water-Energy Nexus (FWE) in Pune (India).
                     
                    The project will develop a long-term systems model that can be used to identify viable paths to sustainability.
                    It brings together scientists, engineers, economists, and stakeholder engagement experts from
                    
                    - [Stanford University in California, USA](https://www.stanford.edu/) 
                    - [IIASA (International Institute for Applied Systems Analysis) in Laxenburg, Austria](https://www.iiasa.ac.at/) 
                    - [UFZ (Helmholtz Centre for Environmental Research) in Leipzig, Germany](https://www.ufz.de/) 
                    - [ÖFSE (Austrian Foundation for Development Research) in Vienna, Austria](https://www.oefse.at/) 
                    
                    
                    
                    The project is a not-for-profit research effort and is part of the Sustainable Urbanisation Global Initiative of JPI Urban Europe and the Belmont Forum. 

                '''),
        html.Hr(),
        dcc.Markdown('''
            by [IIASA BNL/WAT Security](https://iiasa.ac.at/programs/biodiversity-and-natural-resources-bnr/water-security/)''')
    ],
    style={'fontSize': 12, 'font-family':'sans-serif', 'line-height': 15}
)


drop1_dbc = dbc.Form([
                html.P(
                    id="drop1-text",
                    children="",
                ),
                dcc.Dropdown(
                    id = "drop1",
                    options = [
                        {"label": "GCM: All RCPs + GCMs", "value": "All"},
                        {"label": "GCM: GFDL-ESM2M", "value": "GFDL"},
                        {"label": "GCM: MIROC5_ISIMIP", "value": "MIROC5"},
                        {"label": "GCM: MPI_REMO2009_ISIMIP3", "value": "MPI"},
                    ],
                    value='All',
                    searchable=False,
                    clearable=False
                ),
])

drop2_dbc = dbc.Form(
    className="drop_box2",
    children=[
        html.P(
            id="drop2-text",
            children="",
        ),
        dcc.Dropdown(
            id="drop2",
            options=[
                {"label": "RCPs: RCP4.5", "value": "RCP45"},
                {"label": "RCPs: RCP8.5", "value": "RCP85"},
            ],
            value='RCP45',
            searchable=False,
            clearable=False
        ),
    ],
)

drop3_dbc = dbc.Form(
    className="drop_box3",
    children=[
        html.P(
            id="drop3-text",
            children="",
        ),
        dcc.Dropdown(
            id="drop3",
            options=[
                {"label": "Variable: Avg. Temperature", "value": "avgTemp"},
                {"label": "Variable: Tmax Days ≥38°C", "value": "Temp38"},
                {"label": "Variable: Tmax Days ≥40°C", "value": "Temp40"},
                {"label": "Variable: Avg. Precipitation", "value": "avgP"},
                {"label": "Variable: P daily no rain", "value": "P001"},
                {"label": "Variable: P daily ≥20mm", "value": "P020"},
                {"label": "Variable: P daily ≥50mm", "value": "P050"},
                {"label": "Variable: P daily ≥100mm", "value": "P100"},
            ],
            value='avgTemp',
            searchable=False,
            clearable=False
        ),
    ],
)

radio_dbc = dbc.Form([
                html.P(
                    id="radio-text",
                    children="",
                    style={'clear': 'both'}
                ),
            dcc.RadioItems(
                [
                    {
                        "label": html.Div(['1990-2020  --'], style={'font-size': 15}),
                        "value": "1990-2020",
                    },
                    {
                        "label": html.Div(['2025-2055'], style={'font-size': 15}),
                        "value": "2025-2055",
                    },
                ],
                value='1990-2020',
                inline = True,
                id="year-radio",

            )
])






"""

                    id="year-radio",


                    options=['1990-2020', '2025-2055'],
                    value='1990-2020',
                    inline=False,
                )
"""


map_dbc = dbc.Form([
        dcc.Graph(
            id="bhima-choropleth",
            config={'displayModeBar': False},
            figure=dict(
                layout=dict(
                    mapbox=dict(),
                    plot_bgcolor=colorapp["background"],
                    paper_bgcolor=colorapp["background"],
                    autosize=False,
                    # showlegend=False,
                    #uirevision
                ),
            ),
        ),
])

scatter_dbc = dbc.Form([
        dcc.Markdown(""),
        html.Div(
            id="scatter1",
            children=[
                dcc.Graph(id='scatterplot1',
                          config={'displayModeBar': False},
                          style={'height': 400, 'width': 580}
                          #style={'height': 350}
                          )],
        ),
])

#-------------------------------------------------------------------------------
# LAYOUT
app.layout = dbc.Container([
        #dcc.Store(id='sunburstlevel'),

        html.Div([logo]),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(html.H5("Future Climate Bhima Basin")),
                        dbc.Row(html.Div(id='x1')),
                        dbc.Row(html.Div(id='x2')),
                        dbc.Row(html.Div(id='my-output1'))

                    ],width=7),

                dbc.Col(
                    [
                        dbc.Row(drop2_dbc),
                        dbc.Row(drop1_dbc),
                        dbc.Row(drop3_dbc),
                        dbc.Row(radio_dbc)
                    ],width=3),
                dbc.Col(html.H5(" "),width = 2),
            ],
        ),

        dbc.Row(
            [
                dbc.Col(map_dbc),
                dbc.Col(scatter_dbc),
            ],
        ),

        dbc.Row(
            [
                #dbc.Col(html.Div(id='my-output1')),
                dbc.Col(html.Div(id='x4')),
                #dbc.Col(html.Div(id='x5')),
                #dbc.Col(html.Div(id='x6'))
                #dbc.Col(html.Div([html.Button("Download Daten für diese Zelle als csv", id="btn_data"), dcc.Download(id="download-data")])),
            ],
        ),
        html.H1(""),

    dbc.Row(
        [
            dbc.Col(html.Div([jumbotron], className="info")),
            dbc.Col(html.Div([
                html.Button("    Download documentation", id="btn_pdf"), dcc.Download(id="download-pdf"),
            ])),
        ],
    ),
],
    #fluid = True,
)

#----------------------------
# ScatterPLOT

# update scatterplot
@app.callback(
    Output('scatterplot1', 'figure'),
    Output(component_id='my-output1', component_property='children'),
    [Input("bhima-choropleth", "clickData"),
     Input('drop1', 'value'),
     Input('drop2', 'value'),
     Input('drop3', 'value')]
)
def update_scatter1(input_value,d1value,d2value,d3value):

    # dropbox GCM
    GCMindex = GCMS.index(d1value)
    RCPindex = RCPS.index(d2value)
    figindex = figtype.index(d3value)

    if input_value is None:
        inds = 40
    else:
        inds = int(input_value['points'][0]['pointNumber'])

    trigger[0] = figindex
    trigger[1] = GCMindex
    trigger[2] = RCPindex
    trigger[4] = inds

    #text = rcp[RCPindex] + " - " + gcm[GCMindex] + " - " + analysis[figindex]
    #text = str(GCMindex) + str(RCPindex) + str(figindex) + " " + str(inds)+ " " + districts[inds]

    text = dbc.Container(
        [
            dcc.Markdown(". "),
            dcc.Markdown("Tehsil: " + districts[inds]),
            dcc.Markdown("RCP: " + rcp[RCPindex]),
            dcc.Markdown("GCM: "+ gcm[GCMindex]),
            dcc.Markdown("Variable: " + analysis[figindex]),
        ],
        style={'fontSize': 15, 'textAlign': 'left'}
    )

    yy = yyy[trigger[0], trigger[1], trigger[2], :, trigger[4]]
    fig = createscatter(yy)

    bar1 = fig.data[0]
    bar2 = fig.data[1]
    bar3 = fig.data[2]

    # districts
    fig.layout.title = 'Tehsil: ' + districts[inds]

    # c = list(bar.marker.color)
    # with fig2.batch_update():
    # bar.marker.color = color1[inds]

    bar1.y = yy
    bar1.name = analysis[trigger[0]]

    # m,b =np.polyfit(xx,yy,1)
    m1 = yy[:30].mean()
    m11 = [m1] * 30
    bar2.y = m11
    bar2.name = "Average 1990-2020: " + f'{m1:.1f}' + unit[trigger[0]]

    m2 = yy[35:67].mean()
    m22 = [m2] * 31
    bar3.y = m22
    bar3.name = "Average 2025-2055: " + f'{m2:.1f}' + unit[trigger[0]]

    colorbar = np.where(yy > m1,"darkred","lightslategray")
    bar1.marker.color = colorbar

    fig.update_yaxes(range=scale[trigger[0]])
    fig.update_layout(
        plot_bgcolor=colorapp["background"],
        paper_bgcolor=colorapp["background"],
        height = 422,
        width = 500,
        legend=dict(x=0, y=1.0),
        yaxis_title=analysis[trigger[0]] +" [" + unit[trigger[0]] + "]",
    )

    return fig,text


# -------------------------------------------------
# map Salzburg map
@app.callback(
    Output("bhima-choropleth", "figure"),
    Input('drop1', 'value'),
    Input('drop2', 'value'),
    Input('drop3', 'value'),
    [Input("year-radio", "value")],

)
def display_map(d1value,d2value,d3value,year):

    trigger[0] = figtype.index(d3value)
    trigger[1] = GCMS.index(d1value)
    trigger[2] = RCPS.index(d2value)

    q1 = np.mean(yyy[trigger[0],trigger[1],trigger[2],0:30,:],axis=0)
    q2 = np.mean(yyy[trigger[0],trigger[1],trigger[2],36:66,:],axis=0)

    if year == "1990-2020":
        zz = q1
    else:
        zz = q2
    zzmin = scale[trigger[0]][0]
    zzmax = scale[trigger[0]][1]

    ub1[:, 4] = q1
    ub1[:, 5] = q2
    ub1[:, 6] = q2 - q1

    # https://plotly.com/python/builtin-colorscales/
    # fig = go.Figure(go.Choroplethmapbox(name="Global Basins", geojson=global_basins, locations=globalinfo.index, z=zzz,
    # portland balance
    fig = go.Figure(go.Choroplethmapbox(name="Upper Bhima", geojson=ub_districts, locations=ub.index, z=zz,
                                colorscale="Portland", zmin=zzmin, zmax=zzmax, marker_opacity=0.5, customdata=ub1,
                                hovertemplate=hovertext))

    fig.update_layout(mapbox_accesstoken=mapbox_access_token,
                   mapbox_style= "mapbox://styles/bupe/cjw7g6cax0hem1cqy9vc9vln4",
                   mapbox_center={"lat": 18.0, "lon": 74.8},
                   mapbox_pitch=0, mapbox_zoom=6.6,
                   margin={"r": 0, "t": 0, "l": 0, "b": 0},
                   height= 400,
                   autosize=False,
                   uirevision=True,
                   dragmode=False,
                   )

    return fig
#------------------------------
"""
# if all rcp and GCM set RCP to 4.5
@app.callback(
    Output('drop2', 'value'),
    Input('drop1', 'value'),
    [State('drop2', 'value')],
)
def change_rcp(d1value,d2value):
    gcm = GCMS.index(d1value)
    rcp = RCPS[0]
    if gcm == 0:
        return rcp
    else:
        return d2value
"""

#----------------------------------
@app.callback(
    Output("download-pdf", "data"),
    Input("btn_pdf", "n_clicks"),
    prevent_initial_call=True,
)
def downfunc(n_clicks):
    return dcc.send_file(
        "./assets/fuse_bhima_climate_docu.pdf"
    )
# ------------------------------------

if __name__ == "__main__":
    app.run_server(debug=True)