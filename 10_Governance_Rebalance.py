
import streamlit as st
import numpy as np

df = st.session_state.get('portfolio_df')
st.header("Governance: Efficiency & Rebalance Radar")
if df is None:
    st.warning("Upload the holdings CSV in the Home page.")
else:
    thr_over = st.slider("Overweight threshold (%)", 5.0, 15.0, 8.0, 0.5)
    thr_under = st.slider("Underperform threshold (%)", -50.0, 0.0, -15.0, 0.5)
    r = df[['Company Name','Security Code','Sector','weight_%','Gain Loss %','Gain Loss $']].copy()
    r['Overweight Flag'] = np.where(r['weight_%']>thr_over, 'Overweight', 'OK')
    r['Underperform Flag'] = np.where(r['Gain Loss %']<thr_under, 'Underperform', 'OK')
    r['Contribution per 1% weight $'] = np.where(r['weight_%']>0, r['Gain Loss $']/r['weight_%'], np.nan)
    st.dataframe(r.sort_values('Contribution per 1% weight $', ascending=False))
