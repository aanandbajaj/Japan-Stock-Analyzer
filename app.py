from flask import Flask, render_template, jsonify
import yfinance as yf
import csv
import os
import json
import pandas as pd
import pytz
from datetime import datetime

app = Flask(__name__)

# Read CSV and fetch ticker symbols and company names
def get_tickers():
    csv_file_path = os.path.join(os.path.dirname(__file__), 'modified_data.csv')
    tickers = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header row
        for row_num, row in enumerate(csv_reader, start=1):
            ticker_symbol = row[0]
            company_name = row[1]
            tickers.append({'symbol': ticker_symbol, 'name': company_name})
    return tickers

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_tickers')
def fetch_tickers():
    tickers = get_tickers()
    return jsonify({'tickers': tickers})

@app.route('/get_company_data/<ticker_symbol>')
def get_company_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    fundamental_data = ticker.info

    # Fetch historical financial statement data
    income_statement = ticker.income_stmt
    balance_sheet = ticker.balance_sheet
    cash_flow_statement = ticker.cashflow

    operating_stats = pd.DataFrame(income_statement.loc['Total Revenue'])
    operating_stats['Revenue Growth'] = operating_stats['Total Revenue'].pct_change(periods=-1) * 100
    operating_stats['Net Income'] = income_statement.loc['Net Income']
    operating_stats['Income Growth'] = operating_stats['Net Income'].pct_change(periods=-1) * 100
    shares = balance_sheet.loc['Ordinary Shares Number']
    statement_dates = pd.to_datetime(income_statement.columns)
    stock_prices = ticker.history(start=statement_dates.min(), end=statement_dates.max())

    # Fetch market cap for each statement date
    # Find the closest matching dates
    # Convert stock_prices.index to timezone-naive timestamps
    stock_prices.index = stock_prices.index.tz_localize(None)

    # Find the closest matching dates
    # Create an empty list to store the closest dates
    closest_dates = []

    # Iterate through each statement date
    for statement_date in statement_dates:
        # Calculate the time difference between statement date and stock_prices.index
        time_diff = abs(stock_prices.index - statement_date)
        # Find the index of the date with the smallest time difference
        closest_idx = time_diff.argmin()
        closest_date = stock_prices.index[closest_idx]
        closest_dates.append(closest_date)

    stock_prices_for_dates = stock_prices.loc[closest_dates]['Close']

    operating_stats['Shares Outstanding'] = shares

    # Convert DataFrames to JSON
    income_statement_dict = json.loads(income_statement.to_json(orient='split'))
    balance_sheet_dict = json.loads(balance_sheet.to_json(orient='split'))
    cash_flow_statement_dict = json.loads(cash_flow_statement.to_json(orient='split'))

    response_data = {
        'company_data': fundamental_data,
        'income_statement': income_statement_dict,
        'balance_sheet': balance_sheet_dict,
        'cash_flow_statement': cash_flow_statement_dict
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
