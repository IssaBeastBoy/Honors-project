import dash
import dash_bootstrap_components as dbc 
import dash_core_components as dcc 
import dash_html_components as html 

from Methods import Add_CheckBoxMW, AD_dropdown

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
app.config.suppress_callback_exceptions = True

storeOptions = []
activiate_DropDown = ["", "", ""]

def MainWindow(): 
    layout = html.Div(
            [  
            dbc.Row([
                dbc.Col(
                    html.Div(dbc.Button(
                            'Shared Variants', 
                            color = 'success',
                            id = 'SV_button')
                        )),
                dbc.Col(
                    html.Div(dbc.Button(
                            'Unique Variants', 
                            color = 'success',
                            id = 'UV_button')
                        )),
                dbc.Col(
                    html.Div(dbc.Button(
                            'Drugs Affected', 
                            color ='success',
                            id = 'DrugA_button')
                )) 
            ], 
                justify = 'between'),
            dbc.Row([dbc.Collapse(
                        dbc.Card(
                            dbc.CardBody(
                                [html.Div(dbc.Button('Close', color ='danger', id = 'Close_DropDown')),
                                 html.Div([dcc.Loading(
                                     type = 'circle',
                                     children =html.Div(id="Display")
                                 )])
                                ]
                        )
                ),
                        id="Display_table",)]),
            html.Br(),
            html.Div(id = 'activiate', style ={'display':'none'}),
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
                )], width=9, align = '"end"'
                )
              , 
                dbc.Col([
                    dbc.Row([
                             html.Div(id = 'Delete_buttonSpace')
                        ])                
              ,
                    dbc.Row([
                        dbc.Col(
                            dbc.Nav(
                        [
                        dbc.NavItem(
                        dbc.NavLink("Upload VCF", active= True, href='UpLoad')
                        )
                        ],
                        pills= True )
                        ), 
                        dbc.Col([
                        dbc.Button('Delete Selected', color='danger', id ='Delete_button')])
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
                                    {'label':'Sunburst Plot', 'value': '3'},
                                    {'label': 'Orthographic Map', 'value': '4'},
                                    {'label': 'Natural Earth Map', 'value': '5'},
                                    {'label': 'Continential Map', 'value': '6'},
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

