
import streamlit as st
import plotly.express as px
import pandas as pd

df = st.session_state.get('portfolio_df')
st.header("Valuation Outliers: P/E vs Dividend Yield")
if df is None:
    st.warning("Upload the holdings CSV in the Home page.")
else:
    v = df.dropna(subset=['Price to Earnings']).copy()
    if len(v)==0:
        st.info("No P/E data available in the uploaded file.")
    else:
        v['PE'] = v['Price to Earnings']
        pe_mean = v['PE'].mean(); pe_std = v['PE'].std(ddof=0)
        v['PE_z'] = (v['PE']-pe_mean)/pe_std if pe_std and pe_std>0 else 0
        v['DivYld'] = v['Dividend yield %'].fillna(0)
        v['size'] = v['weight_%']
        fig = px.scatter(v, x='PE', y='DivYld', size='size', color='PE_z', hover_data=['Security Code','Sector','weight_%','Dividend yield %'], title='Valuation Map (size = weight, color = PE z-score)')
        st.plotly_chart(fig, use_container_width=True)
