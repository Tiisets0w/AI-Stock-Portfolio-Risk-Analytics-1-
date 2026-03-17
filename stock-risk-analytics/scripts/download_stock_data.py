import yfinance as yf
import pandas as pd

stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

data = yf.download(stocks, start="2018-01-01", end="2024-01-01")

data.to_csv("data/stock_prices.csv")

print("Stock data downloaded successfully!")