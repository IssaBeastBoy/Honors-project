data = [['Yoruba, Nigeria (YRI) -CYP2C19.vcf', 'CYP2C19', {'Lat': 7.3777462, 'Long': 3.8972497, 'Continent': 'africa', 'location': 'Ibadan, Nigeria'}, [''], ''], ['Lberian, Spain(IBS) - CYP2D6.vcf', 'CYP2D6', {'Lat': 39.3262345, 'Long': -4.8380649, 'Continent': 
'africa', 'location': 'Spain'}, [""], ""],['Lberian, Spain(IBS) - CYP2D6.vcf', 'CYP2D6', {'Lat': 39.3262345, 'Long': -4.8380649, 'Continent': 
'europe', 'location': 'Spain'}, [""], ""]]


           
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
            break
    return output

print(Sort_continents(data))