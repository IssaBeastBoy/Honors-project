import dash
import dash_bootstrap_components as dbc 
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output

from UploadPage import Upload

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#app.css.append_css({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css'})
#app.scripts.append_script({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js'})
#app.scripts.append_script({'external_url':'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js'})
app.config.suppress_callback_exceptions = True

body = dbc.Container(
    [
        html.H1('P450 Pharmacogene allele finder', id='check'),
        html.P(
            'VFC files have provided the biological sciences field are new and rapid way of find variants within and between population groups. Providing a way to apply pharmacogenetics analysis on a global scale'
        ),
    ]
)

Button = dbc.Nav(
    [
        dbc.NavItem(
            dbc.NavLink("Begin", active= True, href='UpLoad')
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

