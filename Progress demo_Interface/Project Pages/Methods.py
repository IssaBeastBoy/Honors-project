import plotly.graph_objects as plot 
from plotly.subplots import make_subplots
import plotly.express as plotex
import math
import dash
import io
import dash_bootstrap_components as dbc 
import dash_html_components as html 
import dash_core_components as dcc 
import pandas as data_format
import numpy as np 
#from dash_dependencies import Output,Input



upLoad_requirements = []      
            # [ int(Value) of the uploaded file that are selected at the checkBox ]          
selected_Files = []
            # [ [ FileName, EnzymeName, PopulationGroup, Sample Size, AlleleInfo index, [Variant heading], [file variants] ] ]
upLoaded_Details = []

# returns [ [Variant heading], Sample Size, AlleleInfo index, [file variants] ]
def VCF_FileParse (Files_contents, fileName):
    variants_Data = []
            #[ heading ,VCF file name, [ Variants ]]
    variantInfo= []
    file_data = Files_contents.split('\n')
    start = 0
    Sample_size = 0
    Start_Index = 0
    try:
        while True: 
            variants = file_data[start]
            variant = variants.split('\t')

            if variant[0] == '#CHROM':
                variantInfo.append(variant)
                index = 0
                INCREMENT = False
                while index < len(variant):

                    if variant[index] == 'FORMAT' and INCREMENT == False:
                        Start_Index = index
                        INCREMENT = True
                        
                    if INCREMENT == True:
                        Sample_size =  Sample_size + 1
                    index = index + 1
                break            
            start = start + 1
        start = start + 1
        while start < len(file_data):

            variants = file_data[start]

            start = start + 1

            variant = variants.split('\t')
            if variant[0] == '':
                break
            variants_Data.append(variant)
        variantInfo.append(Sample_size)  
        variantInfo.append(Start_Index)  
        variantInfo.append(variants_Data) 
        return variantInfo

    except Exception as e:
        return html.Div(
            [
                'There was an error processing this file.'
            ]
        )

# returns the points for the selected files
def Plot_points (upLoaded_Details, selected_Files):
    start = 0
              # [ [ Panda(Variant Name, Percentages), File Name,  Enzyme Name] ]                
    plot_info = []
    while start < len(selected_Files):
        X_axis = []
        Y_axis = []
        parse_Variant = 0 

        while parse_Variant < len(upLoaded_Details[start][6]):
            X_axis.append(upLoaded_Details[start][6][parse_Variant][2])
            parse_attributes = 0
            probe_position = upLoaded_Details[start][4]
            attributes =  upLoaded_Details[start][6]
            attributes = attributes[parse_Variant][probe_position-1]
            FORMAT_attributes = attributes.split(';')

            while parse_attributes < len(FORMAT_attributes):
                attributes = FORMAT_attributes[parse_attributes]
                attribute = attributes.split('=')

                if attribute[0] == 'AC':
                    frequency = attribute[1]
                    percentage = ( int(frequency)/int(upLoaded_Details[start][3]) )* 100
                    Y_axis.append(percentage)
                    break

                parse_attributes = parse_attributes + 1
            parse_Variant = parse_Variant + 1  
        data = {'Variant Name': X_axis, 'Percentage': Y_axis} 
        data_Fo = data_format.DataFrame(data) 
        axis = [data_Fo, upLoaded_Details[start][0], upLoaded_Details[start][1]]
        plot_info.append(axis)
        start = start + 1 
    return plot_info

# returns a list of plot information grouped in same enzymes
def Sort_info(Plot_info):
    Sorted_PlotInfo = []
    if len(Plot_info) == 1:
        return Plot_info
    else:
        Sorted = []
        Sorted.append(Plot_info[0])
        enzyme = Plot_info[0][2]
        del Plot_info[0]
        while True:
            index  = 0                       
            while index < len(Plot_info):
                if enzyme == Plot_info[index][2]:
                    Sorted.append(Plot_info[index])                    
                    del Plot_info[index]
                if len(Plot_info) == 0:
                    if len(Sorted) > 0:
                        Sorted_PlotInfo.append(Sorted)
                    return Sorted_PlotInfo
                index = index + 1
            index = 0
            save_info = []
            while index < len(Sorted):
                save_info.append(Sorted[index])
                index = index + 1
            Sorted_PlotInfo.append(save_info)
            Sorted.clear()
            if len(Plot_info) == 0:
                if len(Sorted) > 0:
                    Sorted_PlotInfo.append(Sorted)
                return Sorted_PlotInfo
            Sorted.append(Plot_info[0])
            enzyme = Plot_info[0][2]
            del Plot_info[0]
    return Sorted_PlotInfo           

# returns a graph base on user selection
def Plotly_graph(Plot_info, Plot_type):
    data = []
    figure_data = Sort_info(Plot_info)
    if Plot_type == 'Bar_Graph':
        subplot_layout = len(figure_data)
        if subplot_layout == 1: 
            start = 0
            while start < len(Plot_info):
                file_name = Plot_info[start][2]
                Enzyme_name = Plot_info[start][3]
                data.append(plot.Bar(
                    name = (file_name + ' - ' + Enzyme_name),
                    x = Plot_info[start][0],
                    y = Plot_info[start][1]
                    ))
                start = start + 1
            figure = plot.Figure(data = data)
            figure.update_layout(
                                barmode = 'group',
                                title_text = 'Pharmaco variant found',
                                xaxis = dict(
                                    title = 'Variant ID',
                                    titlefont_size=16,
                                    tickfont_size=14,
                                    ),
                                yaxis = dict(
                                    title ='Percentage (%)',
                                    titlefont_size=16,
                                    tickfont_size=14,
                                    )
                                )
        else:
            domains = []
            specs = []
            start = 0
            while start < len(figure_data):
                domains.append({})    
                if len(domains) == 2:        
                    specs.append(domains)
                    domains = []
                start = start + 1
            if start%2 != 0:
                specs.append([{'colspan': 2}, None ])
            rows = math.ceil(len(figure_data)/2)
            figure = make_subplots(
                            rows=rows, cols=2, specs= specs)
            parse_Points = 0
            col = 1
            row = 1
            while parse_Points < len(figure_data):
                start = 0
                plots = figure_data[parse_Points]
                while start < len(plots):
                    file_name = plots[start][1]
                    Enzyme_name = plots[start][2]
                    figure.add_trace(plot.Bar(
                        name = (file_name + ' - ' + Enzyme_name),
                        x = plots[start][0]['Variant Name'],
                        y = plots[start][0]['Percentage']
                    ), row = row, col=col)
                    start = start + 1
                figure.update_xaxes(title_text="Variant ID", row=row, col=col)
                figure.update_yaxes(title_text="Percentage (%)", row=row, col=col)
                    
                
                if col == 2:
                    col = 1
                    row = row + 1
                col = col + 1
                parse_Points= parse_Points + 1
        figure.update_layout(title_text="Pharmaco variants found"
                                )
        return figure

# returns [  Sample Size, AlleleInfo index, [Variant heading], [Pharmaco variants contained in VCF file] ]
def Pharmaco_VariantParse(PharmacoVariants, VCF_Filedetails):
    variants = VCF_Filedetails[3]
    Pharmaco_Variants = []
    start = 0
    while start < len(variants):
        index = 0
        while index < len(PharmacoVariants):     
            if variants[start][2] == PharmacoVariants[index]:
                Pharmaco_Variants.append(variants[start])
            index = index + 1
        start = start + 1
    VCF_Filedetails[3] =  Pharmaco_Variants
    return VCF_Filedetails
    
# returns a new option form for uploaded file
def Add_CheckBoxMW( NameList):
    option = {}
    store = []
    start = 0
    while start<len(NameList) :
        name =  NameList[start]
        option['label'] = name        
        key = start +1
        option['value'] = str(key)
        store.append(option)
        option = {}
        start = start + 1 
    return store

# returns a html design including newly uploaded vcf files
def setting_CheckBOXMW(option):
    if len(option) == 0:
        layout = html.Div([
             html.Center(html.B('Loaded files')),
             html.P('No files uploaded') 
        ])
    else:
        layout = html.Div([
            html.Center(html.B('Loaded files')),
            dcc.Checklist(
                            id='CheckBox_File',
                            options= option,
                            labelStyle={'display': 'inline-block'})
                          
        ])
    return layout

# returns the converted tuple from database requery into a list form
def ConvertTuple2List(DatabaseInfo_return):
    store_Data = []
    start = 0
    while start < len(DatabaseInfo_return):
        tupleIndex = DatabaseInfo_return[start]
        store_Data.append(tupleIndex[0])
        start = start + 1
    return store_Data

# return the variants from database of the selected CYP enzyme from database
def get_EnzymeVariants(Database, Selected_enzyme):
    Database_Info = Database.cursor()
    enzymeName = Selected_enzyme.lower()
    Database_Info.execute('SELECT Variant_ID FROM ' + enzymeName)
    Enzyme_varaints = Database_Info.fetchall()
    Enzyme_varaints = ConvertTuple2List(Enzyme_varaints)
    return Enzyme_varaints