import plotly.graph_objects as plot 
from plotly.subplots import make_subplots
import plotly.express as plotex
import math

def Plotly_graph(Plot_info, Plot_type):
    data = []
    figure_data = Plot_info
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
                    file_name = plots[start][2]
                    Enzyme_name = plots[start][3]
                    figure.add_trace(plot.Bar(
                        name = (file_name + ' - ' + Enzyme_name),
                        x = plots[start][0],
                        y = plots[start][1]
                    ), row = row, col=col)
                    start = start + 1
                if col == 2:
                    col = 1
                    row = row + 1
                col = col + 1
                parse_Points= parse_Points + 1
        return figure.show()

fig = plot.Figure(
    data=[plot.Bar(y=[2, 1, 3])],
    layout_title_text="A Figure Displayed with fig.show()"
)
fig.show()  
            
data = [[[['rs28399504', 'rs12769205', 'rs41291556', 'rs17884712', 'rs140278421', 'rs4986893', 'rs6413438', 'rs4244285', 'rs3758581', 'rs118203757', 'rs192154563'], [0.0, 44.03669724770643, 0.0, 0.9174311926605505, 0.0, 0.0, 0.0, 33.02752293577982, 198.1651376146789, 0.0, 0.0], 'Yoruba, Nigeria (YRI) -CYP2C19.vcf', 'CYP2C19']], [[['rs72558187', 
'rs1799853', 'rs7900194', 'rs9332131', 'rs28371685', 'rs1057910', 'rs28371686', 'rs9332239'], [0.0, 0.9433962264150944, 0.0, 0.0, 0.0, 9.433962264150944, 0.0, 0.0], 'SouthHan, China(CHS) -  CYP2C9.vcf', 'CYP2C9']]]

info = Plotly_graph(data, 'Bar_Graph')

        
