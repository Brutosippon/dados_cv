from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import requests as rq
from io import BytesIO
from dash_bootstrap_components.themes import BOOTSTRAP
from bs4 import BeautifulSoup

app = Dash(external_stylesheets=[BOOTSTRAP])
server = app.server 

url = "https://github.com/Brutosippon/dados_cv/blob/main/db_PIB_stats_capeverde.xlsx?raw=true"
data = rq.get(url).content
df = pd.read_excel(BytesIO(data))

to_dropdown_options = list(df.columns)

#create an application that reads the excel file and Simple Interactive Dash App with Interactive Visualizations, Indicators example from the previous chapter by updating the time series when we hover over points in our scatter plot.

###dataframe para tabela 1
    ##dataframe para gráfico 1

fig1 = px.bar(df, x="ano", y='Produto_Interno_Bruto' , color="Inflacao_Media_Anual", barmode="group")

fig2 = px.scatter(df, x="ano", y="Produto_Interno_Bruto", size="Life_expectancy_at_birth_total_(years)", color="Adjusted_net_national_income_per_capita_(current_US$)", hover_name="Stock_da_Divida_Externa_",
                    log_x=True, size_max=60)

fig3 = px.line(df, x="ano", y="Produto_Interno_Bruto", color="Inflacao_Media_Anual", line_group="Inflacao_Media_Anual", hover_name="Inflacao_Media_Anual", line_shape="spline", render_mode="svg")
##################################################################################
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


###definir layout apenas dentro de um único div
app.layout = html.Div(className="app-div bg-black text-white black text-center",
    children=[
    html.H1(children='Pró-Estatística'),

    html.H3(children='Dashboard: Com apenas alguns cliques podes ter os principais dados estatísticos de Cabo-Verde.'),
    html.H3(children='Chegou a hora de simplificar a estatística para quem tem o dia a dia na palma da mão.'),
    html.Div(children='''
            ------------------------ 
        '''), 
    html.H4(children='Cabo Verde DataFrame (2000-2021)'),
###gráfico 1 
    html.Div(children='''
        1º Gráfico. 
    '''), 
        dcc.Graph(id='graph1', figure=fig1),


 
html.Div(children='''
        2º Gráfico. 
    '''),
###gráfico 2
dcc.Graph(id='graph2', figure=fig2),

###tabela 1 
    #generate_table(df),


html.H3(children='Configuração dos gráficos'),
    html.Label('Eixo do Y dos Gráficos'),
    dcc.Dropdown(to_dropdown_options, 'Produto_Interno_Bruto' , id='y_axis_column', className="app-div bg-black text-black text-center"),
    #Dropdown para escolher a cor do fig1
    html.Label('Eixo do Cor do Gráfico 1'),
    dcc.Dropdown(to_dropdown_options, 'Inflacao_Media_Anual' , id='color_axis_fig1', className="app-div bg-black text-black text-center"),
    #Dropdown para fig2 escolher size="Life_expectancy_at_birth_total_(years)", color="Adjusted_net_national_income_per_capita_(current_US$)"
    html.Label('Eixo do Size do Gráfico 2'),
    dcc.Dropdown(to_dropdown_options, 'Life_expectancy_at_birth_total_(years)' , id='size_axis_fig2', className="app-div bg-black text-black text-center"),
    html.Label('Eixo do Cor do Gráfico 2'),
    dcc.Dropdown(to_dropdown_options, 'Adjusted_net_national_income_per_capita_(current_US$)' , id='color_axis_fig2', className="app-div bg-black text-black text-center"),


    html.Div(children='''
            ------------------
        '''),

    html.H4(children='''
            Copyright 2022. All Rights Reserved João Fidalgo,  Data Source: The World Bank.  
        ''')
    
])

to_dropdown_options = list(df.columns)

#create a app.callback for the dropdown to update dcc.Graph(id='graph1', figure=fig1)
# create app.callback for id graph1 px.bar
@app.callback(
    Output('graph1', 'figure'),
    Input('y_axis_column', 'value'),
    Input('color_axis_fig1', 'value')
    )


def update_graph(y_axis_column_name,color_axis_fig1_name):
    fig1 = px.bar(df, x="ano", y=y_axis_column_name, color=color_axis_fig1_name , barmode="group")
    return fig1


# create app.callback for id graph2 px.scatter
@app.callback(
    Output('graph2', 'figure'),
    Input('y_axis_column', 'value'),
    Input('size_axis_fig2', 'value'),
    Input('color_axis_fig2', 'value')
    )

def update_graph(y_axis_column_name,size_axis_fig2_name,color_axis_fig2_name):
    fig2 = px.scatter(df, x="ano", y=y_axis_column_name, size=size_axis_fig2_name, color=color_axis_fig2_name, hover_name="Stock_da_Divida_Externa_",
                    log_x=True, size_max=60)
    return fig2


def update_output(value):
    return 'You have selected "{}"'.format(value)




###########################################################



if __name__ == '__main__':
    app.run_server(debug=True)

#if __name__ == '__main__':
    #from os import environ
    #app.run(debug=False, port=environ.get("PORT", 5000), processes=2)
