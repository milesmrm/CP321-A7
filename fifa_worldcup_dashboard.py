# fifa_worldcup_dashboard.py
# Deployed link: https://cp321-a7-bwbq.onrender.com

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Data Preparation
data = [
    {"Year": 1930, "Winner": "Uruguay", "Runner_Up": "Argentina"},
    {"Year": 1934, "Winner": "Italy", "Runner_Up": "Czechoslovakia"},
    {"Year": 1938, "Winner": "Italy", "Runner_Up": "Hungary"},
    {"Year": 1950, "Winner": "Uruguay", "Runner_Up": "Brazil"},
    {"Year": 1954, "Winner": "Germany", "Runner_Up": "Hungary"},
    {"Year": 1958, "Winner": "Brazil", "Runner_Up": "Sweden"},
    {"Year": 1962, "Winner": "Brazil", "Runner_Up": "Czechoslovakia"},
    {"Year": 1966, "Winner": "England", "Runner_Up": "Germany"},
    {"Year": 1970, "Winner": "Brazil", "Runner_Up": "Italy"},
    {"Year": 1974, "Winner": "Germany", "Runner_Up": "Netherlands"},
    {"Year": 1978, "Winner": "Argentina", "Runner_Up": "Netherlands"},
    {"Year": 1982, "Winner": "Italy", "Runner_Up": "Germany"},
    {"Year": 1986, "Winner": "Argentina", "Runner_Up": "Germany"},
    {"Year": 1990, "Winner": "Germany", "Runner_Up": "Argentina"},
    {"Year": 1994, "Winner": "Brazil", "Runner_Up": "Italy"},
    {"Year": 1998, "Winner": "France", "Runner_Up": "Brazil"},
    {"Year": 2002, "Winner": "Brazil", "Runner_Up": "Germany"},
    {"Year": 2006, "Winner": "Italy", "Runner_Up": "France"},
    {"Year": 2010, "Winner": "Spain", "Runner_Up": "Netherlands"},
    {"Year": 2014, "Winner": "Germany", "Runner_Up": "Argentina"},
    {"Year": 2018, "Winner": "France", "Runner_Up": "Croatia"},
    {"Year": 2022, "Winner": "Argentina", "Runner_Up": "France"},
]

df = pd.DataFrame(data)

# Count wins per country
win_counts = df['Winner'].value_counts().reset_index()
win_counts.columns = ['Country', 'Wins']

# Dash App
app = Dash(__name__)
app.title = 'FIFA World Cup Dashboard'

app.layout = html.Div([
    html.H1('FIFA World Cup Finals Dashboard', style={"textAlign": "center"}),

    html.H3("Choropleth Map of World Cup Winners"),
    dcc.Graph(id='choropleth-map'),

    html.Label("Select a country to see number of wins:"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in sorted(df['Winner'].unique())],
        value='Brazil'
    ),
    html.Div(id='country-win-output', style={'marginBottom': '30px'}),

    html.Label("Select a year to see final match result:"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': y, 'value': y} for y in sorted(df['Year'].unique())],
        value=2022
    ),
    html.Div(id='year-result-output')
])

@app.callback(
    Output('choropleth-map', 'figure'),
    Input('country-dropdown', 'value')
)
def update_map(_):
    fig = px.choropleth(win_counts,
                        locations="Country",
                        locationmode='country names',
                        color="Wins",
                        hover_name="Country",
                        color_continuous_scale=px.colors.sequential.Plasma)
    fig.update_layout(title_text='Number of FIFA World Cups Won by Country')
    return fig

@app.callback(
    Output('country-win-output', 'children'),
    Input('country-dropdown', 'value')
)
def display_country_wins(country):
    wins = win_counts.loc[win_counts['Country'] == country, 'Wins']
    if not wins.empty:
        return f"{country} has won the World Cup {wins.values[0]} time(s)."
    else:
        return f"{country} has never won the World Cup."

@app.callback(
    Output('year-result-output', 'children'),
    Input('year-dropdown', 'value')
)
def display_year_result(year):
    row = df[df['Year'] == year]
    if not row.empty:
        winner = row.iloc[0]['Winner']
        runner_up = row.iloc[0]['Runner_Up']
        return f"In {year}, {winner} won the World Cup. Runner-up: {runner_up}."
    else:
        return f"No data available for {year}."

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
