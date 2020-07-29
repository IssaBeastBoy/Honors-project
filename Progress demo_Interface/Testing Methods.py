import pandas

data = [[['Gambain, The Gambia (GWD)  -  CYP2C9.vcf', 'CYP2C9', {'Lat': 13.42732173148185, 'Long': -15.303278821874962, 'Continent': 'africa', 'location': 'The Gambia'}, [      
               rs72558187
Heterogenous Samples         []
Homgeneous Samples           [],                       rs1799853
Heterogenous Samples  [HG02769]
Homgeneous Samples           [],                                                  rs7900194
Heterogenous Samples  [HG02643, HG02716, HG02814, HG03538]
Homgeneous Samples                                      [],
      rs9332131
Heterogenous Samples  [HG02628, HG02757]
Homgeneous Samples                    [],
                  rs28371685
Heterogenous Samples  [HG02465, HG02562, HG02583, HG02629, HG02715, ...
Homgeneous Samples                                                   [],
         rs1057910
Heterogenous Samples        []
Homgeneous Samples          [],                               rs28371686
Heterogenous Samples  [HG02465, HG02610]
Homgeneous Samples                    [],                      rs9332239
Heterogenous Samples        []
Homgeneous Samples          []],   Variants ID  Percentage Homgeneous Count       Heterogenous Count
0  rs72558187    0.000000         [0.0, 0]                 [0.0, 0]
1   rs1799853    0.877193         [0.0, 0]  [0.8771929824561403, 1]
2   rs7900194    3.508772         [0.0, 0]   [3.508771929824561, 4]
3   rs9332131    1.754386         [0.0, 0]  [1.7543859649122806, 2]
4  rs28371685    7.017544         [0.0, 0]   [7.017543859649122, 8]
5   rs1057910    0.000000         [0.0, 0]                 [0.0, 0]
6  rs28371686    1.754386         [0.0, 0]  [1.7543859649122806, 2]
7   rs9332239    0.000000         [0.0, 0]                 [0.0, 0]]]]          

def found_Variants(Enzy_info):
    info = Enzy_info[4]['Percentage']
    start = 0
    variants = []
    while start < len(info):
        if info[start]< 0:
            variants.append(info[start])
        start = start + 1
    start = 0
    samples = []
    while start < len(variants):
        samples.append(Enzy_info[3][variants[start]])
        start = start + 1

        
        
found_Variants(data)
