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
from Methods import VCF_FileParse, plot_Layouts, Usable_files, Coordinates, Coordinates, Plot_points, drugs_Affected, Add_CheckBoxMW, setting_CheckBOXMW, upLoaded_Details, Pharmaco_VariantParse, get_EnzymeVariants, Plotly_graph, setting_VariantInfo, store_Selected, Sort_info, AD_dropdown
from MainWindow import MainWindow, storeOptions, activiate_DropDown


Database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'PharmacoEnzymeVariantInfo@Thulani971108',
    database = 'enzyme_variantinfo',
        )

File_details = []

keep_Open = [True]

selected_Files = []

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.GRID, dbc.themes.FLATLY])
#app.css.append_css({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css'})
#app.scripts.append_script({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js'})
#app.scripts.append_script({'external_url':'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js'})
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

# Call back for changing pages
@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')]
            )

def display_page(pathname): 
    if pathname == '/':
        return Homepage()
    elif pathname == '/UpLoad':
        File_details.clear()
        PharmacoInformation[0] = ''
        PharmacoInformation[1] = ''
        PharmacoInformation[2] = ''
        return Upload()
    elif pathname == '/MainWindow':
        if PharmacoInformation[0] == '' or PharmacoInformation[1] == '' or PharmacoInformation[2] == '':
            return MainWindow()
        else:
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
    Input('close', 'n_clicks')]
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
    Input('close', 'n_clicks'),
    Input('CYP1', 'value'),
    Input('CYP2', 'value'),
    Input('CYP3', 'value'),
    Input('VCF', 'contents')
    ]
    )

def upload_design(value1, value2, value3, value4, value5, value7, value6, value8, value9 , value10, content):
    if (value1 != None or value2 != None or value3 != None or value4 != None or value6 != None or value5 != None or value7 != None) and (value8 != None or value9 != None or value10 != None) and (content != None):
        layout = html.Div(
            [html.Br(),
            html.Center(),
            button]
        )
        return layout        

#Call back for uploading custom population details 
@app.callback(
    Output('submit', 'is_open'),
    [
        Input('lat', 'value'),
        Input('log','value'),
        Input('continent', 'value'),
        Input('location', 'value')
    ],
        [State('submit', 'is_open')]        
    )

def custom_Upload(lat, log, contin, loca, is_open):
    if lat != None and log != None and contin != None and loca != None:        
        if keep_Open[0] == True:
            Continents = ['africa', 'asia', 'europe', 'north america', 'south america']
            PharmacoInformation[1] = loca
            Coordinates[loca] = {'Lat':lat, 'Long':log, 'Continent':Continents[contin], 'location':loca}
            keep_Open[0] = False
            return not is_open
        if is_open == True:
            return is_open
        if is_open == False or is_open == None:
            return not is_open

#Call back for the custom population details
@app.callback(
        Output('Popup', 'is_open'),
        [
            Input('NA', 'value'),
            Input('close', 'n_clicks')
        ],
        [State('Popup', 'is_open')]
    ) 

def Custom_popUp(value, close, is_open):
    if close != None:
        if close%2 > 0:
            return not is_open
    if value != None:
        return not is_open

#Call back for displaying drug anticoagulation table
@app.callback(
    Output('anticoagulation', 'children'),
    [
     Input('Antico', 'n_clicks'),
     Input('CheckBox_File','value')
     ]
 )

def anticoagulation(clicks, value):
    if clicks != None and clicks%2 > 0:
        ordered_Files = Sort_info(Plot_points(upLoaded_Details, value), 'Bar_Graph')
        enzymes_Name = Usable_files(False, ordered_Files)    
        return drugs_Affected(enzymes_Name, 'Anticoagulation', Database)

#Call back for closing anticoagulation collapse
@app.callback(
    Output('anticoagulation_B', 'is_open'),
    [Input('Antico', 'n_clicks')],
    [State('anticoagulation_B', 'is_open')]
 )

def anticoagulation_Collapse(clicks, is_open):
    if clicks == None and is_open == None:
        return is_open
    if clicks != None and clicks%2 >0:
        return not is_open
    else:
        if clicks%2 == 0 or is_open == True:
            return not is_open

#Call back for displaying drug antidepressants table
@app.callback(
    Output('antidepressants', 'children'),
    [
     Input('Antide', 'n_clicks'),
     Input('CheckBox_File','value')]
    )

def antidepressants(clicks, value):
    if clicks != None and clicks%2 > 0:
        ordered_Files = Sort_info(Plot_points(upLoaded_Details, value), 'Bar_Graph')
        enzymes_Name = Usable_files(False, ordered_Files)
        return drugs_Affected(enzymes_Name, 'Antidepressants', Database)

#Call back for closing antidepressants table
@app.callback(
    Output('antidepressants_B', 'is_open'),
    [ Input('Antide', 'n_clicks')],
    [State('antidepressants_B','is_open')]
    )

def antidepressants_Collapse(clicks, is_open):
    if clicks == None and is_open == None:
        return is_open
    if clicks != None and clicks%2 >0:
        return not is_open
    else:
        if clicks%2 == 0 or is_open == True:
            return not is_open

#Call back for displaying drug antifungals table
@app.callback(
    Output('Antifu', 'children'),
    [
     Input('antifungals', 'n_clicks'),
     Input('CheckBox_File','value')]
    )

def antifungals(clicks, value):
    if clicks != None and clicks%2 > 0:
        ordered_Files = Sort_info(Plot_points(upLoaded_Details, value), 'Bar_Graph')
        enzymes_Name = Usable_files(False, ordered_Files)   
        return drugs_Affected(enzymes_Name, 'Antifungals', Database)

#Call back for closing antifungals collapse
@app.callback(
    Output('Antifu_B', 'is_open'),
    [Input('antifungals', 'n_clicks')],
    [State('Antifu_B', 'is_open')]
    )

def antifungals_Collapse(clicks, is_open):
    if clicks == None and is_open == None:
        return is_open
    if clicks != None and clicks%2 >0:
        return not is_open
    else:
        if clicks%2 == 0 or is_open == True:
            return not is_open

#Call back for displaying drug antipsychotics table
@app.callback(
    Output('antipsychotics', 'children'),
    [
     Input('Antips', 'n_clicks'),
     Input('CheckBox_File','value')]
    )

def antipsychotics(clicks, value):
    if clicks != None and clicks%2 > 0:
        ordered_Files = Sort_info(Plot_points(upLoaded_Details, value), 'Bar_Graph')
        enzymes_Name = Usable_files(False, ordered_Files)  
        return drugs_Affected(enzymes_Name, 'Antipsychotics', Database)

#Call back for closing antipsychotics collapse
@app.callback(
    Output("Antips_B", 'is_open'),
    [Input('Antips', 'n_clicks')],
    [State("Antips_B", 'is_open')]
    )

def antipsychotics_Collapse(clicks, is_open):
    if clicks == None and is_open == None:
        return is_open
    if clicks != None and clicks%2 >0:
        return not is_open
    else:
        if clicks%2 == 0 or is_open == True:
            return not is_open

#Call back for displaying drug antitumor table
@app.callback(
    Output('antitumor', 'children'),
    [
     Input('Antitu', 'n_clicks'),
     Input('CheckBox_File','value')]
    )

def Antitumor(clicks, value):
    if clicks != None and clicks%2 > 0:
        ordered_Files = Sort_info(Plot_points(upLoaded_Details, value), 'Bar_Graph')
        enzymes_Name = Usable_files(False, ordered_Files) 
        return drugs_Affected(enzymes_Name, 'Antitumor', Database)

#Call back for closing antitumor collapse
@app.callback(
    Output('Antitu_B', 'is_open'),
    [Input('Antitu', 'n_clicks')],
    [State('Antitu_B', 'is_open')]
    )

def Antitumor_Collapse(clicks, is_open):
    if clicks == None and is_open == None:
        return is_open
    if clicks != None and clicks%2 >0:
        return not is_open
    else:
        if clicks%2 == 0 or is_open == True:
            return not is_open

#Call back for displaying drug antiretroviral table
@app.callback(
    Output('antiretroviral', 'children'),
    [
     Input('Antire', 'n_clicks'),
     Input('CheckBox_File','value')]
    )

def antiretroviral(clicks, value):
    if clicks != None and clicks%2 > 0:
        ordered_Files = Sort_info(Plot_points(upLoaded_Details, value), 'Bar_Graph')
        enzymes_Name = Usable_files(False, ordered_Files) 
        return drugs_Affected(enzymes_Name, 'Antiretroviral', Database)

#Call back for closing antiretroviral collapse
@app.callback(
    Output('Antire_B', 'is_open'),
    [Input('Antire', 'n_clicks')],
    [State('Antire_B', 'is_open')]
    )

def antiretroviral_Collapse(clicks, is_open):
    if clicks == None and is_open == None:
        return is_open
    if clicks != None and clicks%2 >0:
        return not is_open
    else:
        if clicks%2 == 0 or is_open == True:
            return not is_open

#Call back for displaying drug beta-blockers table
@app.callback(
    Output('beta-blockers', 'children'),
    [
     Input('Bet', 'n_clicks'),
     Input('CheckBox_File','value')]
    )

def beta_blockers(clicks, value):
    if clicks != None and clicks%2 > 0:
        ordered_Files = Sort_info(Plot_points(upLoaded_Details, value), 'Bar_Graph')
        enzymes_Name = Usable_files(False, ordered_Files) 
        return drugs_Affected(enzymes_Name, 'Beta_Blockers', Database)

#Call back for closing beta-blockers collapse
@app.callback(
    Output('Bet_B', 'is_open'),
    [Input('Bet', 'n_clicks')],
    [State('Bet_B', 'is_open')]
    )

def beta_blockers_Collapse(clicks, is_open):
    if clicks == None and is_open == None:
        return is_open
    if clicks != None and clicks%2 >0:
        return not is_open
    else:
        if clicks%2 == 0 or is_open == True:
            return not is_open

#Call back for displaying drug immunosuppressive table
@app.callback(
    Output('immunosuppressive', 'children'),
    [
     Input('Immu', 'n_clicks'),
     Input('CheckBox_File','value')]
    )

def immunosuppressive(clicks, value):
    if clicks != None and clicks%2 > 0:
        ordered_Files = Sort_info(Plot_points(upLoaded_Details, value), 'Bar_Graph')
        enzymes_Name = Usable_files(False, ordered_Files) 
        return drugs_Affected(enzymes_Name, 'Immunosuppressive', Database)

#Call back for closing immunosuppressive collapse
@app.callback(
    Output('Immu_B', 'is_open'),
    [Input('Immu', 'n_clicks')],
    [State('Immu_B', 'is_open')]
    )

def immunosuppressive_Collapse(clicks, is_open):
    if clicks == None and is_open == None:
        return is_open
    if clicks != None and clicks%2 >0:
        return not is_open
    else:
        if clicks%2 == 0 or is_open == True:
            return not is_openn

#Call back for displaying drug Miscellaneous table
@app.callback(
    Output('Miscellaneous', 'children'),
    [
     Input('Mis', 'n_clicks'),
     Input('CheckBox_File','value')]
    )

def Miscellaneous(clicks, value):
    if clicks != None and clicks%2 > 0:
        ordered_Files = Sort_info(Plot_points(upLoaded_Details, value), 'Bar_Graph')
        enzymes_Name = Usable_files(False, ordered_Files) 
        return drugs_Affected(enzymes_Name, 'Miscellaneous', Database)

#Call back for closing Miscellaneous collapse
@app.callback(
    Output('Mis_B', 'is_open'),
    [Input('Mis', 'n_clicks')],
    [State('Mis_B', 'is_open')]
    )

def Miscellaneous_Collapse(clicks, is_open):
    if clicks == None and is_open == None:
        return is_open
    if clicks != None and clicks%2 >0:
        return not is_open
    else:
        if clicks%2 == 0 or is_open == True:
            return not is_open

#Call back for displaying drug NSAIDS table
@app.callback(
    Output('NSAI', 'children'),
    [
     Input('NSAIDS', 'n_clicks'),
     Input('CheckBox_File','value')]
    )

def NSAIDS(clicks, value):
    if clicks != None and clicks%2 > 0:
        ordered_Files = Sort_info(Plot_points(upLoaded_Details, value), 'Bar_Graph')
        enzymes_Name = Usable_files(False, ordered_Files) 
        return drugs_Affected(enzymes_Name, 'NSAIDS', Database)

#Call back for closing NSAIDS collapse
@app.callback(
    Output('NSAI_B', 'is_open'),
    [Input('NSAIDS', 'n_clicks')],
    [State('NSAI_B', 'is_open')]
    )

def NSAIDS_Collapse(clicks, is_open):
    if clicks == None and is_open == None:
        return is_open
    if clicks != None and clicks%2 >0:
        return not is_open
    else:
        if clicks%2 == 0 or is_open == True:
            return not is_open

#Call back for displaying drug Opioids table
@app.callback(
    Output('Opio', 'children'),
    [
     Input('opioids', 'n_clicks'),
     Input('CheckBox_File','value')]
    )

def Opioids(clicks, value):
    if clicks != None and clicks%2 > 0:
        ordered_Files = Sort_info(Plot_points(upLoaded_Details, value), 'Bar_Graph')
        enzymes_Name = Usable_files(False, ordered_Files) 
        return drugs_Affected(enzymes_Name, 'Opioids', Database)

#Call back for closing Opioids collapse
@app.callback(
    Output('Opio_B', 'is_open'),
    [Input('opioids', 'n_clicks')],
    [State('Opio_B', 'is_open')]
    )

def Opioids_Collapse(clicks, is_open):
    if clicks == None and is_open == None:
        return is_open
    if clicks != None and clicks%2 >0:
        return not is_open
    else:
        if clicks%2 == 0 or is_open == True:
            return not is_open

#Call back for displaying table for shared, unique variants
@app.callback(
    Output('Display_table', 'is_open'),
    [Input('SV_button', 'n_clicks'),
     Input('UV_button', 'n_clicks'),
     Input('DrugA_button', 'n_clicks'),
     Input('Close_DropDown','n_clicks')],
    [State("Display_table", "is_open")],
    )

def closing_DropDown(svB, uvB, daB, close, is_open):
    if close != None and close%2 > 0:
        if is_open == None or is_open == False:
            return not is_open
    if close != None and close%2 == 0:
        return not is_open
    if svB != None:
        if is_open == None or is_open == False:
            return not is_open
    if uvB != None:
        if is_open == None or is_open == False:
            return not is_open
    if daB != None:
        if is_open == None or is_open == False:
            return not is_open

#Call back for displaying table for shared & unique variants and 
@app.callback(
    Output('Display', 'children'),
    [Input('SV_button', 'n_clicks'),
     Input('UV_button', 'n_clicks'),
     Input('DrugA_button', 'n_clicks'),
     Input('CheckBox_File','value')]
    )

def setTable(svB, uvB, daB, file_select):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if 'SV_button' == button_id and file_select != []:
        if len(file_select) >1:
            ordered_Files = Sort_info(Plot_points(upLoaded_Details, file_select), 'Bar_Graph')
            use_file = Usable_files(True, ordered_Files)
            if len(use_file) > 0:  
                layout = html.Div(
                    style = {'white-space': 'pre-wrap'},
                    children = setting_VariantInfo(True, False, use_file, Database)
                    ) 
                return layout
            else:
                return html.H6("Selected files with different enzymes")
        else:
            return html.H6("Single file selected")
    if 'UV_button' == button_id and file_select !=[]:
        if len(file_select) >1:            
            ordered_Files = Sort_info(Plot_points(upLoaded_Details, file_select), 'Bar_Graph')
            use_file = Usable_files(True, ordered_Files)
            if len(use_file) > 0:  
                layout = html.Div(
                    style = {'white-space': 'pre-wrap'},
                    children = setting_VariantInfo(False, False, use_file, Database)
                    ) 
                return layout
            else:
                return html.H6("Selected files with different enzymes")
        else:
            return html.H6("Single file selected")
    if 'DrugA_button' == button_id and file_select !=[]:
        if len(file_select) >= 1:
            return AD_dropdown()
        else:
            return "No file selected"

#Call back for main window check box files and top buttons
@app.callback(
    Output('activiate', 'children'),
    [Input('CheckBox_File','value')]
)

def ticked_Files(value):
    if value == None :
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
        return layout
    elif radio is None:
        layout = html.Div(
                html.H4(html.Center('Select plot type from available plots'))
            )
        return layout
    elif check is None:
        layout = html.Div(
                html.H4(html.Center('Select file from loaded files'))
            )
        return layout
    else:
        if len(check) == 0:
            layout = html.Div(
                html.H4(html.Center('Select file from loaded files'))
            )
            return layout
        else:
            figure = Plotly_graph(Plot_points(upLoaded_Details, check), avialable_Plot[int(radio)-1])
            if avialable_Plot[int(radio)-1] == 'Orthographic' or avialable_Plot[int(radio)-1] == 'natural_earth':
                layout = html.Div(
                        children = dcc.Graph(figure = figure)
                    )
                return layout
            else:
                layout = html.Div(
                        children = plot_Layouts(figure)
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