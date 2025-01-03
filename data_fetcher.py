import pandas as pd
import yfinance as yf

def fetch_stock_data(ticker, period="3mo"):
    try:
        # Fetch the historical data for the given period
        data = yf.download(ticker, period=period)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [' '.join(col).strip() for col in data.columns]

        if data.empty:
            raise ValueError(f"No historical data found for ticker '{ticker}'.")

        # Fetch live data for the most recent 5 days
        ticker_info = yf.Ticker(ticker)
        live_data = ticker_info.history(period="5d", interval="1d")  # Last 5 days, daily interval

        if live_data.empty:
            raise ValueError(f"No live data found for ticker '{ticker}'.")

        # Get the most recent closing price
        if "Close" in live_data.columns:
            last_traded_price = live_data["Close"].iloc[-1]  # Most recent close price
            last_traded_time = live_data.index[-1].strftime('%Y-%m-%d %H:%M:%S')  # Timestamp of the last trade

            # Get the previous close to calculate price change
            if len(live_data["Close"]) > 1:
                previous_close = live_data["Close"].iloc[-2]
            else:
                previous_close = last_traded_price  # Handle edge cases for new listings or limited data

            price_change = last_traded_price - previous_close
            price_change_pct = (price_change / previous_close) * 100
        else:
            raise ValueError(f"'Close' column not available in live data for ticker '{ticker}'.")

        # Fetch the company name
        company_name = ticker_info.info.get("longName", f"Company Name ({ticker.upper()})")

        return (
            data,
            company_name,
            last_traded_price,
            last_traded_time,
            price_change,
            price_change_pct
        )
    except Exception as e:
        raise ValueError(f"Error fetching stock data for '{ticker}': {e}")
