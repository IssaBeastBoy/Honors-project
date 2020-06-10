import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

colors = {
    'bgColorHome' : '#F0F8FF',
    'textColorHome' : '#000000'
    }


app.layout = html.Div(style = {'backgroundColor': colors['bgColorHome']}, 
    children= [
        html.H1(
            children = ' P450 Pharmacogene Finder',
            style = {
                'textAlign': 'center',
                'color': colors['textColorHome']        
            }
        ),
        html.P(
            'Quick information about aplication...Include background image'
        ),
        html.Button(
                children = 'Begin', 
                    id='HomeButton', 
                    n_clicks=0,
                    style = {
                        'font-size': '20px',
                        'align-items': 'center'
                    }
        ),
        html.Div(id='output'),
        html.P(
            'Link to documentation'
        )
    ]
    
    )

@app.callback(
    Output(component_id='output',component_property='children'),
    [Input('HomeButton', 'n_clicks')])

def update_output(n_clicks):
    if n_clicks >=1:
        

if __name__ == '__main__':
    app.run_server(debug=True)
