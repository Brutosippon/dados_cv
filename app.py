from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import requests as rq
from io import BytesIO

app = Dash(__name__)
#aux_heroku_deploy
server = app.server 

url = "https://github.com/Brutosippon/dados_cv/blob/main/db_PIB_stats_capeverde.xlsx?raw=true"
data = rq.get(url).content
df = pd.read_excel(BytesIO(data))

###dataframe para gráfico 1

fig1 = px.bar(df, x="ano", y="Produto_Interno_Bruto", color="Inflacao_Media_Anual", barmode="group")

###dataframe para gráfico 1
fig2 = px.scatter(df, x="ano", y="Population_total",
                 size="Adjusted_net_national_income_per_capita_(current_US$)", color="Life_expectancy_at_birth_total_(years)", hover_name="Stock_da_Divida_Externa_",
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

###definir layout apenas dentro de um único div
app.layout = html.Div(children=[
    html.H1(children='Pró-Estatística'),

    html.H2(children='Dashboard: Com apenas alguns cliques podes ter os principais dados estatísticos de Cabo-Verde. Chegou a hora de simplificar a estatística para quem tem o dia a dia na palma da mão.'),

    html.Div(children='''
        Fonte: The World Bank. 
    '''),
###gráfico 1 
    dcc.Graph(
        id='example-graph',
        figure=fig1
    ),

###gráfico 2
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig2
    ),

###tabela 1 
    html.H4(children='Cabo Verde DataFrame  (2021)'),
    generate_table(df)

])



if __name__ == '__main__':
    app.run_server(debug=True)