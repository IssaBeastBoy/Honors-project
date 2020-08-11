from plotly import graph_objs as plot
from plotly.subplots import make_subplots
from plotly import express as plotex
import mysql.connector
import math
import dash
import io
import dash_bootstrap_components as dbc 
import dash_html_components as html 
import dash_core_components as dcc 
import pandas as Data_Frame
import numpy as np 
import os
from os.path import join, isfile
from os import listdir
from PIL import Image 
#from dash_dependencies import Output,Input


upLoad_requirements = []   
           # [ [ FileName, EnzymeName, dict(Population Location:{Latitude, Longitude, Continent, location}), Sample Size, AlleleInfo index, [Variant heading], [file variants] ] ]
upLoaded_Details = []
            # Contains all the global coordinates for all the population groups from 1000 Genome project
Coordinates = {
                'The Gambia':{'Lat': 13.42732173148185, 'Long':-15.303278821874962, 'Continent':'africa', 'location':'The Gambia'},
                'Ibadan':{'Lat': 7.3777462, 'Long':3.8972497, 'Continent': 'africa', 'location':'Ibadan, Nigeria'},
                'Dai':{'Lat': 39.0949984, 'Long':113.0430311, 'Continent': 'asia', 'location':'Xishuangbanna, China'},
                'Beijing':{'Lat': 39.906217, 'Long':116.3912757, 'Continent': 'asia', 'location':'Beijing, China'},
                'Tokyo':{'Lat': 35.6828387, 'Long': 139.7594549, 'Continent': 'asia', 'location':'Tokyo, Japan'},
                'Han':{'Lat': 23.1301964, 'Long': 113.2592945 , 'Continent': 'asia', 'location':'Guangzhou City, China'},
                'Kibh':{'Lat': 10.6497452, 'Long': 106.7619794, 'Continent': 'asia', 'location':'Ho Chi Minh City, Vietnam'},
                'Luhya':{'Lat': 0.607628, 'Long': 34.7687756, 'Continent': 'africa', 'location':'Webuye, Kenya'},
                'Esan':{'Lat': 6.5180735, 'Long': 3.6756969, 'Continent': 'africa', 'location':'Esan, Epe, Nigeria'},
                'Menda':{'Lat': 8.922137, 'Long': -11.9448022, 'Continent': 'africa', 'location':'Mende, Bombali District, Sierra Leone'},
                'Bengali':{'Lat': 24.4768783, 'Long': 90.2932426, 'Continent': 'asia', 'location':'Bangladesh'},
                'Punjabi':{'Lat': 31.5656079, 'Long': 74.3141775, 'Continent': 'asia', 'location':'Lahore, Pakistan'},
                'British/Scotish':{'Lat': 54.7023545, 'Long': -3.2765753, 'Continent': 'europe', 'location':'United Kingdom'},
                'Finnish':{'Lat': 63.2467777, 'Long': 25.9209164, 'Continent': 'europe', 'location':'Finland'},
                'Lberian':{'Lat': 39.3262345, 'Long': -4.8380649, 'Continent': 'europe', 'location':'Spain'},
                'Toscani':{'Lat': 41.8747824, 'Long': 12.453984, 'Continent': 'europe', 'location':'Via Antonio Toscani, Italy'},
                'Colombian':{'Lat': 2.8894434, 'Long': -73.783892, 'Continent': 'south america', 'location':'Colombia'},
                'Peruvian':{'Lat': -12.0621065, 'Long': -77.0365256, 'Continent': 'south america', 'location':'Lima, Peru'},
                'Puerto_Rican':{'Lat': 18.200178, 'Long': -66.664513, 'Continent': 'south america', 'location':' Puerto Rico'},
                'Telugu':{'Lat': 54.7023545, 'Long': -3.2765753, 'Continent': 'europe', 'location':'United Kingdom'},
                'Tami':{'Lat': 54.7023545, 'Long': -3.2765753, 'Continent': 'europe', 'location':'United Kingdom'},
                'African':{'Lat': 31.8160381, 'Long': -99.5120986, 'Continent': 'north america', 'location':'SW USA'},
                'Gujarati':{'Lat': 29.7589382, 'Long': -95.3676974, 'Continent': 'north america', 'location':'Houston, TX <br> United States of America'},
                'Caribbean':{'Lat': 18.4, 'Long': -75, 'Continent': 'Island', 'location':'Haiti'},
                'Mexican':{'Lat': 34.0536909, 'Long': -118.2427666, 'Continent': 'north america', 'location':'Los Angeles, CA <br> United States of America'},
                #'':{'Lat': , 'Long': , 'Continent': '', 'location':''}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
            }

store_Selected = []
                # [[[File Name, EnzymeName, Panda{Coords}, Panda{V_ID:HETERO[], HOMO[]}, Panda{V_ID, Homo[%,Count], HETERO[%,Count]}], [Same_ENZY2]], [ENZY_GROUP2] ]

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

# returns ['File Name', 'Enzyme Name', dict(Population Location:{Latitude, Longitude, Continent, location}), Panda(Enzyme: Variant, homo, hetero ), Panda(Variant, % , [homoValue, %], [heteroValues, %]) ]
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
        store_variantInfo = {Pharmaco_Variant[2]:{'Homgeneous Samples': Homo_gene, 'Heterogenous Samples':Hetero_gene}}
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
def Sort_info(Plot_info, Plot_type):
    Sorted_PlotInfo = []
    if Plot_type == 'Bar_Graph' or Plot_type == 'Scatter':
        if len(Plot_info) == 1:
            Sorted_PlotInfo.append(Plot_info)
            return Sorted_PlotInfo
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
                        index = -1
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
    else:
        return Plot_info     

# returns a list that is grouped per continent
def Sort_continents(Plot_info):
    output = []
    parse = 0
    Plot_info_COPY = []
    while parse < len(Plot_info):
        Plot_info_COPY.append(Plot_info[parse])
        parse = parse + 1 
    parse = 0
    temp = []
    temp.append(Plot_info_COPY[parse])
    del Plot_info_COPY[0]
    if Plot_info_COPY == []:
        output.append(temp)
        return output
    while parse < len(Plot_info_COPY):
        if temp[0][2]['Continent'] == Plot_info_COPY[parse][2]['Continent']:
           temp.append(Plot_info_COPY[parse])
           del Plot_info_COPY[parse]
           parse = 0           
        if parse == (len(Plot_info_COPY) - 1):
            output.append(temp)
            temp = []
            temp.append(Plot_info_COPY[0])
            del Plot_info_COPY[0]            
            parse = 0
        else:
            parse = parse + 1
        if Plot_info_COPY == []:
            output.append(temp)
            return output
    return output

# returns a Panda {latitude, longitude, location, Homogenous, Heterogenous, Average Variant Percentage(%)} 
def variant_Info(figure_data):
    start = 0
    latitude = []
    longitude = []
    location = []
    Homo_detail = []
    Hetero_detail = []
    Enzyme = []
    Marker = []
    while start < len(figure_data):
        latitude.append(figure_data[start][2]['Lat'])
        longitude.append(figure_data[start][2]['Long'])
        location.append(figure_data[start][2]['location'])
        Enzyme.append(figure_data[start][1])
        Homo_data = figure_data[start][4]['Homgeneous Count']
        Hetero_data = figure_data[start][4]['Heterogenous Count']
        parse = 0
        homo_detail = 0
        hetero_detail = 0
        while parse < len(Homo_data):
            homo_detail = homo_detail + Homo_data[parse][0]
            hetero_detail = hetero_detail + Hetero_data[parse][0]
            parse = parse + 1
        homo_detail = (homo_detail/parse)
        hetero_detail = (hetero_detail/parse)
        average = (homo_detail + hetero_detail)/2
        Homo_detail.append(str(homo_detail) + '% <br>')
        Hetero_detail.append( str(hetero_detail) + '% <br>')
        Marker.append(average)
        start = start + 1
    data = {'Enzy':Enzyme, 'Lat':latitude, 'Long':longitude, 'loc': location, 'Homogenous': Homo_detail, 'Heterogenous': Hetero_detail, 'Average Variant Percentage(%)': Marker}
    data = Data_Frame.DataFrame(data)
    return data

# return each plot in its own row using dbc
def plot_Layouts(Plots):
    row = []
    parse = 0
    while parse < len(Plots):
        row_item = dbc.Row(
            children = dcc.Graph( figure = Plots[parse])
        )
        row.append(row_item)
        parse = parse + 1
    return row

# returns a graph base on user selection
def Plotly_graph(Plot_info, Plot_type):
    data = []
    figure_data = Sort_info(Plot_info, Plot_type)
    if Plot_type == 'Bar_Graph':
        parse_Points = 0
        store_Plots = []
        while parse_Points < len(figure_data):
            start = 0
            plots = figure_data[parse_Points]
            figure = plot.Figure()  
            while start < len(plots):                    
                file_name = plots[start][0]
                figure.add_trace(plot.Bar(
                    name = file_name,
                    x = plots[start][4]['Variants ID'],
                    y = plots[start][4]['Percentage']
                    ))
                start = start + 1
            figure.update_layout(title_text= ("Pharmaco variants for " + plots[0][1]), yaxis=dict(title_text="Percentage (%)"), xaxis=dict(title_text="Variant ID"))
            store_Plots.append(figure)   
            parse_Points= parse_Points + 1        
        
        return store_Plots
    
    if Plot_type == 'Scatter':
        store_Plots = []
        parse_Points = 0
        while parse_Points < len(figure_data):
            start = 0
            plots = figure_data[parse_Points]   
            figure = plot.Figure()
            while start < len(plots):                    
                file_name = plots[start][0]
                figure.add_trace(plot.Scatter(
                    name = (file_name),
                    x = plots[start][4]['Variants ID'],
                    y = plots[start][4]['Percentage'],
                    mode = 'markers'
                    ))
                start = start + 1
            figure.update_layout(title_text=("Pharmaco variants for " + plots[0][1]), yaxis=dict(title_text="Percentage (%)"), xaxis=dict(title_text="Variant ID"))
            store_Plots.append(figure)   
            parse_Points= parse_Points + 1

        return store_Plots
    
    if Plot_type != 'Continential':
        data = variant_Info(figure_data)
        if Plot_type == 'Orthographic':        
            figure = plotex.scatter_geo( data_frame= data,
                    lat =  'Lat',
                    lon= 'Long',
                    color = 'Average Variant Percentage(%)',
                    hover_name = 'Enzyme - ' + data['Enzy'] + '<br>' + 'Location - ' + data['loc'] + '<br>' + 'Homogenous variants - '+ data['Homogenous'] + 'Heterogenous variants - '+ data['Heterogenous'],
                    projection= 'orthographic',
                    title = 'Globe: Population Geo-location'
                )
            figure.update_geos(
                    showland = True,
                    showcountries = True,
                    showocean=True
                )
            return figure

        if Plot_type == 'natural_earth':
            figure = plotex.scatter_geo( data_frame= data,
                    lat =  'Lat',
                    lon= 'Long',
                    color = 'Average Variant Percentage(%)',
                    hover_name = 'Enzyme -' + data['Enzy'] + '<br>' + 'Location - ' + data['loc'] + '<br>' + 'Homogenous variants - '+ data['Homogenous'] + 'Heterogenous variants - '+ data['Heterogenous'],
                    projection= 'natural earth',
                    title = 'Flat View: Population Geo-location' 
                )
            figure.update_geos(
                    showland = True,
                    landcolor = "rgb(255, 255, 204)",
                    subunitcolor = "rgb(255, 255, 255)",
                    countrycolor = "rgb(204, 204, 179)",
                    showsubunits = True,
                    showcountries = True,
                    oceancolor="LightBlue",
                    showocean=True
                )
            return figure
    else:
        plot_data = Sort_continents(Plot_info) 
        parse_Points = 0
        subplot_titles  = []
        start = 0
        store_Plots = []        
        while parse_Points < len(plot_data):
            figure = plot.Figure()
            plots = plot_data[parse_Points]            
            scope = plots[0][2]['Continent']
            data = variant_Info(plots)
            figure.add_trace(plot.Scattergeo(
                    lat = data['Lat'],
                    lon= data['Long'],
                    mode = 'markers',
                    marker_color = data['Average Variant Percentage(%)'],
                    text  = 'Enzyme -' + data['Enzy'] + '<br>' + 'Location - ' + data['loc'] + '<br>' + 'Homogenous variants - '+ data['Homogenous'] + 'Heterogenous variants - '+ data['Heterogenous']
                ))
            figure.update_geos(dict(
                    scope = scope,
                    showland = True,
                    landcolor = 'rgb(229, 229, 229)',
                    showcountries = True,
                    subunitcolor = "rgb(255, 255, 255)",
                    countrycolor = "rgb(217, 217, 217)",
                    ))
            parse_Points = parse_Points + 1
            figure.update_layout(title_text=scope.upper())
            store_Plots.append(figure)
        return store_Plots
        
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
def Add_CheckBoxMW(NameList):
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

# returns a shared variants [ {File_Name: {V_ID, {[Homo_Samples], [Hetero_Sample]} }, Enzyme_Name]
def shared_Variants(Enzyme):
    Enzyme = copyList(Enzyme)
    start = 0
    results_SharedV = {}
    file_Names = []
    Enzy_Name = Enzyme[1]
    for key in Enzyme[0]:
        file_Names.append(key)
    Sample_info = Enzyme[0]
    parse = 1
    variants =[]
    for key in Sample_info[file_Names[0]]:
        variants.append(key)
    store_Sample = []
    variant_num = 0
    while variant_num < (len(Sample_info) - 1):
        parse2 = 0
        while parse2 < len(variants):
            if Sample_info[file_Names[parse]].get(variants[parse2]) != None:
                store_Sample.append((variants[parse2], variant_num))
                store_Sample.append((variants[parse2], parse))
            parse2 = parse2 + 1
        if (parse + 1) == len(Sample_info):
            variant_num = variant_num + 1            
            variants =[]   
            for key in Sample_info[file_Names[variant_num]]:
                variants.append(key)            
            parse = variant_num + 1
        else:       
            parse = parse + 1
    samples_info = []
    if store_Sample == []:
        return ([], Enzy_Name)
    File_info = store_Sample[0]
    parse = 1
    nextVariant = 0
    while nextVariant < len(store_Sample) - 1:              
        if File_info == store_Sample[parse]:
            del store_Sample[parse]
            parse = parse - 1
        parse = parse + 1
        if parse == len(store_Sample):
            nextVariant = nextVariant + 1
            File_info = store_Sample[nextVariant]
            parse = nextVariant + 1
    parse = 0
    variants = store_Sample[parse][0]
    name = file_Names[store_Sample[parse][1]]
    save = (name, Enzyme[0][name].get(variants))    
    samples_info.append(save)
    del store_Sample[parse]
    while 0 != len(store_Sample):
        if variants == store_Sample[parse][0]:
            name = file_Names[store_Sample[parse][1]]
            save = (name, Enzyme[0][name].get(variants))            
            samples_info.append(save)
            del store_Sample[parse]
            parse = parse - 1
        parse = parse + 1
        if len(store_Sample) == parse:
            parse = 0
            results_SharedV[variants] = samples_info
            if len(store_Sample) != 0:
                samples_info = []
                variants = store_Sample[parse][0]
    return [results_SharedV, Enzy_Name]

#Copies list into a new list
def copyList(List):
    start = 0
    copy = []
    while start < len(List):
        copy.append(List[start])
        start = start + 1
    return copy

# returns unique variants [ {File_Name: {V_ID, {[Homo_Samples], [Hetero_Sample]} }, Enzyme_Name]
def unique_Variants(Enzyme):
    Enzyme = copyList(Enzyme)
    start = 0
    results_SharedV = {}
    file_Names = []
    Enzy_Name = Enzyme[1]
    for key in Enzyme[0]:
        file_Names.append(key)
    Sample_info = Enzyme[0]
    parse = 0
    store_Sample = []
    while parse < len(Sample_info):
        variants =[]   
        for key in Sample_info[file_Names[parse]]:
            variants.append(key)
        parse2 = 0
        while parse2 < len(variants):
            store_Sample.append((variants[parse2], parse))
            parse2 = parse2 + 1         
        parse = parse + 1
    parse = 0
    samples_info = []    
    variants = store_Sample[parse][0]
    store_Sample = copyList(store_Sample)
    name = file_Names[store_Sample[parse][1]]
    save = (name, Enzyme[0][name].get(variants))
    duplic_Variant = False
    del store_Sample[parse]
    while 0 != len(store_Sample):
        if variants == store_Sample[parse][0]:
            duplic_Variant = True
            store_Sample = copyList(store_Sample)
            del store_Sample[parse]
        parse = parse + 1
        if parse >= len(store_Sample):
            if not duplic_Variant:
                samples_info.append(save)
                results_SharedV[variants] = samples_info
                samples_info = []

            duplic_Variant = False
            parse = 0           
            
            if len(store_Sample) != 0:
                variants = store_Sample[parse][0]
                name = file_Names[store_Sample[parse][1]]
                save = (name, Enzyme[0][name].get(variants))
                store_Sample = copyList(store_Sample)
                del store_Sample[0] 
                if len(store_Sample) == 0:
                    samples_info.append(save)
                    results_SharedV[variants] = samples_info
    return [results_SharedV, Enzy_Name]

# returns a [File_Name :{V_ID, {[Homo_Samples], [Hetero_Sample]} }, Enzyme_Name]
def found_Variants(Enzy_info):  
    start = 0 
    store_information = {}
    enzyme = Enzy_info[0][1]
    while start < len(Enzy_info):
        variants = []
        info = Enzy_info[start]
        name = info[0]
        info_percentage = info[4]['Percentage']
        parse = 0
        while parse < len(info_percentage):
            if info_percentage[parse] > 0:
                variants.append(Enzy_info[start][4]['Variants ID'][parse])                
            parse = parse + 1
        parse = 0
        samples = []
        samples_info = []
        while parse < len(info[3]):
            samples_info.append(info[3][parse])
            parse = parse + 1
        parse = 0        
        store_Variants = {}
        while parse < len(variants):
            parse2 = 0                        
            while parse2 < len(samples_info):
                if samples_info[parse2].get(variants[parse]) != None:
                    store_Variants.update(samples_info[parse2])
                    del samples_info[parse2]
                    break
                parse2 = parse2 + 1
            parse = parse + 1              
        store_information[name] = store_Variants 
        start = start + 1
    results = [store_information, enzyme]
    return results

# returns a string format of the sample data
def Samples_format(samples_Data):
    store_String = ''
    samples = []
    start = 0
    while start < len(samples_Data):
        store_String = store_String + samples_Data[start][0] + ':                                                  \n'
        samples = []
        for key in samples_Data[start][1]:
            samples.append(key)
        parse2 = 0
        while parse2 < len(samples):
            sampleName = samples_Data[start][1].get(samples[parse2])
            store_String = store_String + '\t' + samples[parse2] + ' - '       
            if sampleName == []:
                store_String = store_String + ' None ' + '\n'
            else:
                parse3 = 0
                while parse3 < len(sampleName):
                    store_String = store_String + ' ' + sampleName[parse3]
                    parse3 = parse3 + 1
                store_String = store_String + '\n'
            parse2 = parse2 + 1
        start = start + 1
    return store_String

# returns the html layout for the shared and unique varients table
def setting_VariantInfo(booleanSU, booleanD, variants_Data, Database):
    if not booleanD:
        layout = []
        start = 0
        while start < len(variants_Data) :
            if booleanSU:
                boolSU = False
            else:
                boolSU = True
            enzyme_Info = variants_Data[start]
            if len(enzyme_Info) > 1:
                rows = []
                Variants_found = found_Variants(enzyme_Info)
                if len(Variants_found[0]) > 0:
                    if booleanSU:
                        shared = shared_Variants(Variants_found)
                        info_string = ' shared '
                        header_string = ' Shared '
                    else: 
                        shared = unique_Variants(Variants_found)
                        info_string = ' unique '
                        header_string = ' Unique '
                    if len(shared[0]) > 0:
                        variants = []
                        for key in shared[0]:
                            variants.append(key)
                        dataBase_extraction = get_TableInfo(Database, shared[1])
                        parse = 0
                        table_Rows = []
                        while parse < len(variants):
                            ID = variants[parse]
                            info = 0
                            while info < len(dataBase_extraction):
                                if ID == dataBase_extraction[info][1]:
                                    name = dataBase_extraction[info][2]
                                    position = dataBase_extraction[info][3]
                                    effect = dataBase_extraction[info][4]
                                    del dataBase_extraction[info]
                                    break
                                info = info + 1
                            samples_Data = Samples_format(shared[0].get(variants[parse]))
                            Table_row = html.Tr([html.Td(ID), html.Td(name), html.Td(position), html.Td(effect), html.Td(samples_Data)]) 
                            rows.append(Table_row)
                            parse = parse + 1
                        table_headers = [
                            html.Thead(
                            html.Tr(
                            [
                                html.Th('Variant ID'), html.Th('Variant Name'), html.Th('Position'), html.Th('Effect'), html.Th('Samples with variants')
                            ]))
                        ]
                        heading = html.H5(shared[1] + ' - '+ header_string + ' variants in the selected files') 
                        tabel = dbc.Table(table_headers + rows,bordered = True, dark = boolSU, responsive = True)
                        layout.append(heading)
                        layout.append(tabel)
                    else:
                        heading = html.H5(shared[1] + ' - No'+ info_string +'variants in the selected files')
                        layout.append(heading)
                else:
                    heading = html.H5(Variants_found[1] + ' - No Pharmaco Variants found in the selected files')
                    layout.append(heading)
            
            start = start + 1
        return layout     
    
#Layout for drugs affected Dropdown
def AD_dropdown():
    layout = html.Div(
        [
            html.Div([dbc.Button("Anticoagulation Drugs", id="Antico"), dbc.Collapse(dbc.Card(dbc.CardBody(id = 'anticoagulation')), id = 'anticoagulation_B')]),
            html.Div([dbc.Button("Antidepressants Drugs", id="Antide"), dbc.Collapse(dbc.Card(dbc.CardBody(id = 'antidepressants')), id="antidepressants_B")]),
            html.Div([dbc.Button("Antifungals Drugs", id = 'antifungals'), dbc.Collapse( dbc.Card(dbc.CardBody(id="Antifu")), id="Antifu_B")]),
            html.Div([dbc.Button( "Antipsychotics Drugs", id="Antips"), dbc.Collapse(dbc.Card(dbc.CardBody(id = 'antipsychotics')),id="Antips_B")]),
            html.Div([dbc.Button("Antiretroviral Drugs", id="Antire"), dbc.Collapse(dbc.Card(dbc.CardBody(id = 'antiretroviral')),id="Antire_B")]),
            html.Div([dbc.Button("Antitumor Drugs", id="Antitu"), dbc.Collapse(dbc.Card(dbc.CardBody(id = 'antitumor')),id="Antitu_B")]),
            html.Div([dbc.Button("Beta-Blockers Drugs", id="Bet"), dbc.Collapse(dbc.Card(dbc.CardBody(id = 'beta-blockers')),id="Bet_B")]),
            html.Div([dbc.Button('Immunosuppressive Drugs', id="Immu"), dbc.Collapse(dbc.Card(dbc.CardBody(id = 'immunosuppressive')),id="Immu_B")]),
            html.Div([dbc.Button("Miscellaneous Drugs", id="Mis"), dbc.Collapse(dbc.Card(dbc.CardBody(id = 'Miscellaneous')),id="Mis_B")]),
            html.Div([dbc.Button("NSAIDS Drugs", id = 'NSAIDS'), dbc.Collapse(dbc.Card(dbc.CardBody(id="NSAI")),id="NSAI_B")]),
            html.Div([dbc.Button("Opioids Drugs", id = 'opioids'), dbc.Collapse(dbc.Card(dbc.CardBody(id="Opio")),id="Opio_B")]),
            #dbc.DropdownMenu(label="Drugs", children = [dbc.DropdownMenuItem(id = 'Drugs')], id="Dru")
        ]
    )
    return layout

# return files that can be used for unique, shared variants and enzyme names for affected drugs
def Usable_files(output_Type, selected_Files):
    if output_Type:
        start = 0
        Usable_filesOutput = []
        while start < len(selected_Files):
            loaded_files = selected_Files[start]
            if len(loaded_files) > 1:
                Usable_filesOutput.append(loaded_files)
            start = start + 1
        return Usable_filesOutput
    else:
        start = 0
        selected_Enzymes = []
        while start < len(selected_Files):
            selected_Enzymes.append(selected_Files[start][0][1])
            start = start + 1
        return selected_Enzymes

# returns the table of drugs which are proccessed by the enzyme in question
def drugs_Affected(enzymes, selected_Drug, Database):
    Database = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'PharmacoEnzymeVariantInfo@Thulani971108',
        database = 'enzyme_variantinfo',
        )
    start = 0
    table_color = False
    path = os.getcwd()      
    store_items = []
    path = path + '\\Drugs\\' + selected_Drug
    while start < len(enzymes):
        enzymeName = enzymes[start]
        drugs_detail = get_TableInfo(Database, selected_Drug)
        parse = 0
        drugName = selected_Drug.lower() 
        tableNames = html.Div(html.H6(enzymeName + " metabolized " + selected_Drug))
        store_items.append(tableNames)
        header = [html.Thead(html.Tr([html.Th("Drug Name"), html.Th("Function"), html.Th("Structure"), html.Th("Metabolite(s)")]))]
        Table_rows = []
        while parse < len(drugs_detail):
            affected = False
            drug_Type = drugs_detail[parse]
            involved_Enzy = drug_Type[2]
            Enzy_list = involved_Enzy.split(',')
            find_Enzy = 0
            while find_Enzy < len(Enzy_list):
                if enzymeName == Enzy_list[find_Enzy].strip():
                    structure_Path = path + '\\' + drug_Type[1]
                    structure_List = [
                        join( structure_Path, fn )                    
                        for fn in listdir(structure_Path.strip())           
                        if isfile( join( structure_Path, fn ) ) and fn.lower().endswith(('.png','.jpg'))
                       ]
                    metabolite_Path = structure_Path + '\\' + 'Metabolite(s)'
                    metabolite_List = [ 
                        join( metabolite_Path, fn )                    
                        for fn in listdir(metabolite_Path.strip())           
                        if isfile( join( metabolite_Path, fn ) ) and fn.lower().endswith(('.png','.jpg')) and fn.startswith(enzymeName)
                        ]                          
                    affected = True
                    break
                find_Enzy = find_Enzy + 1
            if affected:
                parse2 = 0
                store_metabolite = []
                while parse2 < len(metabolite_List):
                    metabolite = Image.open(metabolite_List[parse2])
                    store_metabolite.append(html.Img(src = metabolite))
                    store_metabolite.append(html.Br())
                    parse2 = parse2 + 1
                structure = Image.open(structure_List[0])
                row = html.Tr([html.Td(drug_Type[1]), html.Td(drug_Type[3]), html.Td(html.Img(src = structure)), html.Td(html.Div(store_metabolite))])
                Table_rows.append(row)
            parse = parse + 1
        if len(Table_rows) > 0:
            table_body = [html.Tbody(Table_rows)]
            store_items.append(dbc.Table(header + table_body, bordered=True, dark=table_color))
            if table_color:
                table_color = False
            else:
                table_color = True
        else:
            store_items.append(html.Div('Enzyme does not participate in metabolizing any drug in selected category'))
        start = start + 1   
    layout = html.Div(children = store_items)
    return layout

# returns selected table(s) details from database 
def get_TableInfo(Database, Table_name):
    Database_Info = Database.cursor()
    tableName = Table_name.lower()
    Database_Info.execute('SELECT * FROM ' + tableName)
    tabel_contents =  Database_Info.fetchall()
    return tabel_contents

# return the variants from database of the selected CYP enzyme from database
def get_EnzymeVariants(Database, Selected_enzyme):
    Database_Info = Database.cursor()
    enzymeName = Selected_enzyme.lower()
    Database_Info.execute('SELECT Variant_ID FROM ' + enzymeName)
    Enzyme_varaints = Database_Info.fetchall()
    Enzyme_varaints = ConvertTuple2List(Enzyme_varaints)
    return Enzyme_varaints