import pandas as pd
import requests
import plotly.express as px

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def request_data(temporada):
    response = requests.get(f'https://www.openligadb.de/api/getmatchdata/bl1/{temporada}')

    if response.status_code == 200:
        matches = response.json()
    else:
        print(f"Erro ao acessar a API: {response.status_code}")
        matches = []

    return matches

def create_df(matches):
    data = []
    for match in matches:
        match_date = match['matchDateTimeUTC']
        home_team = match['team1']['teamName']
        away_team = match['team2']['teamName']
        home_score = match['matchResults'][-1]['pointsTeam1']
        away_score = match['matchResults'][-1]['pointsTeam2']
        
        data.append([match_date, home_team, away_team, home_score, away_score])

    df = pd.DataFrame(data, columns=['Date', 'HomeTeam', 'AwayTeam', 'HomeScore', 'AwayScore'])

    df['Date'] = pd.to_datetime(df['Date'])

    return df

def goal_minutes(matches):
    goal_minutes = []
    for match in matches:
        if "goals" in match and match["goals"]:
            for goal in match["goals"]:
                if "matchMinute" in goal:
                    goal_minutes.append(goal["matchMinute"])
                    
    return goal_minutes

def options(df):
    opcoes = list(df.HomeTeam.sort_values().unique())
    opcoes.append('Todos')

    return opcoes

def variance_table(df):
    pos = pd.DataFrame()
    for date in df['Date'].unique():
        current_matches = df[df['Date'] <= date]
        home_points = current_matches.groupby('HomeTeam')['HomePoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'HomePoints': 'Points'})
        away_points = current_matches.groupby('AwayTeam')['AwayPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'AwayPoints': 'Points'})

        draw_points_home = current_matches.groupby('HomeTeam')['DrawPoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'DrawPoints': 'Points'})
        draw_points_away = current_matches.groupby('AwayTeam')['DrawPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'DrawPoints': 'Points'})
        
        total_draw_points = pd.concat([draw_points_home, draw_points_away]).groupby('Team').sum().reset_index()
        
        total_points = pd.concat([home_points, away_points, total_draw_points]).groupby('Team').sum().reset_index()
        
        total_points['Date'] = date
        total_points['Positions'] = total_points['Points'].rank(method='min', ascending=False)
        
        pos = pd.concat([pos, total_points])

    return pos
    
def process_results(df):
    wins = []
    draws = []
    loses = []

    for i in df.index:
        if df.iloc[i]['HomeScore'] > df.iloc[i]['AwayScore']:
            wins.append(df.iloc[i]['HomeTeam'])
            loses.append(df.iloc[i]['AwayTeam'])
        elif df.iloc[i]['HomeScore'] < df.iloc[i]['AwayScore']:
            loses.append(df.iloc[i]['HomeTeam'])
            wins.append(df.iloc[i]['AwayTeam'])
        else:
            draws.append(df.iloc[i]['HomeTeam'])
            draws.append(df.iloc[i]['AwayTeam'])

    wins = pd.DataFrame(wins, columns=['Team'])
    draws = pd.DataFrame(draws, columns=['Team'])
    loses = pd.DataFrame(loses, columns=['Team'])

    wins = wins['Team'].value_counts().reset_index()
    loses = loses['Team'].value_counts().reset_index()
    draws = draws['Team'].value_counts().reset_index()

    wins.columns = ['Team', 'Count']
    loses.columns = ['Team', 'Count']
    draws.columns = ['Team', 'Count']
    
    return wins, draws, loses

def process_goals(df):
    home_score = df.groupby('HomeTeam')['HomeScore'].sum().sort_values(ascending=False).reset_index()
    home_score.columns = ['Team', 'Goals']
    
    away_score = df.groupby('AwayTeam')['AwayScore'].sum().sort_values(ascending=False).reset_index()
    away_score.columns = ['Team', 'Goals']
    
    total_score = pd.concat([home_score, away_score])
    total_score = total_score.groupby('Team')['Goals'].sum().sort_values(ascending=False).reset_index()
    
    return total_score

def create_table(df, total_score):
    df['HomeWin'] = (df['HomeScore'] > df['AwayScore']).astype(int)
    df['AwayWin'] = (df['AwayScore'] > df['HomeScore']).astype(int)

    df['HomePoints'] = df['HomeWin'] * 3
    df['AwayPoints'] = df['AwayWin'] * 3
    df['DrawPoints'] = ((df['HomeScore'] == df['AwayScore']) * 1).astype(int)

    home_points = df.groupby('HomeTeam')['HomePoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'HomePoints': 'Points'})
    away_points = df.groupby('AwayTeam')['AwayPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'AwayPoints': 'Points'})
    total_points = pd.concat([home_points, away_points]).groupby('Team').sum().reset_index()
    draw_points_home = df.groupby('HomeTeam')['DrawPoints'].sum().reset_index().rename(columns={'HomeTeam': 'Team', 'DrawPoints': 'DrawPoints'})
    draw_points_away = df.groupby('AwayTeam')['DrawPoints'].sum().reset_index().rename(columns={'AwayTeam': 'Team', 'DrawPoints': 'DrawPoints'})
    total_draw_points = pd.concat([draw_points_home, draw_points_away]).groupby('Team').sum().reset_index()

    team_stats = total_points.merge(total_score, on='Team')
    team_stats.sort_values('Points', ascending=False, inplace=True)
    table = team_stats.drop('Goals', axis=1).reset_index()
    table.drop('index', axis=1, inplace=True)

    table = table.merge(total_draw_points, on='Team', how='left')
    table['Points'] += table['DrawPoints']
    table.drop('DrawPoints', axis=1, inplace=True)

    return table

def result_graph(df):
    fig = px.bar(df, x = 'Count', y = 'Team')
    fig.update_yaxes(autorange = 'reversed')
    return fig

def score_graph(df):
    fig = px.bar(df, x = 'Goals', y = 'Team')
    fig.update_yaxes(autorange = 'reversed')
    return fig

def table_variance_plot(positions, teams):
    teams = teams
    team_positions = positions[positions['Team'].isin(teams)]

    fig = px.line(team_positions, x = 'Date', y = 'Positions', color='Team', markers=True)

    fig.update_yaxes(autorange = 'reversed', range = [0,18])

    return fig

def goals_minutes_graph(data):
    all_goal_minutes = []
    all_goal_minutes.extend(goal_minutes(data))


    fig = px.histogram(
        x=all_goal_minutes, 
        nbins=45, 
        template="plotly_white"
    )
    fig.update_layout(
        bargap=0.2
    )

    return fig

# Regressão Linear

def dummies(tables, seasons):
    new_table = None
    
    for table, season in zip(tables, seasons):
        table = table.reset_index(drop=True)
        table = table.iloc[:-3]
        
        table[f'position'] = table.index + 1 

        for i in range(1, 19):  
            table[f'pos_{i}'] = (table.index == i - 1).astype(int)  

        table = table.add_suffix(f'_{season}')
        table = table.rename(columns={f'Team_{season}': 'Team'})

        if new_table is None:
            new_table = table.copy()
        else:
            new_table = pd.merge(new_table, table, on='Team', how='outer')
            
    return new_table