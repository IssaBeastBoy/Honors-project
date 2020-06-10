import dash
import dash_bootstrap_components as dbc 
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.graph_objects as plot 

#app.css.append_css({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css'})
#app.scripts.append_script({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js'})
#app.scripts.append_script({'external_url':'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js'})

share_Variants = html.Div(
    [
        html.H3('Will information about the shared variants'),
        dbc.Button('Close', color='danger', id ='Back_ToSVB')
    ],
        id = 'Share_Vinfo'
)

unique_Variants = html.Div(
    [
        html.H3('Write all the unique variants'),
        dbc.Button('Close', color='danger', id ='Back_ToUVB')
    ],
        id = 'Unique'
)

drug_Affected = html.Div(
    [
        html.H3('Write all the drugs that are affected'),
        dbc.Button('Close', color='danger', id ='Back_ToDrugAB')
    ],
        id = 'Drug_A'
)

SU_button =  html.Div(
    [
                    dbc.Button('Shared variants', color='secondary', id = 'SV_button')
    ],
                        id = 'Info_PlayGround1'
)

AV_button = html.Div(
    [
                     dbc.Button('Unique variants', color='secondary', id = 'UV_button')
    ],                      
                        id = 'Info_PlayGround2'
)

DrugA_button = html.Div(    
    [
                        dbc.Button('Drugs Affected', color='secondary', id = 'DrugA_button')
    ],
                        id = 'Info_PlayGround3'
)

AlleleInfo_button = html.Div(    
    [
                        dbc.Button('Alleles information', color='secondary', id = 'AI_button')
    ],
                        id = 'Info_PlayGround4'
)

AI = html.Div(
    [
        html.H3('Write all the allele information that were found'),
        dbc.Button('Close', color='danger', id ='Back_ToAIB')
    ],
        id = 'AI'
)