import dash
import io
import dash_bootstrap_components as dbc 
import dash_html_components as html 
import dash_core_components as dcc 
from dash.dependencies import Output,Input

from Methods import upLoad_requirements

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#app.css.append_css({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css'})
#app.scripts.append_script({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js'})
#app.scripts.append_script({'external_url':'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js'})
app.config.suppress_callback_exceptions = True

                    # EnzymeName, Population, FileName
PharmacoInformation = ['','','']

upLoad = dbc.Container(
        [
            dbc.Col(
                html.H2(
                    'Upload VCF file'
                    )
            ),
            dbc.Col(
                dcc.Loading(  
                    children = dcc.Upload(
                        html.Div(
                            id = 'place_Filename'
                            ),
                    className = 'Upload_File',
                    multiple = False,
                    id = 'VCF'
                )            ,
                type = 'default'
            ), width = 'auto'),
        ]
        )

CYP1_dropdown = html.Div(
                 dcc.RadioItems( 
                            id = 'CYP1',
                            options=[
                                {'label':'CYP1A1', 'value': '1'},
                                {'label':'CYP1A2', 'value': '2'}
                            ],
                            )
            )

CYP2_dropdown = html.Div(
                 dcc.RadioItems( 
                            id = 'CYP2',
                            options=[
                                {'label':'CYP2A6', 'value': '1'},
                                {'label':'CYP2C8', 'value': '2'},
                                {'label':'CYP2C9', 'value': '3'},
                                {'label':'CYP2C19', 'value': '4'},
                                {'label':'CYP2D6', 'value': '5'},
                                {'label':'CYP2E1', 'value': '6'},
                                {'label':'CYP2F1', 'value': '7'},
                            ],
                            labelStyle={'display': 'block'}
                        )
    )

CYP3_dropdown = html.Div(
                 dcc.RadioItems( 
                            id = 'CYP3',
                            options=[
                                {'label':'CYP3A4', 'value': '1'},
                                {'label':'CYP3A5', 'value': '2'},
                                {'label':'CYP3A43', 'value': '3'},                                
                            ],
                            labelStyle={'display': 'block'}
                            )
            )

enzymeSelection =[
        dbc.DropdownMenu(
            label = 'CYP1 Family',
            children = CYP1_dropdown
        ),
        dbc.DropdownMenu(
            label = 'CYP2 Family',
            children = CYP2_dropdown
            ),
        dbc.DropdownMenu(
            label = 'CYP3 Family',
            children = CYP3_dropdown
        )
    ]

enzymeFamily = html.Div([
    dbc.DropdownMenu(
        label='Select P450 Pharmaco enzyme',
        bs_size="lg",
        children= enzymeSelection
    )
    ], id='enzyme')

button = dbc.Nav(
    [
        dbc.NavItem(
            dbc.NavLink("Submit", active= True, href='MainWindow')
            )
    ],
    pills= True,
    )

East_Asian = html.Div(
                 dcc.RadioItems( 
                            id = 'EA',
                            options=[
                                {'label':'Chinses Dai, China - Code: CDX ', 'value': '1'},
                                {'label':'Han Chinese, China - Code: CHB', 'value': '2'},
                                {'label':'Japanese, Japan - Code: JPT ', 'value': '3'},
                                {'label':'Kibh, Vietnam- Code: KHV', 'value': '4'},
                                {'label':'Southern Han Chinese, China - Code: CHS ', 'value': '5'}
                            ]
                        )
    )

South_Asian = html.Div(
                 dcc.RadioItems( 
                            id = 'SA',
                            options=[
                                {'label':'Bengali, India - Code: BEB', 'value': '1'},
                                {'label':'Punjabi, Pakistan - Code: PJL', 'value': '2'}
                            ]
                        )
    )

African = html.Div(
                 dcc.RadioItems( 
                            id = 'AF',
                            options=[
                                {'label':'Esan, Nigeria - Code: ESN', 'value': '1'},
                                {'label':'Gambain, The Gambia - Code: GWD', 'value': '2'},
                                {'label':'Luhya, Kenya - Code: LWK', 'value': '3'},
                                {'label':'Mende, Sierra Leone - Code: MSL', 'value': '4'},
                                {'label':'Yoruba, Nigeria - Code: YRI', 'value': '5'}
                            ]
                        )
    )

European =  html.Div(
                 dcc.RadioItems( 
                            id = 'EU',
                            options=[
                                {'label':'British/Scotish, UK - Code: GBR', 'value': '1'},
                                {'label':'Finnish, Finland - Code: FIN', 'value': '2'},
                                {'label':'Lberian, Spain - Code: IBS', 'value': '3'},
                                {'label':'Toscani, Italy - Code: TSI', 'value': '4'}
                            ]
                        )
    )

American =  html.Div(
                 dcc.RadioItems( 
                            id = 'AM',
                            options=[
                                {'label':'Colombian, Colmbia - Code: CLM ', 'value': '1'},
                                {'label':'Peruvian, Peru - Code: PEL', 'value': '2'},
                                {'label':'Puerto Rican, Puerto Rico - Code: PUR', 'value': '3'}
                            ]
                        )
    )

Ancestry = html.Div(
                 dcc.RadioItems( 
                            id = 'AN',
                            options=[
                                {'label':'Telugu(Indian), UK - Code: ITU', 'value': '1'},
                                {'label':'Tami (Sri Lankan), UK - Code: STU', 'value': '2'},
                                {'label':'African, USA - Code: ASW', 'value': '3'},
                                {'label':'Caribbean, Barbados - Code: ACB', 'value': '4'},
                                {'label':'Gujarati, USA - Code: GIH', 'value': '5'},
                                {'label':'Mexican, USA - Code: MXL', 'value': '6'}
                            ]
                        )
    )

population = [
    dbc.DropdownMenu(
        label='African population',
        children= African
    ),
    dbc.DropdownMenu(
        label='Ancestry population',
        children= Ancestry
    ),
    dbc.DropdownMenu(
        label='American population',
        children= American
    ),
    dbc.DropdownMenu(
        label='East Asia population',
        children= East_Asian
    ),
    dbc.DropdownMenu(
        label='European population',
        children= European
    ),
    dbc.DropdownMenu(
        label='South Asia population',
        children= South_Asian
    ),
    html.Div(
                 dcc.RadioItems( 
                            id = 'NA',
                            options=[
                                {'label':'Enter custom population', 'value': '1'}
                            ],
                            )
            )
    ]

populationGroups =  html.Div([
    dbc.DropdownMenu(
        label='Select population group',
        bs_size="lg",
        children= population
    )
    ], id = 'population')

Continent_Form = dbc.FormGroup(
        [
            dbc.Label('Selected continent which the .vcf file is fom'),
            dcc.Dropdown(
                options=[
                    {'label': 'Africa', 'value': 0},
                    {'label': 'Asia', 'value': 1},
                    {'label': 'Europe', 'value': 2},
                    {'label': 'North America', 'value': 3},
                    {'label': 'South America', 'value': 4}
                    ],
                id = 'continent',
                placeholder="Select a continent...")
        ]
    )

Location_form = dbc.FormGroup(
        [
            dbc.Label('Enter the location (Country, Province or State, Town)'),
            dbc.Input(type='text', id='location')
        ]
    )

Coors_Form = dbc.FormGroup(
        [
            dcc.ConfirmDialog(
                id='confirm',
                message='Danger! Moving to MainWindow without adding all the required upLoading details',
            ),
            dbc.Row([
                dbc.Col(
                [
                    dbc.Label('Enter the longitude coordinates.'),
                    dbc.Input(type='text', placeholder = 'Longitude...', id = 'log')
                ],
                    width=6
                ),
                dbc.Col(
                [
                    dbc.Label('Enter the Latitude coordinates.'),
                    dbc.Input(type='text', placeholder = 'Latitude...', id = 'lat')
                ],
                    width=6
                )
            ]),
            dbc.Row(
                    children =[dbc.Button("Get coordinates", color="link", href='https://www.latlong.net/', target = '_blink')],
                    justify = "end"
            ),
            dbc.Row(
                [
                    html.Div(['All the above fields are required and incorrect inputs will results in processing errors'], style={'color':'red'})
                   
                ]
            ),
            dbc.Row(
                    [dbc.Collapse(
                        dbc.Card(dbc.CardBody(dbc.Button('Submit', id = 'close', color = 'success'))),
                            id="submit",
                        )]
            )
        ]
    )

Popup = html.Div([
                dbc.Alert(
                    [
                        html.Center(html.H5('You have added a custom .vcf')),
                        dbc.Form(
                            [Continent_Form, Location_form, Coors_Form]
                        )
                    ],
                    color = 'success',
                    is_open = False,
                    id = 'Popup'
                )
    ])

##app.layout = html.Div([
##    dcc.Location(id = 'url', refresh = False),
##    html.Div(id = 'page-content')
##])
##
##@app.callback(Output('page-content', 'children'),
##            [Input('url', 'pathname')]
##            )

def Upload():
    layout = html.Div(
        [
            html.Div(
                className = 'popup_File',
                id = 'Wrong_file',
                children = [
                        html.Div( 
                            className = 'header', 
                            children = [
                                html.Div("Invalid file type", className = 'title'),
                                html.Button('&times', className = 'Close_wrongFile', id = 'File')]),
                        html.Div('The file you have uploaded does not have the vcf file extension.', className = 'Warning_wrongfile')
                    ]
            ),
            dbc.Row([
                upLoad
            ]),
            dbc.Row(
                [
                    Popup
                ],
                justify="center",
            ),
            dbc.Row([
                dbc.Col(
                    [
                    enzymeFamily,
                    html.Div(id='output_Enzy'),
                    ]),
                dbc.Col([
                    populationGroups,
                    html.Div(id='output_pop')
                   
                ])
            ]),
            dbc.Row(                
                [html.Div(id='Upload_button')]
            )
        ]
    )
    return layout

##if __name__ == "__main__":
##    app.run_server(debug=False)
