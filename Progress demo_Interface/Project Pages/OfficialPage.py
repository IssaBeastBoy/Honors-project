import mysql.connector
import base64
import dash
import dash_bootstrap_components as dbc 
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output, State
from plotly import graph_objs as plot

from HomePage import Homepage
from UploadPage import Upload, PharmacoInformation, button
from Methods import VCF_FileParse, Coordinates, Plot_points, Add_CheckBoxMW, selected_Files, setting_CheckBOXMW, upLoaded_Details, Pharmaco_VariantParse, get_EnzymeVariants, Plotly_graph, setting_VariantInfo, store_Selected, Sort_info
from MainWindow import MainWindow, storeOptions

Database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'PharmacoEnzymeVariantInfo@Thulani971108',
    database = 'enzyme_variantinfo',
    )

            # [ Variant heading, [Pharmaco variants contained in VCF file] ]
File_details = []

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.GRID, dbc.themes.BOOTSTRAP])
#app.css.append_css({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css'})
#app.scripts.append_script({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js'})
#app.scripts.append_script({'external_url':'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js'})
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

# Call for changing pages
@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')]
            )


def display_page(pathname): 
    if pathname == '/':
        return Homepage()
    elif pathname == '/UpLoad':
        File_details.clear()
        PharmacoInformation[0] == ''
        PharmacoInformation[1] == ''
        PharmacoInformation[2] == ''
        return Upload()
    elif pathname == '/MainWindow':
        file_UploadedInfo = []
        storeList = []
        start = 0      
        while start < len(PharmacoInformation):
            storeList.append(PharmacoInformation[start])
            start = start + 1
        
        file_UploadedInfo.append(storeList[2]) 
        file_UploadedInfo.append(storeList[0]) 
        file_UploadedInfo.append(Coordinates[storeList[1]])
        variant_Info = Pharmaco_VariantParse(get_EnzymeVariants(Database, storeList[0]), File_details[0])
        file_UploadedInfo.append(variant_Info[1])
        file_UploadedInfo.append(variant_Info[2])
        file_UploadedInfo.append(variant_Info[0])
        file_UploadedInfo.append(variant_Info[3])
        upLoaded_Details.append(file_UploadedInfo)        
        return MainWindow()

#Call back for checking uploaded file   
@app.callback(
    Output('place_Filename', 'children'),
    [Input('VCF', 'contents')],
    [State('VCF', 'filename')]
)

def VCF_processing(contents, filename):  
    if filename is None:
        layout = html.Div(
        [
            html.H6(
                'Drag and Drop .vcf '
            )
        ]
        )
    else:       
        format_Content = contents.split(',')
        file_information = format_Content[1]
        base64_bytes = file_information.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        file_Content = message_bytes.decode('ascii')
        File_details.append(VCF_FileParse(file_Content, filename))
        storeOptions.append(filename)
        PharmacoInformation[2] = filename
        layout = html.Div(
        [
            html.H6(
                filename
            )
        ]
        )
    return layout

#Call back for enzyme family dropdown
@app.callback(
    Output('output_Enzy', 'children'),
    [Input('CYP1', 'value'),
    Input('CYP2', 'value'),
    Input('CYP3', 'value')]
)

def EnzyFamily(value1, value2, value3):
    if value1 is None and value2 is None and value3 is None:
        layout = html.Div(
            html.Center('*Fill in up the field above', style={"color":"rgb(255,0,0)"})
        )        
    else:
        layout = html.Div('')
    if value1 != None:
        enzy = ['CYP1A1', 'CYP1A2']
        PharmacoInformation[0]= enzy[int(value1)-1]
    if value2 != None: 
        enzy = ['CYP2A6', 'CYP2C8', 'CYP2C9','CYP2C19', 'CYP2D6', 'CYP2E1', 'CYP2F1']
        PharmacoInformation[0]= enzy[int(value2)-1]
    if value3 != None: 
        enzy = ['CYP3A4', 'CYP3A5', 'CYP3A43']
        PharmacoInformation[0]= enzy[int(value3)-1]
    return layout

#Call back for population dropdown
@app.callback(
    Output('output_pop', 'children'),
    [Input('AF', 'value'),
    Input('EA', 'value'),
    Input('SA', 'value'),
    Input('AM', 'value'),
    Input('AN', 'value'),
    Input('EU', 'value'),
    Input('NA', 'value')
    ]
)

def populationGroup(value1, value2, value3, value4, value5, value6, value7):
    if value1 is None and value2 is None and value3 is None and value4 is None and value5 is None and value6 is None and value7 is None:
        layout = html.Div(
            html.Center('*Fill in up the field above', style={"color":"rgb(255,0,0)"})
        )
    else:
        layout = html.Div('')
    if value1 != None: 
        popu = ['Esan', 'The Gambia', 'Luhya','Menda', 'Ibadan']
        PharmacoInformation[1]= popu[int(value1)-1]
    if value2 != None: 
        popu = ['Dai', 'Beijing', 'Tokyo', 'Kibh', 'Han']
        PharmacoInformation[1]= popu[int(value2)-1]
    if value3 != None: 
        popu = ['Bengali', 'Punjabi']
        PharmacoInformation[1]= popu[int(value3)-1]
    if value4 != None: 
        popu = ['Colombian', 'Peruvian', 'Puerto_Rican']
        PharmacoInformation[1]= popu[int(value4)-1]
    if value5 != None: 
        popu = ['Telugu', 'Tami', 'African', 'Caribbean', 'Gujarati', 'Mexican']
        PharmacoInformation[1]= popu[int(value5)-1]
    if value6 != None: 
        popu = ['British/Scotish', 'Finnish', 'Lberian', 'Toscani']
        PharmacoInformation[1]= popu[int(value6)-1]
    if value7 != None: 
        PharmacoInformation[1]= 'None Specfic'
    return layout
     
#Call back for the uploading details
@app.callback(
    Output('Upload_button', 'children'), 
    [Input('AF', 'value'),
    Input('EA', 'value'),
    Input('SA', 'value'),
    Input('AM', 'value'),
    Input('AN', 'value'),
    Input('EU', 'value'),
    Input('NA', 'value'),
    Input('CYP1', 'value'),
    Input('CYP2', 'value'),
    Input('CYP3', 'value'),
    Input('VCF', 'contents')
    ]
)

def upload_design(value1, value2, value3, value4, value5, value6, value7, value8, value9 , value10, content):
    if (value1 != None or value2 != None or value3 != None or value4 != None or value5 != None or value6 != None or value7 != None) and (value8 != None or value9 != None or value10 != None) and (content != None):
        layout = html.Div(
            [html.Br(),
            html.Center(),
            button]
        )
        return layout        
    
                   
#Call back for shared variant button
@app.callback(
    Output('info_field', 'is_open'),
    [Input('SV_button', 'n_clicks'),
     Input('UV_button', 'n_clicks'),
     Input('DrugA_button', 'n_clicks')],
    [State("info_field", "is_open")],
)

def Variant_data(svB, uvB, daB, is_open):
    if (svB != None  or uvB != None or daB != None ):
        if (svB != None and (svB==1 or svB%2 > 0)):
            return not is_open
        elif (uvB != None and (uvB == 1 or uvB%2 > 0)):
            return not is_open
        elif (daB != None and (daB == 1 or daB%2 > 0)):
            return not is_open    
        else:
            return not is_open    
    else:
        return not is_open

#Call back for shared variant button
@app.callback(
    Output('Tables', 'children'),
    [Input('SV_button', 'n_clicks'),
     Input('UV_button', 'n_clicks'),
     Input('DrugA_button', 'n_clicks'),
     Input('CheckBox_File','value')]
)

def set_Table(svB, uvB, daB, file_select):
    if (svB != None  or uvB != None or daB != None ) and file_select != None:
        start = 0
        if (svB != None and (svB==1 or svB%2 > 0)):
            ordered_Files = Sort_info(Plot_points(upLoaded_Details, selected_Files), 'Bar_Graph')  
            layout = html.Div(
                style = {'white-space': 'pre-wrap'} ,
                children = setting_VariantInfo(True, False, ordered_Files, Database)
                )
            return layout
        if (uvB != None and (uvB == 1 or uvB%2 > 0)):
            ordered_Files = Sort_info(Plot_points(upLoaded_Details, selected_Files), 'Bar_Graph')  
            layout = html.Div(
                style = {'white-space': 'pre-wrap'} ,
                children = setting_VariantInfo(False, False, ordered_Files, Database)
                )
            return layout        
    else:
        layout = html.Div(
            html.H6("No file select")
        )
        return layout
   
        
    
#Call back for main window check box files
@app.callback(
    Output('CheckBox', 'children'),
    [Input('CheckBox_File','value')]
)

def ticked_Files(value):
    if value is None: 
        selected_Files.clear()
    else:
        selected_Files.clear()
        start = 0
        while start < len(value):        
            selected_Files.append(value[start])
            start = start + 1 

#Call back for drawing plot
@app.callback(
    Output('Plot', 'children'),
    [Input('Plot_Options', 'value'),
    Input('CheckBox_File','value')]
)

def Figure(radio, check):
    avialable_Plot = ['Bar_Graph', 'Scatter', 'Orthographic', 'natural_earth', 'Continential']    
    if radio is None and check is None:
        layout = html.Div(
                html.H4(
                    html.Center('Select file \n and \n plot type')
                )
            )
    elif radio is None:
        layout = html.Div(
                html.H4(html.Center('Select plot type from available plots'))
            )
    elif check is None:
        layout = html.Div(
                html.H4(html.Center('Select file from loaded files'))
            )
    else:
        if len(check) == 0:
            layout = html.Div(
                html.H4(html.Center('Select file from loaded files'))
            )
        else:
            figure = Plotly_graph(Plot_points(upLoaded_Details, selected_Files), avialable_Plot[int(radio)-1])
            layout = html.Div(
                    dcc.Graph(figure = figure)
                )
    return layout

#Call back for main window delete file button
@app.callback(
    Output('Delete_buttonSpace','children'),
    [Input('Delete_button','n_clicks')]
)

def deleteFile_action(n_clicks):     
    if n_clicks is None:
        option = Add_CheckBoxMW(storeOptions)
        layout = setting_CheckBOXMW(option)
    else:
        start = 0
        while start < len(selected_Files):
            index = int(selected_Files[start])
            item = storeOptions[index-1]
            storeOptions.remove(item)
            index = 0
            while index < len(upLoaded_Details):
                if upLoaded_Details[index][0] == item:                    
                    del upLoaded_Details[index]
                    break
                index = index + 1
            start = start + 1
        option = Add_CheckBoxMW(storeOptions)
        layout = setting_CheckBOXMW(option)
    return layout

if __name__ == '__main__':
    app.run_server(debug=False)