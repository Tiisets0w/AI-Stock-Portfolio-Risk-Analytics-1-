# AI-Driven Stock Portfolio Risk Analytics Platform

## Overview

This project is an end-to-end data analytics and machine learning pipeline that analyzes stock portfolio risk using historical data and AI-based volatility forecasting.

## Features

* Download stock data using Python
* Transform and compute daily returns & volatility
* Store data in PostgreSQL
* Predict stock volatility using Machine Learning (Random Forest)
* Calculate portfolio-level metrics:

  * Portfolio Return
  * Portfolio Volatility
  * Sharpe Ratio
* Compute 30-day moving averages
* Visualize insights using Power BI

## Tech Stack

* Python (Pandas, NumPy, scikit-learn)
* PostgreSQL
* SQLAlchemy
* Power BI

## Project Workflow

1. Download stock data
2. Transform and calculate metrics
3. Load into PostgreSQL
4. Run ML pipeline for volatility prediction
5. Compute portfolio risk metrics
6. Visualize in Power BI

## How to Run

```bash
pip install -r requirements.txt

python scripts/download_stock_data.py
python scripts/transform_stock_data.py
python scripts/load_to_postgres.py
python scripts/full_portfolio_pipeline.py
```

## Screenshots
![alt text](<Screenshot 2026-03-17 160751-1.png>)
![alt text](<Screenshot 2026-03-17 161103.png>)


## Future Improvements

* Deploy dashboard online
* Add real-time data streaming
* Improve ML model accuracy
* Integrate AI-based trading signals
