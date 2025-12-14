
import streamlit as st
import pandas as pd

df = st.session_state.get('portfolio_df')
st.header("Scenario Studio: Sector Shocks")
if df is None:
    st.warning("Upload the holdings CSV in the Home page.")
else:
    st.markdown("Define % shocks per sector and see portfolio impact.")
    sectors = sorted([s for s in df['Sector'].dropna().unique()])
    cols = st.columns(3)
    shocks = {}
    for i, s in enumerate(sectors):
        shocks[s] = cols[i%3].number_input(f"{s}", value=0.0, step=1.0, format="%0.1f")
    total_mv = df['Market Value $'].fillna(0).sum()
    impact = 0.0
    for sec, pct in shocks.items():
        sec_mv = df.loc[df['Sector']==sec, 'Market Value $'].sum()
        impact += sec_mv * (pct/100.0)
    st.metric("Scenario Impact ($)", f"${impact:,.0f}")
    st.metric("Scenario Impact (% of portfolio)", f"{(impact/total_mv*100 if total_mv>0 else 0):.2f}%")
