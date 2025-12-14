
import streamlit as st
import pandas as pd

st.header("Tax-Lot Smart Rebalance (illustrative)")
lot_file = st.file_uploader("Upload tax lots CSV", type=['csv'])
df = st.session_state.get('portfolio_df')
if df is None:
    st.warning("Upload the holdings CSV in the Home page.")
elif lot_file is None:
    st.info("Provide tax lots to run optimisation. Columns: Security Code, Lot Date, Quantity, CostPerShare")
else:
    lots = pd.read_csv(lot_file)
    lots['LastPrice'] = lots['Security Code'].map(df.set_index('Security Code')['Last Price'])
    lots['GainPerShare'] = lots['LastPrice'] - lots['CostPerShare']
    st.dataframe(lots.sort_values('GainPerShare').head(20))
