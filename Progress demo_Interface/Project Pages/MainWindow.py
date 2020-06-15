import dash
import dash_bootstrap_components as dbc 
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.graph_objects as plot 

from Methods import Add_CheckBoxMW
from MW_Topbuttons import SU_button , AV_button, DrugA_button, AlleleInfo_button


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

storeOptions = []

UpperButtons = dbc.Row(
    [dbc.Col(
                    [
                      SU_button
                    ]
                ),
                dbc.Col(
                    [
                        AV_button                       
                    ]
                ),
                dbc.Col(
                    [
                        DrugA_button
                    ]
                ),
                dbc.Col(
                    [
                        AlleleInfo_button
                    ]
                )
    ],
            align = 'around',
)


def bottomPart():
    BottomPart = html.Div([
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
            )],
                width = 9,
                align = 'start'
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
                    ]),
                dbc.Row([
                        html.Center(html.B('Available plots')),
                        html.Br(),
                        dcc.RadioItems(
                            options=[
                                {'label':'Bar Graph', 'value': '1'},
                                {'label':'Scatter Plot', 'value': '2'},
                                {'label': '...', 'value': '3'}
                            ],
                            id = 'Plot_Options',
                            labelStyle={'display': 'block'}
                        )
                ])
                 ],
                    width = 3,
                    align = 'end')
        ]),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button('Population ratio', color='secondary')
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Button('Help', color='secondary')
                    ]
                )
            ]
        )
    ]) 
    return BottomPart      
   

def MainWindow():  
    layout = html.Div(
        [  dbc.Row(
            [
            UpperButtons
            ]
        ),
        dbc.Row(
            [
            bottomPart()
            ]
        )
        ]
    )
    return layout

