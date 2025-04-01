import dash
from dash import dcc, html
import pandas as pd
import numpy as np
import plotly.graph_objs as go

# Load Data
returns = pd.read_csv("selected_stock_returns.csv", index_col=0, parse_dates=True)
nifty_returns = pd.read_csv("nifty_returns.csv", index_col=0, parse_dates=True)

# MVO Optimized Weights
mvo_weights = {
    'BALKRISIND': 0.0264, 'BAJAJ-AUTO': 0.1736, 'HDFCBANK': 0.1366,
    'HINDUNILVR': 0.2000, 'INFY': 0.0949, 'HCLTECH': 0.1051,
    'ADANIENT': 0.0119, 'APLAPOLLO': 0.0515, 'ABBOTINDIA': 0.2000
}

weights = np.array(list(mvo_weights.values()))
stock_names = [s + '.NS' for s in mvo_weights.keys()]
weights /= np.sum(weights)

# Compute Portfolio Returns
portfolio_returns = returns[stock_names].dot(weights)
cumulative_returns = (1 + portfolio_returns).cumprod()
cumulative_nifty = (1 + nifty_returns['^NSEI']).cumprod()

def rebalance_portfolio(returns, initial_weights, rebalance_freq):
    rebalance_dates = returns.resample(rebalance_freq).first().index
    weights = np.array(list(initial_weights.values()))
    weights /= np.sum(weights)
    
    rebalanced_returns = []
    start_date = returns.index[0]

    for i in range(len(rebalance_dates) - 1):
        end_date = rebalance_dates[i + 1]
        period_returns = returns.loc[start_date:end_date].dot(weights)
        rebalanced_returns.append(period_returns)
        weights = np.array(list(initial_weights.values()))
        weights /= np.sum(weights)
        start_date = end_date

    return pd.concat(rebalanced_returns)

def calculate_annual_return(cumulative_returns):
    total_years = (cumulative_returns.index[-1] - cumulative_returns.index[0]).days / 365
    return (cumulative_returns.iloc[-1] ** (1 / total_years)) - 1

annual_return_mvo = calculate_annual_return(cumulative_returns)
annual_return_nifty = calculate_annual_return(cumulative_nifty)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Portfolio Performance", style={'text-align': 'center'}),

    html.Div([
        html.Label("Select Portfolio Type:"),
        dcc.Dropdown(
            id='portfolio-type-dropdown',
            options=[
                {'label': 'MVO Portfolio (No Rebalancing)', 'value': 'no_rebalancing'},
                {'label': 'Rebalanced Portfolio', 'value': 'rebalanced'}
            ],
            value='rebalanced',
            style={'width': '50%'}
        )
    ], style={'margin': '20px'}),

    html.Div([
        html.Label("Select Rebalancing Frequency (For Rebalanced Portfolio):"),
        dcc.Dropdown(
            id='rebalance-dropdown',
            options=[
                {'label': 'Monthly', 'value': 'M'},
                {'label': 'Quarterly', 'value': 'Q'},
                {'label': 'Half-Yearly', 'value': '2Q'}
            ],
            value='2Q',
            style={'width': '50%'}
        )
    ], style={'margin': '20px'}),

    dcc.Graph(id='cumulative-performance'),

    html.Div([
        html.H3("Performance Metrics", style={'text-align': 'center'}),
        html.Table(id='performance-table')
    ], style={'margin-top': '20px'})
])

@app.callback(
    [dash.dependencies.Output('cumulative-performance', 'figure'),
     dash.dependencies.Output('performance-table', 'children')],
    [dash.dependencies.Input('portfolio-type-dropdown', 'value'),
     dash.dependencies.Input('rebalance-dropdown', 'value')]
)
def update_chart(portfolio_type, rebalance_freq):
    if portfolio_type == 'no_rebalancing':
        selected_cumulative = cumulative_returns
        annual_return = annual_return_mvo
        portfolio_name = "MVO Portfolio (No Rebalancing)"
    else:
        rebalanced_portfolio_returns = rebalance_portfolio(returns[stock_names], mvo_weights, rebalance_freq)
        selected_cumulative = (1 + rebalanced_portfolio_returns).cumprod()
        annual_return = calculate_annual_return(selected_cumulative)
        portfolio_name = f"MVO Portfolio (Rebalanced {rebalance_freq})"

    figure = {
        'data': [
            go.Scatter(x=selected_cumulative.index, y=selected_cumulative, mode='lines',
                       name=portfolio_name, line=dict(color='blue', width=2)),
            go.Scatter(x=cumulative_nifty.index, y=cumulative_nifty, mode='lines',
                       name='NIFTY 50', line=dict(color='orange', width=2, dash='dot'))
        ],
        'layout': go.Layout(
            title=f'Cumulative Returns: {portfolio_name} vs NIFTY 50',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Cumulative Returns'),
            legend=dict(x=0, y=1),
            template='plotly_white'
        )
    }

    table_children = [
        html.Tr([html.Th("Portfolio Type"), html.Th("Annual Return")]),
        html.Tr([html.Td(portfolio_name), html.Td(f"{annual_return:.2%}")]),
        html.Tr([html.Td("NIFTY 50"), html.Td(f"{annual_return_nifty:.2%}")])
    ]

    return figure, table_children

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)