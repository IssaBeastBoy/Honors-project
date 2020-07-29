import dash
import dash_bootstrap_components as dbc 
import dash_core_components as dcc 
import dash_html_components as html 

from Methods import Add_CheckBoxMW
from MW_Topbuttons import SU_button , AV_button, DrugA_button, Variant_information


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.GRID, dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

storeOptions = []

def MainWindow(): 
    layout = html.Div(
            [  dbc.Row(
                [
                    dbc.Col(
                        html.Div(SU_button), width=4
                    ),
                    dbc.Col(
                        html.Div(AV_button), width=4
                    ),
                    dbc.Col(
                        html.Div(DrugA_button), width=4
                    )
                ],
                justify="between",
            ),
                dbc.Row(
                [Variant_information]
            ),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Loading(
                    type = 'circle',
                    children = html.Div(
                                    id = 'Plot',
                                    style ={
                                            'width': '100%',
                                            'height': '200px'
                                        }
                                )
                )], width=9
                )
              , 
                dbc.Col([
                    dbc.Row([
                             html.Div(id = 'Delete_buttonSpace'),
                            html.Div(id = 'CheckBox', style={'display': 'none'})
                        ])                
              ,
                    dbc.Row([
                        dbc.Col(
                            dbc.Nav(
                        [
                        dbc.NavItem(
                        dbc.NavLink("Upload", active= True, href='UpLoad')
                        )
                        ],
                        pills= True )
                        ), 
                        dbc.Col([
                        dbc.Button('Delete', color='danger', id ='Delete_button')])
                        ],
                            justify="around",),
                    html.Br(),
                    dbc.Row([                            
                            html.Div(html.Center(html.B('Available plots')))
                            ]),
                    dbc.Row([
                                dcc.RadioItems(
                                options=[
                                    {'label':'Bar Graph', 'value': '1'},
                                    {'label':'Scatter Plot', 'value': '2'},
                                    {'label': 'Orthographic Map', 'value': '3'},
                                    {'label': 'Natural Earth Map', 'value': '4'},
                                    {'label': 'Continential Map', 'value': '5'},
                                ],
                                id = 'Plot_Options',
                                labelStyle={'display': 'block'}
                            )
                            ]
                    )
                ], width=3)  
            ],
                justify="between",)
            ]
        )
    return layout

