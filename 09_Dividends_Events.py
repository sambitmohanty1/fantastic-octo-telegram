
import streamlit as st
import yfinance as yf
import pandas as pd

df = st.session_state.get('portfolio_df')
st.header("Dividend Calendar & Events (optional)")
if df is None:
    st.warning("Upload the holdings CSV in the Home page.")
else:
    tickers = list(df['Security Code'].unique())
    selected = st.multiselect("Select tickers to query", tickers, default=tickers[:10])
    rows = []
    for t in selected:
        try:
            info = yf.Ticker(t)
            cal = info.calendar
            divs = info.dividends
            rows.append({'Ticker': t, 'Calendar': str(cal) if cal is not None else '', 'Last Dividend': float(divs.iloc[-1]) if divs is not None and len(divs)>0 else None})
        except Exception as e:
            rows.append({'Ticker': t, 'Calendar': '', 'Last Dividend': None})
    st.dataframe(pd.DataFrame(rows))
