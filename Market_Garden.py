from datetime import date, timedelta
import pandas as pd
import streamlit as st
from market_garden_helper import get_ticker_info, format_with_commas, format_with_commas_scale, get_stock_data


# Page config
st.set_page_config(
        page_title="MarketGarden",
        layout="wide",
        menu_items={"About": "tony.wei@outlook.com"},
    )

def main():
# Input data container
    with st.container():
        with st.expander("Input", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                ticker = st.text_input("Ticker", "msft")
                st.write("DEBUG - Ticker:", ticker)  # Debug statement
                
            with col2:
                # Calculate one year ago
                five_year_ago = date.today() - timedelta(days=365 * 5)
                start_date = st.date_input("Start Date", five_year_ago)
            with col3:
                end_date = st.date_input("End Date")
  

    # Histoical stock price and company info container
    with st.expander(f"{ticker.upper()} Last 5 year price and Financial Data", expanded=True):
        ticker_data = get_stock_data(tickers=ticker, start_date=start_date, end_date=end_date)
        st.dataframe(ticker_data, use_container_width=True)
        ticker_info = get_ticker_info(ticker)
        st.write("Audit Risk:", ticker_info["auditRisk"])
        recommendation = ticker_info["recommendationKey"]
        st.markdown(f"Recommendation: {recommendation}", unsafe_allow_html=True)
        st.write(ticker_info)
                    

    
if __name__ == "__main__":
    main()