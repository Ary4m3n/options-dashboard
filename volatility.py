import yfinance as yf
import numpy as np
from scipy.optimize import brentq
from black_scholes import black_scholes_price
from data_fetcher import fetch_stock_data

def historical_volatility(ticker, period="3mo"):
    try:
        data, *_ = fetch_stock_data(ticker, period=period)
        if f'Close {ticker}' in data.columns:
            close_prices = data[f'Close {ticker}']
        elif f'Adj Close {ticker}' in data.columns:
            close_prices = data[f'Adj Close {ticker}']
        else:
            raise ValueError("No 'Close' or 'Adj Close' data found.")

        log_returns = np.log(close_prices / close_prices.shift(1)).dropna()
        return np.std(log_returns) * np.sqrt(252)
    except Exception as e:
        raise ValueError(f"Error calculating historical volatility: {e}")


