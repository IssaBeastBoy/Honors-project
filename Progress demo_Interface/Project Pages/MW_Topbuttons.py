import dash
import dash_bootstrap_components as dbc 
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.graph_objects as plot 


#app.css.append_css({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css'})
#app.scripts.append_script({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js'})
#app.scripts.append_script({'external_url':'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js'})

Variant_information = dbc.Collapse(
            dbc.Card(
                dbc.CardBody(
                    dcc.Loading(
                type="default",
                children=html.Div(id="Tables")
        )
                 )
            ),
            id = 'info_field'
        )

SU_button = dbc.Button('Shared variants', 
                        color='secondary', 
                        className="mt-3",
                        id = 'SV_button')

AV_button = dbc.Button('Unique variants', 
                        color='secondary', 
                        className="mt-3",
                        id = 'UV_button')

DrugA_button = dbc.Button('Drugs Affected', 
                        color='secondary', 
                        className="mt-3",
                        id = 'DrugA_button')

