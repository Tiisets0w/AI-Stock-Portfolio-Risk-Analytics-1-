import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime

# -----------------------------
# Database connection
# -----------------------------
DB_USER = "postgres"
DB_PASSWORD = "Tiisetso2002#"
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "stock_portfolio_db"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# -----------------------------
# Load stock metrics
# -----------------------------
df_stock_metrics = pd.read_sql("SELECT * FROM stock_metrics", engine)

stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
window = 30  # for moving averages

# -----------------------------
# Predict next-day volatility for each stock
# -----------------------------
predictions = []

for stock in stocks:
    df_stock = df_stock_metrics[["Date", f"{stock}_Daily_Return", f"{stock}_Volatility"]].dropna()
    returns = df_stock[f"{stock}_Daily_Return"].values
    vol = df_stock[f"{stock}_Volatility"].values

    # Prepare features for ML
    X, y = [], []
    for i in range(window, len(returns)):
        X.append(returns[i-window:i])
        y.append(vol[i])

    X = np.array(X)
    y = np.array(y)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict next-day volatility
    last_window = returns[-window:].reshape(1, -1)
    next_vol = model.predict(last_window)[0]

    # Store prediction and all historical predictions
    for date, v in zip(df_stock["Date"], vol):
        predictions.append({
            "Stock": stock,
            "Date": date,
            "Predicted_Volatility": v
        })

    # Add next-day predicted volatility
    predictions.append({
        "Stock": stock,
        "Date": datetime.today().strftime("%Y-%m-%d"),
        "Predicted_Volatility": next_vol
    })

    print(f"{stock} predicted next day volatility: {next_vol:.4f}")

# Convert to DataFrame
df_predicted = pd.DataFrame(predictions)

# -----------------------------
# Calculate 30-day moving averages
# -----------------------------
df_predicted['Vol_MA_30'] = df_predicted.groupby('Stock')['Predicted_Volatility'].transform(lambda x: x.rolling(window).mean())

# -----------------------------
# Upload predicted volatility with moving averages
# -----------------------------
df_predicted.to_sql("predicted_volatility", engine, if_exists="replace", index=False)
print("\nAll predicted volatilities and 30-day MAs uploaded to PostgreSQL!")

# -----------------------------
# Calculate Portfolio Metrics
# -----------------------------
weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])  # equal weights

# Merge daily returns into portfolio calculation
df_returns = df_stock_metrics[['Date'] + [f"{s}_Daily_Return" for s in stocks]].copy()
returns_matrix = df_returns[[f"{s}_Daily_Return" for s in stocks]].values

# Portfolio daily return
df_returns['Portfolio_Return'] = returns_matrix.dot(weights)

# Portfolio rolling volatility
df_returns['Portfolio_Volatility'] = df_returns['Portfolio_Return'].rolling(window).std()

# Portfolio Sharpe ratio (risk-free ~ 0)
df_returns['Portfolio_Sharpe'] = df_returns['Portfolio_Return'] / df_returns['Portfolio_Volatility']

# Upload portfolio metrics to PostgreSQL
df_returns[['Date','Portfolio_Return','Portfolio_Volatility','Portfolio_Sharpe']].to_sql(
    "portfolio_metrics", engine, if_exists="replace", index=False
)
print("Portfolio metrics uploaded to PostgreSQL!")