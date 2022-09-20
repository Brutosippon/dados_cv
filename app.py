from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import requests as rq
from io import BytesIO
from dash_bootstrap_components.themes import BOOTSTRAP

app = Dash(external_stylesheets=[BOOTSTRAP])
server = app.server 


url = "https://github.com/Brutosippon/dados_cv/blob/main/db_PIB_stats_capeverde.xlsx?raw=true"
data = rq.get(url).content
df = pd.read_excel(BytesIO(data))


###dataframe para gráfico 1
to_dropdown_options = list(df.columns)

#@app.callback(
    #Output('dd-output-container', 'children'),
    #Input('demo-dropdown', 'value')
    #)


fig1 = px.bar(df, x="ano", y="Produto_Interno_Bruto", color="Inflacao_Media_Anual", barmode="group")

###dataframe para gráfico 1
fig2 = px.scatter(df, x="ano", y="Population_total",
                 size="Life_expectancy_at_birth_total_(years)", color="Adjusted_net_national_income_per_capita_(current_US$)", hover_name="Stock_da_Divida_Externa_",
                 log_x=True, size_max=60)

###dataframe para tabela 1
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

@app.callback(
    Output('dd-output-container', 'children'),
    Input('dropdown_options', 'value')
)
def update_output(value):
    return f'{value}'


###definir layout apenas dentro de um único div
app.layout = html.Div(className="app-div bg-black text-white black text-center",
    children=[
    html.H1(children='Pró-Estatística'),

    html.H3(children='Dashboard: Com apenas alguns cliques podes ter os principais dados estatísticos de Cabo-Verde.'),
    html.H3(children='Chegou a hora de simplificar a estatística para quem tem o dia a dia na palma da mão.'),
    
    html.Div(children='''
        1º Gráfico. 
    '''),
    
        html.Label('Dropdown'),
        dcc.Dropdown(to_dropdown_options, 'Produto_Interno_Bruto' , id='dropdown_options'),
        html.Div(id='dd-output-container'),
        
###gráfico 1 
    dcc.Graph(
        id='bar-graph',
        figure=(px.bar(df, x="ano", y='Produto_Interno_Bruto', color="Inflacao_Media_Anual", barmode="group")),
        style={'color':'#0a0a0a','text-align':'center'}
    ),
html.Div(children='''
        2º Gráfico. 
    '''),
###gráfico 2
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig2,
        style={'color':'#0a0a0a','text-align':'center'}
    ),

###tabela 1 
    html.H4(children='Cabo Verde DataFrame (2000-2021)'),
    generate_table(df),

    html.Div(children='''
            ------------------
        '''),

    html.H4(children='''
            Copyright 2022. All Rights Reserved João Fidalgo,  Data Source: The World Bank.  
        ''')
    
])




if __name__ == '__main__':
    app.run_server(debug=True)


#if __name__ == '__main__':
    #from os import environ
    #app.run(debug=False, port=environ.get("PORT", 5000), processes=2)