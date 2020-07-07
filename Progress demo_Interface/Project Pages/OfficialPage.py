import mysql.connector
import base64
import dash
import dash_bootstrap_components as dbc 
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output, State, ALL, State, Match, ALLSMALLER
from plotly import graph_objs as plot

from HomePage import Homepage
from UploadPage import Upload, PharmacoInformation
from Methods import VCF_FileParse, Coordinates, Plot_points, Add_CheckBoxMW, selected_Files, setting_CheckBOXMW, upLoaded_Details, Pharmaco_VariantParse, get_EnzymeVariants, Plotly_graph
from MainWindow import MainWindow, storeOptions
from MW_Topbuttons import share_Variants, unique_Variants, drug_Affected, SU_button, AV_button, DrugA_button, AlleleInfo_button, AI

Database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'PharmacoEnzymeVariantInfo@Thulani971108',
    database = 'enzyme_variantinfo',
    )

            # [ Variant heading, [Pharmaco variants contained in VCF file] ]
File_details = []

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
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
    [Input('enzyme', 'value')]
)

def EnzyFamily(value):
    if (PharmacoInformation[0] == '') and (value is None):
        layout = html.Div(
            html.Center('*Fill in up the field above', style={"color":"rgb(255,0,0)"})
        )
    else:
        layout = html.Div('')
    return layout

#Call back for CYP1 family radio buttons
@app.callback(
     Output('outputCYP1', 'children'),
    [Input('CYP1', 'value')]
)

def CYP1(value):
     if value != None:
        enzy = ['CYP1A1', 'CYP1A2']
        PharmacoInformation[0]= enzy[int(value)-1]

#Call back for CYP2 family radio buttons
@app.callback(
     Output('outputCYP2', 'children'),
    [Input('CYP2', 'value')]
) 

def CYP2(value):
    if value != None: 
        enzy = ['CYP2A6', 'CYP2C8', 'CYP2C9','CYP2C19', 'CYP2D6', 'CYP2E1', 'CYP2F1']
        PharmacoInformation[0]= enzy[int(value)-1]

#Call back for CYP3 family radio buttons
@app.callback(
     Output('outputCYP3', 'children'),
    [Input('CYP3', 'value')]
)

def CYP3(value):
    if value != None: 
        enzy = ['CYP3A4', 'CYP3A5', 'CYP3A43']
        PharmacoInformation[0]= enzy[int(value)-1]
#Call back for population dropdown
@app.callback(
    Output('output_pop', 'children'),
    [Input('population', 'value')]
)

def populationGroup(value):
    if (PharmacoInformation[1] == '') and (value is None):
        layout = html.Div(
            html.Center('*Fill in up the field above', style={"color":"rgb(255,0,0)"})
        )
    else:
        layout = html.Div('')
    return layout
    
#Call back for African population radio buttons
@app.callback(
     Output('output_AF', 'children'),
    [Input('AF', 'value')]
)

def AF(value):
    if value != None: 
        popu = ['Esan', 'The Gambia', 'Luhya','Menda', 'Ibadan']
        PharmacoInformation[1]= popu[int(value)-1]


#Call back for East Asia population radio buttons
@app.callback(
     Output('output_EA', 'children'),
    [Input('EA', 'value')]
)

def EA(value):
    if value != None: 
        popu = ['Dai', 'Beijing', 'Tokyo', 'Kibh', 'Han']
        PharmacoInformation[1]= popu[int(value)-1]

#Call back for South Asia population radio buttons
@app.callback(
     Output('output_SA', 'children'),
    [Input('SA', 'value')]
)

def SA(value):
    if value != None: 
        popu = ['Bengali', 'Punjabi']
        PharmacoInformation[1]= popu[int(value)-1]

#Call back for American population radio buttons
@app.callback(
     Output('output_AM', 'children'),
    [Input('AM', 'value')]
)

def AM(value):
    if value != None: 
        popu = ['Colombian', 'Peruvian', 'Puerto_Rican']
        PharmacoInformation[1]= popu[int(value)-1]

#Call back for Ancestry population radio buttons
@app.callback(
     Output('output_AN', 'children'),
    [Input('AN', 'value')]
)

def AN(value):
    if value != None: 
        popu = ['Telugu', 'Tami', 'African', 'Caribbean', 'Gujarati', 'Mexican']
        PharmacoInformation[1]= popu[int(value)-1]

#Call back for European population radio buttons
@app.callback(
     Output('output_EU', 'children'),
    [Input('EU', 'value')]
)

def EU(value):
    if value != None: 
        popu = ['British/Scotish', 'Finnish', 'Lberian', 'Toscani']
        PharmacoInformation[1]= popu[int(value)-1]

#Call back for Non Specfic population radio buttons
@app.callback(
     Output('output_NA', 'children'),
    [Input('NA', 'value')]
)

def N_A(value):
    if value != None: 
        PharmacoInformation[1]= 'None Specfic'
        
#Call back for shared variant button
@app.callback(
    Output('Info_PlayGround1', 'children'),
    [Input('SV_button', 'n_clicks')]
)

def SV_action(n_clicks):
    if n_clicks is None :
        layout = html.Div(
            [
                SU_button
            ]
        )
    if n_clicks != None :
        layout = html.Div(
            [
                share_Variants
            ]
        )
    return layout


#Call back for unique variant button
@app.callback(
    Output('Info_PlayGround2', 'children'),
    [Input('UV_button', 'n_clicks')]
)

def UV_action(n_clicks):
    if n_clicks is None :
        layout = html.Div(
            [
                AV_button
            ]
        )
    if n_clicks != None :
        layout = html.Div(
            [
                unique_Variants
            ]
        )
    return layout

#Call back for affected drugs button
@app.callback(
    Output('Info_PlayGround3', 'children'),
    [Input('DrugA_button', 'n_clicks')]
)

def DrugA_action(n_clicks):
    if n_clicks is None :
        layout = html.Div(
            [
                DrugA_button
            ]
        )
    if n_clicks >= 1 :
        layout = html.Div(
            [
                drug_Affected
            ]
        )
    return layout

#Call back for  closin shared variant dropdown
@app.callback(
    Output('Share_Vinfo', 'children'),
    [Input('Back_ToSVB', 'n_clicks')]
)

def SV_close(n_clicks):
    if n_clicks is None :
        layout = html.Div(
            [
                share_Variants
            ]
        )
    if n_clicks != None:
        layout = html.Div(
            [
                SU_button                
            ]
        )
    return layout

#Call back for closing unique variant dropdown
@app.callback(
    Output('Unique', 'children'),
    [Input('Back_ToUVB', 'n_clicks')]
)

def UV_close(n_clicks):
    if n_clicks is None :
        layout = html.Div(
            [
                unique_Variants
            ]
        )
    if n_clicks != None :
        layout = html.Div(
            [
                AV_button                
            ]
        )
    return layout

#Call back for  closing affected drugs dropdown
@app.callback(
    Output('Drug_A', 'children'),
    [Input('Back_ToDrugAB', 'n_clicks')]
)

def DrugA_close(n_clicks):
    if n_clicks is None :
        layout = html.Div(
            [
                drug_Affected
            ]
        )
    if n_clicks != None:
        layout = html.Div(
            [
                DrugA_button                
            ]
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
    [Input('Plot_Options', 'value')]
)

def Figure(value):
    avialable_Plot = ['Bar_Graph', 'Scatter', 'Orthographic', 'natural_earth', 'Continential']    
    if value is None:
        if len(selected_Files) == 0:
            layout = html.Div(
                html.H4(
                    html.Center('Select file \n and \n plot type')
                )
            )
        else:
            layout = html.Div(
                html.H4(html.Center('Select plot type'))
            )
    else:
        if len(selected_Files) == 0:
            layout = html.Div(
                html.H4(
                    html.Center('Select .vcf file \n')
                )
            )
        else:
            figure = Plotly_graph(Plot_points(upLoaded_Details, selected_Files), avialable_Plot[int(value)-1])
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

#Call back for allele present button
@app.callback(
    Output('Info_PlayGround4', 'children'),
    [Input('AI_button', 'n_clicks')]
)

def Allele_action(n_clicks):
    if n_clicks is None :
        layout = html.Div(
            [
                AlleleInfo_button
            ]
        )
    if n_clicks != None :
        layout = html.Div(
            [
                AI
            ]
        )
    return layout

#Call back for  closing the allele information dropdown
@app.callback(
    Output('AI', 'children'),
    [Input('Back_ToAIB', 'n_clicks')]
)

def Alleleinfo_close(n_clicks):
    if n_clicks is None :
        layout = html.Div(
            [
                AI
            ]
        )
    if n_clicks >= 1 :
        layout = html.Div(
            [
                AlleleInfo_button                
            ]
        )
    return layout

if __name__ == '__main__':
    app.run_server(debug=False)