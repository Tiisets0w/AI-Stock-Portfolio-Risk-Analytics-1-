import pandas as pd
import numpy as np

# Load processed stock data
df = pd.read_csv("data/processed_stock_data.csv")

# Portfolio weights (custom)
weights = {
    "AAPL": 0.25,
    "MSFT": 0.20,
    "GOOGL": 0.20,
    "AMZN": 0.15,
    "TSLA": 0.20
}

# Calculate weighted daily portfolio returns
df["Portfolio_Daily_Return"] = (
    df["AAPL_Daily_Return"] * weights["AAPL"] +
    df["MSFT_Daily_Return"] * weights["MSFT"] +
    df["GOOGL_Daily_Return"] * weights["GOOGL"] +
    df["AMZN_Daily_Return"] * weights["AMZN"] +
    df["TSLA_Daily_Return"] * weights["TSLA"]
)

# Portfolio metrics
portfolio_volatility = df["Portfolio_Daily_Return"].std() * np.sqrt(252)  # annualized
portfolio_mean_return = df["Portfolio_Daily_Return"].mean() * 252        # annualized
sharpe_ratio = portfolio_mean_return / portfolio_volatility               # assume risk-free rate ~0
var_95 = df["Portfolio_Daily_Return"].quantile(0.05)                      # 5% Value at Risk

print("Portfolio Annualized Volatility:", round(portfolio_volatility, 4))
print("Portfolio Annualized Return:", round(portfolio_mean_return, 4))
print("Portfolio Sharpe Ratio:", round(sharpe_ratio, 4))
print("Portfolio Value at Risk (95% confidence):", round(var_95, 4))

# Save portfolio daily returns for AI/modeling
df.to_csv("data/portfolio_returns.csv", index=False)
print("Portfolio returns saved to portfolio_returns.csv")