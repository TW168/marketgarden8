from datetime import datetime, timedelta
import yfinance as yf
import streamlit as st

# Page config
st.set_page_config(
    page_title="Market Garden",
    layout="wide",
    menu_items={"About": "tony.wei@outlook.com"},
)


def get_10_years_ago():
    current_date = datetime.now()
    ten_years_ago = current_date - timedelta(days=365 * 10)
    return ten_years_ago


def validate_ticker(ticker):
    """
    Check if a ticker is valid by attempting to retrieve its historical data.

    Arguments:
    ticker -- a string representing the ticker symbol of a stock

    Returns:
    True if the ticker is valid and has historical data, False otherwise.
    """
    try:
        stock = yf.Ticker(ticker)
        # If the history is empty, this will also raise an error
        hist = stock.history(period="1d")
        if len(hist) == 0:
            return False
        else:
            return True
    except:
        return False


def get_history(ticker, start_date, end_date):
    """
    Retrieves the historical market data for a specific ticker within a date range.

    Arguments:
    ticker -- a string representing the ticker symbol of a stock
    start_date -- a string or datetime object representing the start date of the range
    end_date -- a string or datetime object representing the end date of the range

    Returns:
    A Pandas DataFrame containing the historical market data if successful.
    If an error occurs, returns a string containing the error message.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)
        return hist
    except Exception as e:
        return str(e)


# Streamlit Code
st.title("Market Garden")


with st.expander("Data Input", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        ticker = st.text_input("Enter Ticker:", "AAPL")
    with col2:
        start_date = st.date_input("Enter Start Date:", get_10_years_ago())
        # start_date = "2023-07-01"
    with col3:
        end_date = st.date_input("Enter End Date:", datetime.now())
        # end_date = "2023-08-02"
if st.button("Get Stock History"):
    if validate_ticker(ticker):
        with st.spinner("Fetching data..."):
            data = get_history(ticker, start_date, end_date)
        with st.expander(f"{ticker.upper()} Historical Data", expanded=True):
            data = get_history(ticker, start_date, end_date)

            if isinstance(data, str):
                st.error("An error occurred: " + data)
            else:
                st.dataframe(data, use_container_width=True)
    else:
        st.error(f"{ticker.upper()} is not valid.")
