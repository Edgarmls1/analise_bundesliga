import dash_bootstrap_components as dbc
from dash import Dash, dcc, Input, Output, dash_table, html

from componentes_bl import *


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


#2020
data_20 = request_data(2020)
df_20 = create_df(data_20)
goal_min_20 = goal_minutes(data_20)
wins_20, draws_20, loses_20 = process_results(df_20)
score_20 = process_goals(df_20)
table_20 = create_table(df_20, score_20)
positions_20 = variance_table(df_20)
options_20 = options(df_20)

#2021
data_21 = request_data(2021)
df_21 = create_df(data_21)
goal_min_21 = goal_minutes(data_21)
wins_21, draws_21, loses_21 = process_results(df_21)
score_21 = process_goals(df_21)
table_21 = create_table(df_21, score_21)
positions_21 = variance_table(df_21)
options_21 = options(df_21)

#2022
data_22 = request_data(2022)
df_22 = create_df(data_22)
goal_min_22 = goal_minutes(data_22)
wins_22, draws_22, loses_22 = process_results(df_22)
score_22 = process_goals(df_22)
table_22 = create_table(df_22, score_22)
positions_22 = variance_table(df_22)
options_22 = options(df_22)

#2023
data_23 = request_data(2023)
df_23 = create_df(data_23)
goal_min_23 = goal_minutes(data_23)
wins_23, draws_23, loses_23 = process_results(df_23)
score_23 = process_goals(df_23)
table_23 = create_table(df_23, score_23)
positions_23 = variance_table(df_23)
options_23 = options(df_23)

season_data = {
    "2020": {
        "data": data_20,
        "df": df_20,
        "goal_minutes": goal_min_20,
        "wins": wins_20,
        "draws": draws_20,
        "loses": loses_20,
        "score": score_20,
        "positions": positions_20,
        "options": options_20,
        "table": table_20
    },
    "2021": {
        "data": data_21,
        "df": df_21,
        "goal_minutes": goal_min_21,
        "wins": wins_21,
        "draws": draws_21,
        "loses": loses_21,
        "score": score_21,
        "positions": positions_21,
        "options": options_21,
        "table": table_21
    },
    "2022": {
        "data": data_22,
        "df": df_22,
        "goal_minutes": goal_min_22,
        "wins": wins_22,
        "draws": draws_22,
        "loses": loses_22,
        "score": score_22,
        "positions": positions_22,
        "options": options_22,
        "table": table_22
    },
    "2023": {
        "data": data_23,
        "df": df_23,
        "goal_minutes": goal_min_23,
        "wins": wins_23,
        "draws": draws_23,
        "loses": loses_23,
        "score": score_23,
        "positions": positions_23,
        "options": options_23,
        "table": table_23
    }
}


tables = [season_data['2020']['table'], season_data['2021']['table'], season_data['2022']['table'], season_data['2023']['table']]
seasons = [2020, 2021, 2022, 2023]
new_table = dummies(tables, seasons)


feature_columns = [f'position_{season}' for season in seasons[:-1]]
target_column = f'position_{seasons[-1]}'

data = new_table[['Team'] + feature_columns + [target_column]].dropna()

X = data[feature_columns]
y = data[target_column]

model = LinearRegression()
model.fit(X, y)

def predict(team_name):
    team_data = new_table[new_table['Team'] == team_name]
    if team_data.empty:
        print(f"Time '{team_name}' não encontrado na base de dados.")
        return
    
    team_features = team_data[feature_columns].values
    predicted_position = model.predict(team_features)[0]

 
    return f"A previsão para o time {team_name} é terminar na {round(predicted_position)}ª colocação."

##################################################################################################
# LAYOUT
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Análise Bundesliga", className="text-center my-4"),
                width=12
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("Seleção de Temporada e Times"),
                                dbc.CardBody(
                                    [
                                        dcc.Dropdown(
                                            id='season-dropdown',
                                            value='2023',
                                            options=[
                                                {'label': str(year), 'value': str(year)}
                                                for year in range(2020, 2024)
                                            ],
                                            placeholder="Selecione a temporada",
                                            className="mb-3",
                                        ),
                                        dcc.Dropdown(
                                            id='team-dropdown',
                                            value=[],
                                            multi=True,
                                            placeholder="Selecione os times",
                                            className="mb-3",
                                        ),
                                        dcc.Dropdown(
                                            id='graph-dropdown',
                                            options=[
                                                {'label': 'Tabela', 'value': 'Tabela'},
                                                {'label': 'Mais Gols', 'value': 'Mais Gols'},
                                                {'label': 'Mais Vitórias', 'value': 'Mais Vitórias'},
                                                {'label': 'Mais Empates', 'value': 'Mais Empates'},
                                                {'label': 'Mais Derrotas', 'value': 'Mais Derrotas'},
                                                {'label': 'Minutos dos Gols', 'value': 'Minutos dos Gols'}
                                            ],
                                            value='Tabela',
                                            placeholder="Selecione o tipo de gráfico",
                                            className="mb-3",
                                        ),
                                    ]
                                ),
                            ],
                            className="mb-4"
                        )
                    ],
                    width=4
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("Gráfico"),
                                dbc.CardBody(
                                    dcc.Graph(id='grafico-mais-gols')
                                ),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Tabela"),
                                dbc.CardBody(
                                    dash_table.DataTable(
                                        id='table-output',
                                        columns=[],
                                        data=[],
                                        style_table={'overflowX': 'auto'},
                                        style_cell={'textAlign': 'center'},
                                        style_header={'fontWeight': 'bold'}
                                    )
                                ),
                            ],
                            className="mt-4"
                        ),
                    ],
                    width=8
                ),
            ],
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardHeader("Previsão de Posição"),
                            dbc.CardBody(
                                dcc.Textarea(
                                    id='predict-output',
                                    style={'width': '100%', 'height': '100px'},
                                    readOnly=True
                                )
                            ),
                        ],
                        className="mb-4"
                    )
                ],
                width=12
            )
        ),
    ],
    fluid=True
)
##################################################################################################
# CALLBACK
@app.callback(
    Output('team-dropdown', 'options'),
    [Input('season-dropdown', 'value')]
)
def update_teams(temporada):
    return [{'label': team, 'value': team} for team in season_data[temporada]["options"]]

    
##########################################################################################
@app.callback(
    Output('grafico-mais-gols', 'figure'),
    [Input('season-dropdown', 'value'),
     Input('team-dropdown', 'value'),
     Input('graph-dropdown', 'value')]
)
def update_graph(temporada, equipe, grafico):
    season = season_data[temporada]
    
    score_filtered = season["score"][season["score"]['Team'].isin(equipe)] if 'Todos' not in equipe else season["score"]
    wins_filtered = season["wins"][season["wins"]['Team'].isin(equipe)] if 'Todos' not in equipe else season["wins"]
    draws_filtered = season["draws"][season["draws"]['Team'].isin(equipe)] if 'Todos' not in equipe else season["draws"]
    loses_filtered = season["loses"][season["loses"]['Team'].isin(equipe)] if 'Todos' not in equipe else season["loses"]
    positions_filtered = season["positions"][season["positions"]['Team'].isin(equipe)] if 'Todos' not in equipe else season["positions"]
    data = season["data"]
    
    if grafico == 'Mais Gols':
        return score_graph(score_filtered)
    elif grafico == 'Mais Vitórias':
        return result_graph(wins_filtered)
    elif grafico == 'Mais Empates':
        return result_graph(draws_filtered)
    elif grafico == 'Mais Derrotas':
        return result_graph(loses_filtered)
    elif grafico == 'Tabela':
        return table_variance_plot(positions_filtered, equipe)
    elif grafico == 'Minutos dos Gols':
        return goals_minutes_graph(data)
    
###########################################################################################

@app.callback(
    Output('table-output', 'columns'),
    Output('table-output', 'data'),
    Input('season-dropdown', 'value')
)
def update_table(temporada):

    table_data = season_data[temporada]['table']

    columns = [{"name": col, "id": col} for col in table_data.columns]
    data = table_data.to_dict('records')

    return columns, data


#########################################################################################

@app.callback(
    Output('predict-output', 'value'),
    Input('team-dropdown', 'value')
)
def update_predict(teams):

    if not teams:
        return "Selecione ao menos um time."
    
    predictions = [predict(team) for team in teams]
    return '\n'.join(predictions)


if __name__ == '__main__':
    app.run_server(debug=True)