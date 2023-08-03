import pandas as pd
from alpha_vantage.timeseries import TimeSeries

def get_stock_data(api_key, ticker, start_date, end_date):
    try:
        # Initialize Alpha Vantage API client
        ts = TimeSeries(key=api_key, output_format='pandas')

        # Get the stock data
        data, meta_data = ts.get_daily(symbol=ticker, outputsize='full')

        # Reset the index to make 'date' a regular column
        data.reset_index(inplace=True)

        # Convert the 'date' column to a pandas datetime object
        data['date'] = pd.to_datetime(data['date'])

        print("Data retrieved from API:")
        print(data.head())

        # Filter the data based on date range
        data = data.loc[(data['date'] >= start_date) & (data['date'] <= end_date)]

        # Rename the '1. open' column to 'open'
        data.rename(columns={'1. open': 'open', '2. high':'high', '3. low':'low', '4. close':'close', '5. volume':'volume'}, inplace=True)

        print("Data after filtering:")
        print(data.head())

        return data

    except Exception as e:
        # Handle any exceptions, including Alpha Vantage API related errors
        print(f"Error occurred while fetching data: {e}")
        return None


# Example usage:
if __name__ == "__main__":
    api_key = "YDWKDAAZXT30QQVP"
    ticker = "AAPL"  # Replace with the desired stock symbol
    start_date = "2023-07-01"  # Replace with the desired start date
    end_date = "2023-08-02"  # Replace with the desired end date

    stock_data = get_stock_data(api_key, ticker, start_date, end_date)

    if stock_data is not None:
        print(stock_data)
