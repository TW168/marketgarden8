from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import yfinance as yf


# https://python-yahoofinance.readthedocs.io/en/latest/api.html#
@st.cache_data
def get_stock_data(ticker, start_date, end_date):
    """
    Get historical stock prices and company information for a specific ticker from Yahoo Finance.

    Parameters:
        ticker (str): The ticker symbol of the company to get data for.
        start_date (str): The start date for historical stock prices in the format 'YYYY-MM-DD'.
        end_date (str): The end date for historical stock prices in the format 'YYYY-MM-DD'.

    Returns:
        dict: A dictionary containing two DataFrames - 'historical_prices' and 'company_info'.
              'historical_prices': DataFrame with historical stock prices.
              'company_info': DataFrame with information about the company.
    """
    try:
        # Get historical stock prices
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        if stock_data.empty:
            raise ValueError("An error occurred while fetching historical stock prices.")

        # Get company information
        ticker_info = yf.Ticker(ticker)
        info = ticker_info.info

        # Convert non-standard types to compatible types for DataFrame
        for key, value in info.items():
            if isinstance(value, (dict, list)):
                info[key] = str(value)  # Convert dictionaries and lists to strings
            elif isinstance(value, int):
                info[key] = float(value)  # Convert int to float to handle Arrow serialization

        df_info = pd.DataFrame.from_dict(info, orient='index', columns=['Value'])
        
        # Convert the 'Value' column to strings
        df_info['Value'] = df_info['Value'].astype(str)

        return {'historical_prices': stock_data, 'company_info': df_info}
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise Exception("An exception occurred while fetching data. Please try again later.")

def get_10_years_ago():
    current_date = datetime.now()
    ten_years_ago = current_date - timedelta(days=365*10)
    return ten_years_ago

def main():
    # Get the date that was 10 years ago
    ten_years_ago = get_10_years_ago()

    with st.expander("Data Input", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            ticker = st.text_input("Enter Ticker:", "AAPL")
        with col2:
            start_date = st.date_input("Enter Start Date:", ten_years_ago)
            # start_date = "2023-07-01"
        with col3:
            end_date = st.date_input("Enter End Date:", datetime.now())
            # end_date = "2023-08-02"
    try:
        data = get_stock_data(ticker, start_date, end_date)
        historical_prices = data['historical_prices']
        company_info = data['company_info']

        st.write(f"{ticker.upper()} Historical Stock Prices:")
        st.dataframe(historical_prices)

        st.write("\nCompany Information:")
        st.write(company_info)
       
    except Exception as e:
        st.error(str(e))

if __name__ == "__main__":
    main()

