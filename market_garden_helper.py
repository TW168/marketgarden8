import yfinance as yf
import streamlit as st
import pandas as pd

"""
Market Garden Helper Module

This module contains helper functions for the Market Garden application.
"""


@st.cache_data
def get_stock_data(tickers, start_date, end_date):
    """
    Fetches historical market data for given ticker symbols between specified dates.

    Parameters:
    tickers (list): A list of string ticker symbols for which to fetch data.
    start_date (str): The start date for the date range in the 'YYYY-MM-DD' format.
    end_date (str): The end date for the date range in the 'YYYY-MM-DD' format.

    Returns:
    pandas.DataFrame: A DataFrame containing the historical market data for the ticker symbols.

    Example usage
    tickers = ['AMZN']  # List of ticker symbols
    start_date = '2013-01-01'  # Start date of the date range
    end_date = '2023-07-14'  # End date of the date range
    stock_data = get_stock_data(tickers, start_date, end_date)
    """
    data = yf.download(tickers, start=start_date, end=end_date, progress=False)

    return data


@st.cache_data
def get_ticker_info(ticker):
    """
    Get information about a specific ticker from Yahoo Finance.

    Parameters:
        ticker (str): The ticker symbol of the company to get information about.

    Returns:
        dict: A dictionary containing information about the company, including income statement and balance sheet data.
    """
    ticker_info = yf.Ticker(ticker)
    info = ticker_info.info
    # income_statement = ticker_info.financials
    # balance_sheet = ticker_info.balance_sheet

    # # Add income statement and balance sheet data to the info dictionary
    # info['income_statement'] = income_statement.to_dict()
    # info['balance_sheet'] = balance_sheet.to_dict()

    return info


def format_with_commas(number):
    """
    Format a number with commas as thousand separators.

    Parameters:
        number (int or float): The number to be formatted.

    Returns:
        str: The formatted number with commas as thousand separators.
    """
    return "{:,}".format(number)


def format_with_commas_scale(number):
    """
    Format a number with commas and scale abbreviations (thousand, million, billion, etc.).

    Parameters:
        number (int or float): The number to be formatted.

    Returns:
        str: The formatted number with commas and scale abbreviations.
    """
    if not isinstance(number, (int, float)):
        return str(number)

    scales = [
        "",
        " thousand",
        " million",
        " billion",
        " trillion",
        " quadrillion",
        " quintillion",
    ]
    magnitude = 0
    while abs(number) >= 1000:
        number /= 1000.0
        magnitude += 1

    return "{:,.2f}{}".format(number, scales[magnitude])


