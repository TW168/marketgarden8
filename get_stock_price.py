import pandas as pd
import streamlit as st
from helper import get_stock_data
import json
#from alpha_vantage.timeseries import TimeSeries

# Page config
st.set_page_config(
        page_title="MarketGarden",
        layout="wide",
        menu_items={"About": "tony.wei@outlook.com"},
    )

def main():
    st.title("Stock Data Viewer")
    with st.expander("Enter Ticker Symbol and Dates", expanded=True):
        # Read API key from secrets.toml file
        api_key = st.secrets["alpha_vantage_api_key"]["api_key"]
        # st.write(api_key)
        col1, col2, col3 = st.columns(3)
        with col1:
            ticker = st.text_input("Enter ticker symbol (e.g., AAPL):")
        with col2:
            start_date = st.date_input("Enter start date:")
        with col3:
            end_date = st.date_input("Enter end date:")

    if ticker and start_date and end_date:
        stock_data, meta_data = get_stock_data(api_key, ticker, start_date, end_date)
        st.write("Stock Data:")
        st.dataframe(stock_data, use_container_width=True)
        #st.write("Ticker: ", meta_data("2. Symbol").upper())
        # st.write(meta_data)


if __name__ == "__main__":
    main()
