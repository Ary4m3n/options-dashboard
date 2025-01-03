from dash import Dash, dcc, html, Input, Output, State, dash_table
import dash
import dash_bootstrap_components as dbc
import numpy as np
from data_fetcher import fetch_stock_data
from volatility import historical_volatility
from black_scholes import black_scholes_price, calculate_greeks
from visualization import plot_payoff
import plotly.graph_objects as go

# Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# App layout
app.layout = html.Div([
    dcc.Store(id="volatility-store", data=30.0),
    # Search Bar Container
    html.Div([
        dcc.Input(
            id="ticker-input",
            type="text",
            placeholder="Enter stock ticker (e.g., AAPL)",
            className="search-bar"
        ),
        dbc.Button("Submit", id="submit-ticker", color="primary", className="search-button"),
        dbc.Toast(
            id="error-toast",
            header="Error",
            icon="danger",
            duration=4000,
            is_open=False,
            dismissable=True,
            style={"position": "fixed", "top": 10, "right": 10, "width": 300}
        )
    ], className="search-container"),

    # Main container with sidebar and content
    html.Div([
        # Sidebar
        html.Div([
            html.H3("Options Dashboard", className="sidebar-title"),
            html.Label("Strike Price:", className="slider-label"),
            dcc.Slider(
                id="strike-price",
                min=100, max=300, step=1, value=150,
                marks=None,
                tooltip={"always_visible": False},
                className="slider"
            ),
            html.Div(id="strike-price-value", className="slider-value"),

            html.Label("Time to Maturity (Years):", className="slider-label"),
            dcc.Slider(
                id="time-to-maturity",
                min=0.1, max=2, step=0.1, value=0.25,
                marks=None,
                tooltip={"always_visible": False},
                className="slider"
            ),
            html.Div(id="time-to-maturity-value", className="slider-value"),

            html.Label("Interest Rate (%):", className="slider-label"),
            dcc.Slider(
                id="interest-rate",
                min=0, max=10, step=0.1, value=2,
                marks=None,
                tooltip={"always_visible": False},
                className="slider"
            ),
            html.Div(id="interest-rate-value", className="slider-value"),
        ], className="sidebar"),

        # Main content
        html.Div([
            # Information Box
            dbc.Alert(
                "Explore how option prices fluctuate with varying 'Strike Prices', 'Time to Maturities' and 'Interest Rates'. A historical measure (3mo) of Volatility for each stock has been used. Click on the 'Call Value' or 'Put Value' cards to view the corresponding payoff diagram. You can observe the impact of different parameters on the option greeks too.",
                color="primary",
                className="info-box",
                style={
                    "textAlign": "center",
                    "fontSize": "16px",
                    "fontWeight": "bold",
                    "padding": "10px",
                    "marginBottom": "20px"
                }
            ),

            # Stock Information
            html.Div([
                html.Div(id="company-name", className="company-name"),
                html.Div([
                    html.Span(id="current-price", className="current-price"),
                    html.Span(id="stock-change", className="stock-change"),
                    html.Span(id="stock-change-pct", className="stock-change-pct")
                ], className="price-line"),
                html.Div(id="close-time", className="close-time"),
                # Historical Volatility Line
                html.Div([
                    html.Label("Historical Volatility (%):"),
                    dcc.Input(
                        id="volatility-input",
                        type="number",
                        value=30.0,
                        min=0,
                        max=100,
                        step=0.1,
                        style={"width": "150px", "margin-left": "10px"}
                    )
                ], className="volatility-container", style={"margin-top": "10px"})
            ], id="stock-info", className="stock-info"),

            # Output Cards
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4("CALL Value", className="card-title"),
                                    html.H2(id="call-value", className="card-value"),
                                ]),
                                className="call-card",
                            ),
                            id="call-card",
                            style={"cursor": "pointer"}, 
                            n_clicks=0
                        ),
                        width={"size": 3, "offset": 1},
                    ),
                    dbc.Col(
                        html.Div(
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4("PUT Value", className="card-title"),
                                    html.H2(id="put-value", className="card-value"),
                                ]),
                                className="put-card",
                            ),
                            id="put-card",
                            style={"cursor": "pointer"},
                            n_clicks=0
                        ),
                        width={"size": 3},
                    ),
                ],
                justify="center",
                className="output-cards"
            ),

            # Payoff diagram
            html.Div([
                # Heading for the graph
                html.Div(
                    "Option Payoff Diagram",
                    className="graph-heading"
                ),
                # Graph
                dcc.Graph(id="payoff-diagram", className="payoff-diagram")
            ], className="graph-container"),

            # Greeks Table Section
            html.Div([
                # Heading for the Greeks Table
                html.Div(
                    "Option Greeks",
                    className="graph-heading"
                ),
                # Greeks Table
                html.Div([
                    dash_table.DataTable(
                        id="greeks-table",
                        columns=[
                        {"name": "Option Type", "id": "option_type"},
                        {"name": "Delta", "id": "Delta"},
                        {"name": "Gamma", "id": "Gamma"},
                        {"name": "Theta", "id": "Theta"},
                        {"name": "Vega", "id": "Vega"},
                        {"name": "Rho", "id": "Rho"},
                        ],
                        style_cell={"textAlign": "center", "padding": "5px"},
                        style_table={"marginTop": "20px", "width": "80%", "marginLeft": "auto", "marginRight": "auto"},
                        style_header={"backgroundColor": "#f4f4f9", "fontWeight": "bold"},
                    )
                ], id="greeks-container"),
            ], className="graph-container"),
        ], className="content"),
    ], className="main-container")
])

@app.callback(
    [
        Output("error-toast", "is_open"),
        Output("error-toast", "children"),
        Output("company-name", "children"),
        Output("current-price", "children"),
        Output("stock-change", "children"),
        Output("stock-change", "style"),
        Output("stock-change-pct", "children"),
        Output("stock-change-pct", "style"),
        Output("close-time", "children"),
        Output("strike-price", "min"),
        Output("strike-price", "max"),
        Output("strike-price", "value"),
    ],
    [Input("submit-ticker", "n_clicks")],
    [State("ticker-input", "value")]
)
def update_ticker(n_clicks, ticker):
    if not n_clicks or not ticker:
        return False, "", "", "", "", {}, "", {}, "", 100, 300, 150

    try:
        # Fetch stock data and company name
        (
            stock_data,
            company_name,
            last_traded_price,
            last_traded_time,
            price_change,
            price_change_pct
        ) = fetch_stock_data(ticker)

        # Determine colors for positive and negative changes
        color = "green" if price_change > 0 else "red"

        return (
            False, "",
            f"{company_name} ({ticker.upper()})",
            f"${last_traded_price:.2f}",
            f"{price_change:+.2f}",
            {"color": color, "font-weight": "bold"},
            f"({price_change_pct:+.2f}%)",
            {"color": color, "font-weight": "bold"},
            f"Last traded at: {last_traded_time}",
            max(1, last_traded_price * 0.5), last_traded_price * 1.5, last_traded_price
        )
    except Exception as e:
        return True, str(e), "", "", "", {}, "", {}, "", 100, 300, 150

# Callback to update slider values dynamically
@app.callback(
    [Output("strike-price-value", "children"),
     Output("time-to-maturity-value", "children"),
     Output("interest-rate-value", "children")],
    [Input("strike-price", "value"),
     Input("time-to-maturity", "value"),
     Input("interest-rate", "value")]
)
def update_slider_values(strike_price, time_to_maturity, interest_rate):
    return (
        f"Strike Price: ${strike_price:.2f}",
        f"Time to Maturity: {time_to_maturity:.2f} years",
        f"Interest Rate: {interest_rate:.2f}%"
    )

# Callback to update the main dashboard with option calculations
@app.callback(
    [Output("call-value", "children"),
     Output("put-value", "children"),
     Output("payoff-diagram", "figure")],
    [Input("strike-price", "value"),
     Input("time-to-maturity", "value"),
     Input("interest-rate", "value"),
     Input("volatility-input", "value"),
     Input("call-card", "n_clicks"),
     Input("put-card", "n_clicks")],
    [State("current-price", "children"),
     State("ticker-input", "value")]
)
def update_dashboard(K, T, r, sigma, call_clicks, put_clicks, current_price_str, ticker):
    ctx = dash.callback_context
    if not current_price_str:
        # Default empty figure
        default_figure = go.Figure()
        default_figure.update_layout(
            xaxis_title="Stock Price",
            yaxis_title="Payoff",
            template="plotly_white",
            xaxis=dict(range=[200, 300]),
            yaxis=dict(range=[-50, 50]),
            margin=dict(l=0, r=0, t=30, b=30)
        )
        return "", "", default_figure

    try:
        current_price = float(current_price_str.replace("$", ""))
        sigma = sigma / 100
        r = r / 100

        # Calculate option prices
        call_price = black_scholes_price(current_price, K, T, r, sigma, option_type="call")
        put_price = black_scholes_price(current_price, K, T, r, sigma, option_type="put")

        # Determine which payoff diagram to display
        stock_prices_min = min(current_price, K) * 0.8
        stock_prices_max = max(current_price, K) * 1.2
        stock_prices = np.linspace(stock_prices_min, stock_prices_max, 100)

        if ctx.triggered_id == "call-card":
            payoff_fig = plot_payoff(stock_prices, K, option_type="call")
        elif ctx.triggered_id == "put-card":
            payoff_fig = plot_payoff(stock_prices, K, option_type="put")
        else:
            # Default to call option if no card clicked yet
            payoff_fig = plot_payoff(stock_prices, K, option_type="call")

        return f"${call_price:.2f}", f"${put_price:.2f}", payoff_fig

    except Exception as e:
        return f"Error: {str(e)}", f"Error: {str(e)}", go.Figure()

    
@app.callback(
    Output("greeks-table", "data"),
    [
        Input("strike-price", "value"),
        Input("time-to-maturity", "value"),
        Input("interest-rate", "value"),
        Input("volatility-input", "value"),
    ],
    [
        State("current-price", "children"),
        State("ticker-input", "value"),
    ]
)
def update_greeks_table(K, T, r, sigma, current_price_str, ticker):
    if not current_price_str:
        return []

    try:
        # Convert current price to float
        current_price = float(current_price_str.replace("$", ""))
        sigma = sigma / 100

        # Calculate Greeks for Call and Put options
        call_greeks = calculate_greeks(current_price, K, T, r / 100, sigma, option_type="call")
        put_greeks = calculate_greeks(current_price, K, T, r / 100, sigma, option_type="put")

        # Convert numpy.float64 to Python float
        call_greeks = {key: round(float(value), 5) for key, value in call_greeks.items()}
        put_greeks = {key: round(float(value), 5) for key, value in put_greeks.items()}

        # Prepare data for DataTable
        table_data = [
            {"option_type": "Call", **call_greeks},
            {"option_type": "Put", **put_greeks}
        ]

        return table_data
    except Exception as e:
        return [{"option_type": "Error", "Delta": str(e), "Gamma": "", "Theta": "", "Vega": "", "Rho": ""}]

@app.callback(
    Output("volatility-store", "data"),
    [Input("submit-ticker", "n_clicks")],
    [State("ticker-input", "value")]
)
def fetch_volatility(n_clicks, ticker):
    if not n_clicks or not ticker:
        return 30.0
    try:
        sigma = historical_volatility(ticker, period="3mo")
        return round(sigma * 100, 2)
    except Exception:
        return 30.0

@app.callback(
    Output("volatility-input", "value"),
    Input("volatility-store", "data")
)
def update_volatility_input(stored_volatility):
    return stored_volatility

if __name__ == "__main__":
    app.run_server(debug=True)