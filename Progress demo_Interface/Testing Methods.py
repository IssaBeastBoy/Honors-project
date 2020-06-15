Data_Frame = [['SouthHan, China(CHS) -  CYP2C9.vcf', 'CYP2C9', 'Southern Han Chinese, China - Code: CHS ', [                     rs72558187
Heterogenous Samples         []
Homgeneous Samples           [],                       rs1799853
Heterogenous Samples  [HG00581]
Homgeneous Samples           [],                      rs7900194
Heterogenous Samples        []
Homgeneous Samples          [],                      rs9332131
Heterogenous Samples        []
Homgeneous Samples          [],                      rs28371685
Heterogenous Samples         []
Homgeneous Samples           [],                                                               rs1057910
Heterogenous Samples  [HG00421, HG00457, HG00472, HG00530, HG00543, ...
Homgeneous Samples                                            [HG00419],                      rs28371686
Heterogenous Samples         []
Homgeneous Samples           [],                      rs9332239
Heterogenous Samples        []
Homgeneous Samples          []],   Variants Name  Perentage         Homgeneous Count       Heterogenous Count
0    rs72558187   0.000000                 [0.0, 0]                 [0.0, 0]
1     rs1799853   0.943396                 [0.0, 0]  [0.9433962264150944, 1]
2     rs7900194   0.000000                 [0.0, 0]                 [0.0, 0]
3     rs9332131   0.000000                 [0.0, 0]                 [0.0, 0]
4    rs28371685   0.000000                 [0.0, 0]                 [0.0, 0]
5     rs1057910   8.490566  [0.9433962264150944, 1]   [7.547169811320755, 8]
6    rs28371686   0.000000                 [0.0, 0]                 [0.0, 0]
7     rs9332239   0.000000                 [0.0, 0]                 [0.0, 0]], ['Gambain, The Gambia (GWD)  -  CYP2C9.vcf', 'CYP2C9', 'Gambain, The Gambia - Code: GWD', [
         rs72558187
Heterogenous Samples         []
Homgeneous Samples           [],                       rs1799853
Heterogenous Samples  [HG02769]
Homgeneous Samples           [],                                                  rs7900194
Heterogenous Samples  [HG02643, HG02716, HG02814, HG03538]
Homgeneous Samples                                      [],                                rs9332131
Heterogenous Samples  [HG02628, HG02757]
Homgeneous Samples                    [],                                                              rs28371685
Heterogenous Samples  [HG02465, HG02562, HG02583, HG02629, HG02715, ...
Homgeneous Samples                                                   [],                      rs1057910
Heterogenous Samples        []
Homgeneous Samples          [],                               rs28371686
Heterogenous Samples  [HG02465, HG02610]
Homgeneous Samples                    [],                      rs9332239
Heterogenous Samples        []
Homgeneous Samples          []],   Variants Name  Perentage Homgeneous Count       Heterogenous Count
0    rs72558187   0.000000         [0.0, 0]                 [0.0, 0]
1     rs1799853   0.877193         [0.0, 0]  [0.8771929824561403, 1]
2     rs7900194   3.508772         [0.0, 0]   [3.508771929824561, 4]
3     rs9332131   1.754386         [0.0, 0]  [1.7543859649122806, 2]
4    rs28371685   7.017544         [0.0, 0]   [7.017543859649122, 8]
5     rs1057910   0.000000         [0.0, 0]                 [0.0, 0]
6    rs28371686   1.754386         [0.0, 0]  [1.7543859649122806, 2]
7     rs9332239   0.000000         [0.0, 0]                 [0.0, 0]]]


           
# returns ['File Name', 'Enzyme Name', 'Population', [Dict{Enzy:{homo, hetero}}], Panda(Variant, % , [homoValue, %], [heteroValues, %]) ]
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
                check_Homo = True
            if allele_type == '1|1':
                Homo_gene.append(header[start])
                Hetero_gene.append(None)
                check_Hetero = True
            start = start + 1     
        parse =  parse + 1    
        store_variantInfo = {Pharmaco_Variant[2]:{'Homgeneous Samples': Homo_gene, 'Heterogenous Samples':Hetero_gene}} 
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
        structure = Data_Frame.DataFrame(store_variantInfo)
        allele_info.append(structure)
    compile_Data = {'Variants Name': X_axis, 'Perentage': Y_axis, 'Homgeneous Count': store_HomoCount, 'Heterogenous Count':store_HeteroCount }
    structure = Data_Frame.DataFrame(compile_Data)
    Organized_format.append(allele_info)
    Organized_format.append(structure)
    print()
    print(Organized_format)
    print()
    return Organized_format

Data_Structure(data)