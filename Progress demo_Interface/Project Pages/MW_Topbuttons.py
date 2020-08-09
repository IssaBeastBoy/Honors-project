import dash
import dash_bootstrap_components as dbc 
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.graph_objects as plot 


#app.css.append_css({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css'})
#app.scripts.append_script({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js'})
#app.scripts.append_script({'external_url':'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js'})



SU_button = dbc.DropdownMenu(
                        label = 'Shared Variants', 
                        color = activiate_DropDown[0],
                        children=[ 
                        dcc.Loading(
                                type = 'circle',
                                children = dbc.DropdownMenuItem(id = 'Display_SV')
                            )],
                        id = 'SV_button'
                        )

AV_button = dbc.DropdownMenu(
                        label = 'Unique Variants', 
                        color = activiate_DropDown[1],
                        children=[ 
                            dcc.Loading(
                                type = 'circle',
                                children = dbc.DropdownMenuItem(id = 'Display_UV')
                            )],
                        id = 'UV_button'                       
                        )

DrugA_button = dbc.DropdownMenu(
                        label = 'Drugs Affected', 
                        color = activiate_DropDown[2],
                        children=[ 
                            dcc.Loading(
                                type = 'circle',
                                children = dbc.DropdownMenuItem(id = 'Display_DrugA')
                            )],
                        id = 'DrugA_button'  
                        ) 

