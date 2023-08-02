from datetime import date, timedelta
import pandas as pd
import streamlit as st
from market_garden_helper import get_ticker_info, format_with_commas, get_stock_data

# Page config
st.set_page_config(
    page_title="MarketGarden",
    layout="wide",
    menu_items={"About": "tony.wei@outlook.com"},
)


# Input data container
with st.container():
    with st.expander("Input", expanded=True):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            ticker = st.text_input("Ticker", "GOOG")
            cap_ticker = ticker.upper()
        with col2:
            # Calculate one year ago
            five_year_ago = date.today() - timedelta(days=365 * 5)
            start_date = st.date_input("Start Date", five_year_ago)
        with col3:
            end_date = st.date_input("End Date")


# Histoical stock price and company info container
with st.container():
    with st.expander(
        f"{cap_ticker} Last 5 year price and Financial Data", expanded=False
    ):
        ticker_data = get_stock_data(ticker, start_date, end_date)
        st.dataframe(ticker_data, use_container_width=True)
        ticker_info = get_ticker_info(ticker)
        st.write("Name:", ticker_info.get("longName", "N/A"))
        st.write("Industry:", ticker_info.get("industry", "N/A"))
        st.write("Sector:", ticker_info.get("sector", "N/A"))
        st.write("Website:", ticker_info.get("website", "N/A"))

        st.write("Financial Information:")
        st.write("Market Cap:", format_with_commas(ticker_info.get("marketCap", "N/A")))
        st.write(
            "Price to Earnings (Trailing 12 Months):",
            ticker_info.get("trailingPE", "N/A"),
        )
        st.write("Dividend Yield:", ticker_info.get("dividendYield", "N/A"))
