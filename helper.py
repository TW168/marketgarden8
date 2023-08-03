import pandas as pd
import streamlit as st
from alpha_vantage.timeseries import TimeSeries

@st.cache_data
def get_stock_data(api_key, ticker, start_date, end_date):
    """
    Fetches daily stock data for a given ticker from the Alpha Vantage API.

    Parameters:
        api_key (str): Your Alpha Vantage API key.
        ticker (str): Ticker symbol of the stock (e.g., 'AAPL' for Apple Inc.).
        start_date (str): Start date for the data (format: 'YYYY-MM-DD').
        end_date (str): End date for the data (format: 'YYYY-MM-DD').

    Returns:
        pd.DataFrame: A DataFrame containing the stock data with columns 'date', 'open', 'high', 'low', 'close', and 'volume'.
    """
    try:
        # Initialize Alpha Vantage API client
        ts = TimeSeries(key=api_key, output_format='pandas')

        # Get the stock data
        data, meta_data = ts.get_daily(symbol=ticker, outputsize='full')
        # st.write("meta_data: ", meta_data)
        # Reset the index to make 'date' a regular column
        data.reset_index(inplace=True)

        # Convert the 'date' column to a pandas datetime object
        data['date'] = pd.to_datetime(data['date'])

        # st.write("Data retrieved from API:")
        # st.write(data.head())

        # Convert start_date and end_date to datetime64[ns]
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filter the data based on date range
        data = data.loc[(data['date'] >= start_date) & (data['date'] <= end_date)]

        # Rename columns
        data.rename(columns={'date':'Date', '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'}, inplace=True)

        # st.write("Data after filtering:")
        # st.write(data.head())

        return data, meta_data['2. Symbol'].upper()
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None, None