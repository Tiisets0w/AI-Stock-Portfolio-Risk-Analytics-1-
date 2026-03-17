import pandas as pd
from sqlalchemy import create_engine

# Database credentials
DB_USER = "postgres"
DB_PASSWORD = "Tiisetso2002#"
DB_HOST = "localhost"
DB_PORT = "5433"
DB_NAME = "stock_portfolio_db"

# Create connection
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Load CSV
df = pd.read_csv("../data/processed_stock_data.csv")

# Upload to PostgreSQL
df.to_sql("stock_metrics", engine, if_exists="replace", index=False)

print("Data successfully loaded into PostgreSQL!")