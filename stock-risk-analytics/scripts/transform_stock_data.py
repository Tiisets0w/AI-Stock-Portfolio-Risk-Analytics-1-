import pandas as pd

# Load CSV
df = pd.read_csv("data/stock_prices.csv")

# Map your Close columns to stock symbols
close_cols = {
    'Close': 'AAPL',
    'Close.1': 'MSFT',
    'Close.2': 'GOOGL',
    'Close.3': 'AMZN',
    'Close.4': 'TSLA'
}

# Create a new dataframe for processed data
processed_df = pd.DataFrame()
processed_df['Date'] = df['Price']  # 'Price' column is the date

# Calculate metrics for each stock
for col, symbol in close_cols.items():
    processed_df[f'{symbol}_Close'] = pd.to_numeric(df[col], errors='coerce')
    processed_df[f'{symbol}_Daily_Return'] = processed_df[f'{symbol}_Close'].pct_change()
    processed_df[f'{symbol}_Moving_Avg_30'] = processed_df[f'{symbol}_Close'].rolling(window=30).mean()
    processed_df[f'{symbol}_Volatility'] = processed_df[f'{symbol}_Daily_Return'].rolling(window=30).std()

# Save processed data
processed_df.to_csv("data/processed_stock_data.csv", index=False)

print("Data transformation complete for all 5 stocks!")