######################################################################################################
# Package Import
######################################################################################################
import pandas as pd
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import json
import datetime as dt

######################################################################################################
# Define Inputs
######################################################################################################

# Set year range and default selections
Min_Year = 2010
Max_Year = 2021
Selected_Year = 2017
start_date = dt.date(Min_Year - 1, 10, 1)
end_date = dt.date(Max_Year + 1, 2, 1)
Selected_Bedroom = '3 Bedroom'

# Style sheet
Tile_Border = 'thick double #565D73'
Border_Radius = '7px'
Tile_Fill_Clr = '#3A3F4E'
Text_Clr_Desc = 'white'
Text_Clr_Drp = 'black'
Main_Font = 'Arial'
Font_Size_Header = 54
Font_Size_Title = 20
Font_Size_Desc = 16
Font_Size_Tick = 12

######################################################################################################
# Import and Prepare Data
######################################################################################################

# Import housing data
df_choro = pd.read_csv("df_choro.csv", dtype={"CountyCode": "string"})
df_line = pd.read_csv("df_line.csv", dtype={"CountyCode": "string"})

# import county geo data
counties = json.load(open('counties.json'))


######################################################################################################
# Define App Layout
######################################################################################################
# Define slider marks generator


def get_marks(start, end, color):
    result = {}

    for i in range(start, end + 1):
        result[i] = {'label': str(i), 'style': {'color': color, 'font-size': '15px'}}

    return result


# App instance
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

# App layout
app.layout = html.Div([
    dbc.Row([
        dbc.Col(
            html.P(
                'US Housing Values',
                style={
                    'font-size': Font_Size_Header,
                    'font-family': Main_Font,
                    'margin-bottom': '0px'
                }
            ),
            width={
                'size': 6,
                'offset': 1
            },
            style={'margin-bottom': '0px'}
        )],
        style={
            'margin-bottom': '0px',
            'margin-top': '30px',
        }
    ),

    dbc.Row([
        dbc.Col(
            html.P(
                "* Value estimated using Zillow's home value index.",
                style={
                    'font-size': Font_Size_Desc,
                    'font-family': Main_Font,
                    'margin-bottom': '0px'
                }
            ),
            width={
                'size': 6,
                'offset': 1
            },
            style={'margin-bottom': '0px'}
        ),
        dbc.Col([
            dbc.Button(
                'View in Github',
                href='https://https://github.com/chrismdavis/Housing-Dashboard',
                external_link=True,
                color='secondary',
                style={
                    'border': 'solid white',
                    'font': Main_Font
                }
            )],

            width={
                'size': 1,
                'offset': 3
            },
            style={'margin-bottom': '0px'}
        )],
        style={
            'margin-bottom': '10px',
            'margin-top': '0px'
        },

    ),

    dbc.Row([
        dbc.Col([
            html.P(
                id="slider-text",
                children="Drag the slider to select year:",
                style={  # Slider Text Style
                    'color': Text_Clr_Desc,
                    'font-size': Font_Size_Desc,
                    'font-family': Main_Font
                }
            ),
            dcc.Slider(
                id="years_slider",
                min=Min_Year,
                max=Max_Year,
                marks=get_marks(Min_Year, Max_Year, Text_Clr_Desc),
                value=Selected_Year
            )],
            width={
                'size': 6,
                'offset': 1,
                'order': 1},
            style={  # Slider Tile Style
                'border': Tile_Border,
                'border-radius': Border_Radius,
                'background-color': Tile_Fill_Clr,
                'padding-top': '10px',
                'padding-bottom': '10px',
                'padding-left': '10px',
                'padding-right': '10px',
                'margin-right': '10px'
            }
        ),

        dbc.Col([
            html.P(
                id='dropdown-text',
                children='Select Housing Size:',
                style={  # Dropdown Text Style
                    'color': Text_Clr_Desc,
                    'font-size': Font_Size_Desc,
                    'font-family': Main_Font
                }
            ),

            dcc.Dropdown(
                id='dropdown_bdr',
                placeholder='Bedroom_Dropdown',
                options=[
                    {'label': '1 Bedroom', 'value': '1 Bedroom'},
                    {'label': '2 Bedroom', 'value': '2 Bedroom'},
                    {'label': '3 Bedroom', 'value': '3 Bedroom'}],
                value=Selected_Bedroom,
                style={  # Dropdown Style
                    'color': Text_Clr_Drp,
                }
            )],
            width={
                'size': 4,
                'offset': 0,
                'order': 2},
            style={  # Dropdown Tile Style
                'border': Tile_Border,
                'border-radius': Border_Radius,
                'background-color': Tile_Fill_Clr,
                'padding-top': '10px',
                'padding-bottom': '10px',
                'padding-left': '10px',
                'padding-right': '10px'

            }
        )],
        style={  # Row 2 Style
        }
    ),

    dbc.Row([
        dbc.Col(
            [
                dcc.Loading(
                    id='loading',
                    fullscreen=True,
                    color='#198E8A',
                    type='cube',
                    style={'background-color': 'rgba(50,50,50,0.5)'}
                ),
                dcc.Graph(
                    id='fig_map',
                    style={  # Choropleth Style
                        'height': '100%'
                    }
                )
            ],
            width={
                'size': 6,
                'offset': 1,
                'order': 1
            },
            style={  # Choropleth Tile Style
                'border': Tile_Border,
                'border-radius': Border_Radius,
                'background-color': Tile_Fill_Clr,
                'height': '65vh',
                'padding-top': '10px',
                'padding-bottom': '10px',
                'padding-left': '10px',
                'padding-right': '10px',
                'margin-right': '10px'
            }
        ),

        dbc.Col(
            dcc.Graph(
                id='fig_line',
                style={  # Line Graph Style
                    'border-radius': Border_Radius,
                    'height': '100%'
                }
            ),
            width={
                'size': 4,
                "offset": 0,
                'order': 2},
            style={  # Line Graph Tile Style
                'border': Tile_Border,
                'border-radius': Border_Radius,
                'background-color': Tile_Fill_Clr,
                'padding-top': '10px',
                'padding-bottom': '10px',
                'padding-left': '10px',
                'padding-right': '10px',
                'height': '65vh'
            }
        )],
        style={  # Row 3 Style
            'margin-top': '10px'
        }
    )]
)


# Callbacks
@app.callback(
    [Output('fig_map', 'figure'),
     Output('loading', 'parent_style')],
    [Input('years_slider', 'value'),
     Input('dropdown_bdr', 'value')]
)
def update_map(year_val, bdr_val):
    fig_map = px.choropleth_mapbox(
        df_choro[(df_choro.Year == year_val) & (df_choro.Size == bdr_val)],
        geojson=counties,
        locations='CountyCode',
        color='Home Value',
        color_continuous_scale='Portland',
        mapbox_style='carto-positron',
        range_color=(50000, 500000),
        zoom=3.1,
        center={"lat": 37.0902, "lon": -95.7129},
        opacity=0.8,
        labels={'L2': 'L1'},
        hover_data=['StateName', 'RegionName'],
        title='Average House Value by County (' + str(year_val) + ' | ' + bdr_val + ')'
    )

    fig_map.update_layout(
        legend={
            'font_color': 'black'
        },
        paper_bgcolor=Tile_Fill_Clr,
        margin={"r": 10, "t": 30, "l": 10, "b": 10},
        clickmode="event+select",
        font_family=Main_Font,
        font_color=Text_Clr_Desc,
        title_font_size=Font_Size_Title,
        font_size=Font_Size_Desc
    )

    return fig_map, {'display': 'inline'}


@app.callback(
    Output('fig_line', 'figure'),
    [Input('dropdown_bdr', 'value'),
     Input('fig_map', "selectedData")]
)
def update_line(bdr_val, slct_data):
    if slct_data is None:
        fig_line = px.line(title="Average Housing Price By Year")
        fig_line.add_annotation(
            text="Select counties in map. <br> Hold shift key to select multiple. <br> (Max selection = 8).",
            showarrow=False,
            font_family=Main_Font,
            font_color='black',
            font_size=Font_Size_Title
        )

    else:
        fips_lst = [str(pt["location"].split("<br>")[-1]) for pt in slct_data['points']]
        fig_line = px.line(df_line[(df_line.Size == bdr_val) & (df_line['CountyCode'].isin(fips_lst[:8]))],
                           x="Date",
                           y="Home Value",
                           color='RegionName',
                           title='Average House Value by Year (' + bdr_val + ')')

    fig_line.update_layout(
        legend={
            'x': .02,
            'y': .98,
            'bgcolor': 'rgba(50,50,50,0.5)',
            'bordercolor': 'white',
            'borderwidth': 2
        },
        xaxis_range=[start_date, end_date],
        paper_bgcolor=Tile_Fill_Clr,
        margin={"r": 10, "t": 30, "l": 10, "b": 10},
        font_family=Main_Font,
        font_color=Text_Clr_Desc,
        title_font_size=Font_Size_Title,
        font_size=Font_Size_Desc,
        xaxis_title='Date',
        yaxis_title='Average House Price',
        xaxis={'tickfont': {'size': Font_Size_Tick}},
        yaxis={'tickfont': {'size': Font_Size_Tick}},
    )

    return fig_line


if __name__ == '__main__':
    app.run_server(debug=True)

