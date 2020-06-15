import plotly.graph_objects as plot 
from plotly.subplots import make_subplots
import plotly.express as plotex
import math
import dash
import io
import dash_bootstrap_components as dbc 
import dash_html_components as html 
import dash_core_components as dcc 
import pandas as Data_Frame
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

# return [Data_Structure]
def Plot_points (uploaded_info, selected_Files):
    store_Data = []
    start = 0
    while start< len(selected_Files):
        selected = uploaded_info[int(selected_Files[start])-1]
        store_Data.append(Data_Structure(selected))
        start = start + 1
    return store_Data


# returns ['File Name', 'Enzyme Name', 'Population', Panda(Enzyme: Variant, homo, hetero ), Panda(Variant, % , [homoValue, %], [heteroValues, %]) ]
def Data_Structure (Input_VCFdata):
    Organized_format = []
    Organized_format.append(Input_VCFdata[0])
    Organized_format.append(Input_VCFdata[1])
    Organized_format.append(Input_VCFdata[2])
    header = Input_VCFdata[5]    
    parse = 0
    X_axis = []
    Y_axis = []
    store_HomoCount = []
    store_HeteroCount = []
    allele_info = []
    variant_Data = Input_VCFdata[6]
    while parse < len(variant_Data):
        Hetero_gene = []
        Homo_gene = []
        start = Input_VCFdata[4]        
        Pharmaco_Variant = variant_Data[parse]
        X_axis.append(Pharmaco_Variant[2])
        while start < len(Pharmaco_Variant):
            allele_type  = Pharmaco_Variant[start]
            if allele_type == '0|1' or allele_type == '1|0':
                Hetero_gene.append(header[start])
                Homo_gene.append(None)
            if allele_type == '1|1':
                Homo_gene.append(header[start])
                Hetero_gene.append(None)
            start = start + 1     
        parse =  parse + 1            
        store_variantInfo = Data_Frame.DataFrame({Pharmaco_Variant[2]:{'Homgeneous Samples': Homo_gene, 'Heterogenous Samples':Hetero_gene}})
        allele_info.append(store_variantInfo)
        start = 0
        while start < len(Hetero_gene):
            if Hetero_gene[start] == None:                
                del Hetero_gene[start]
                start = 0
            else:
                start = start + 1            
        start = 0
        while start < len(Homo_gene):
            if Homo_gene[start]== None:
                del Homo_gene[start]
                start = 0
            else:
                start = start + 1
        variant_Count = ((len(Hetero_gene) + len(Homo_gene)) * 100) / Input_VCFdata[3]
        Y_axis.append(variant_Count)
        Homogene_count = (len(Homo_gene)* 100)/ Input_VCFdata[3]
        store_HomoCount.append([Homogene_count, len(Homo_gene)])
        Heterogene_count = (len(Hetero_gene)* 100)/ Input_VCFdata[3]
        store_HeteroCount.append([Heterogene_count,len(Hetero_gene)])  
    compile_Data = {'Variants ID': X_axis, 'Percentage': Y_axis, 'Homgeneous Count': store_HomoCount, 'Heterogenous Count':store_HeteroCount }
    Organized_format.append(allele_info)
    structure = Data_Frame.DataFrame(compile_Data)
    Organized_format.append(structure)    
    return Organized_format

# returns a list of plot information grouped in same enzymes
def Sort_info(Plot_info):
    Sorted_PlotInfo = []
    if len(Plot_info) == 1:
        return Plot_info
    else:
        Sorted = []
        Sorted.append(Plot_info[0])
        enzyme = Plot_info[0][1]
        del Plot_info[0]
        while True:
            index  = 0                       
            while index < len(Plot_info):
                if enzyme == Plot_info[index][1]:
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
            enzyme = Plot_info[0][1]
            del Plot_info[0]
    return Sorted_PlotInfo           

# returns a graph base on user selection
def Plotly_graph(Plot_info, Plot_type):
    data = []
    figure_data = Sort_info(Plot_info)
    if Plot_type == 'Bar_Graph':
        if len(Plot_info) == 1: 
            start = 0
            while start < len(Plot_info):
                file_name = Plot_info[start][0]
                Enzyme_name = Plot_info[start][1]
                data.append(plot.Bar(
                    name = (file_name + ' - ' + Enzyme_name),
                    x = Plot_info[start][4]['Variants ID'],
                    y = Plot_info[start][4]['Percentage']
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
                specs.append([{'colspan': 2}, None])
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
                        x = plots[start][4]['Variants ID'],
                        y = plots[start][4]['Percentage']
                    ), row = row, col=col)
                    start = start + 1
                figure.update_xaxes(title_text="Variant ID", row=row, col=col)
                figure.update_yaxes(title_text="Percentage (%)", row=row, col=col)
                    
                
                if col == 2:
                    col = 0
                    row = row + 1
                col = col + 1
                parse_Points= parse_Points + 1
        figure.update_layout(title_text="Pharmaco variants found"
                                )
        return figure
    if Plot_type == 'Scatter':
        if len(Plot_info) == 1:
            start = 0
            while start < len(Plot_info):
                file_name = Plot_info[start][0]
                Enzyme_name = Plot_info[start][1]
                data.append(plot.Scatter(
                    name = (file_name + ' - ' + Enzyme_name),
                    x = Plot_info[start][4]['Variants ID'],
                    y = Plot_info[start][4]['Percentage'],
                    mode = 'markers'
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
                specs.append([{'colspan': 2}, None])
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
                    figure.add_trace(plot.Scatter(
                        name = (file_name + ' - ' + Enzyme_name),
                        x = plots[start][4]['Variants ID'],
                        y = plots[start][4]['Percentage'],
                        mode = 'markers'
                    ), row = row, col=col)
                    start = start + 1
                figure.update_xaxes(title_text="Variant ID", row=row, col=col)
                figure.update_yaxes(title_text="Percentage (%)", row=row, col=col)
                    
                
                if col == 2:
                    col = 0
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