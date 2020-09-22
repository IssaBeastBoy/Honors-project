import dash
import dash_bootstrap_components as dbc 
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output
from PIL import Image

from UploadPage import Upload

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
#app.css.append_css({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css'})
#app.scripts.append_script({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js'})
#app.scripts.append_script({'external_url':'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js'})
app.config.suppress_callback_exceptions = True

body = dbc.Container(
    [
        html.H1('P450 Pharmacogene allele finder', id='check'),
       html.P(
            "VFC files have provided the biological sciences field with a new and convenient way of"
            + " storing large genetic variant data for proteins and general genetic structures." ),
        html.P("This web application uses uploaded P450 VCF file to find variants that affect that particular CYP enzyme"
            + " ability to function normally, therefore affecting the pharmaceutical drugs that are metabolized by "
            + " that particular CYP enzyme."),
        html.P("Shared and unique variant can be produced when the same CYP enzyme is uploaded of different population groups"
            + " along with the pharmaceutical drug that are metabolized by that particular drug."),
        html.P( "All the VCF data used to design and testing this web application were taken from: "
            ),
        html.Li(dcc.Link('Ensemble',href = 'https://www.ensembl.org/index.html', target ='_blink')),
        html.Br(),
        html.P('All the Pharmaco variants in the data base where taken from:'),
        html.Li(dcc.Link('PharmVar',href = 'https://www.pharmvar.org/genes', target ='_blink')),
        html.Br(),
        html.P('The affect drugs information including metabolites that are produced was taken from:'),
        html.Li(dcc.Link('PharmGKB',href = 'https://www.pharmgkb.org', target ='_blink')),
        html.Br(),
        html.Li(dcc.Link('Drug Bank',href = 'https://www.drugbank.ca', target ='_blink')),
        html.Br(),
        dbc.Row([html.H6('Designed by Thulani Tshabalala')], justify = 'end')
    ]
)

Button = dbc.Nav(
    [
        dbc.NavItem(
            dbc.NavLink("Begin", active= True, href='MainWindow')
            )
    ],
    pills= True,
)

def Homepage():
    layout = html.Div(
        [
            body,
            Button
        ]
    )
    return layout

