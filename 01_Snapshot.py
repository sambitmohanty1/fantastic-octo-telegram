
import streamlit as st
import pandas as pd
from utils import load_portfolio

st.header("Snapshot: Top Holdings & Movers")
df = st.session_state.get('portfolio_df')
if df is None:
    st.warning("Upload the holdings CSV in the Home page.")
else:
    left, right = st.columns([3,2])
    with left:
        st.subheader("Top 15 by Weight")
        st.dataframe(df.sort_values('weight_%', ascending=False).head(15)[['Company Name','Security Code','Sector','weight_%','Gain Loss $']], use_container_width=True)
    with right:
        st.subheader("Top 5 Gainers / Losers ($)")
        gainers = df.sort_values('Gain Loss $', ascending=False).head(5)[['Security Code','Company Name','Gain Loss $','Gain Loss %','weight_%']]
        losers = df.sort_values('Gain Loss $').head(5)[['Security Code','Company Name','Gain Loss $','Gain Loss %','weight_%']]
        st.dataframe(gainers)
        st.dataframe(losers)
