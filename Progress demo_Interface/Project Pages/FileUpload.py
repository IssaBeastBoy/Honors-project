import plotly.graph_objects as go 
import dash
import io
import dash_bootstrap_components as dbc 
import dash_html_components as html 
import dash_core_components as dcc 
#from dash_dependencies import Output,Input

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.css.append_css({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css'})
app.scripts.append_script({'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js'})
app.scripts.append_script({'external_url':'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.bundle.min.js'})
app.config.suppress_callback_exceptions = True



def VCF_FileParse (Files_contents, fileName):
    population_Amount = 0 
    variantInfo= [fileName]
    try:
        if '.vcf' in Files_contents:
            with open(Files_contents) as VCF_fileInfo:

                variants = VCF_fileInfo.readline()
                while True: 
                    variants = VCF_fileInfo.readline()
                    variant = variants.split('\t')

                    if variant[0] == '#CHROM':
                        break            
                while True:

                    variants = VCF_fileInfo.readline()

                    if variants == '':
                        break

                    variant = variants.split('\t')
                    variantInfo.append(variant)
            return variantInfo
        else:
            return html.Div(
            [
                'File not .vcf'
            ]
        )

    except Exception as e:
        return html.Div(
            [
                'There was an error processing this file.'
            ]
        )


