
import streamlit as st
import pandas as pd
import numpy as np

df = st.session_state.get('portfolio_df')
st.header("Factor Tilt Radar (proxy)")
if df is None:
    st.warning("Upload the holdings CSV in the Home page.")
else:
    x = df.copy()
    x['val_score'] = (x['Dividend yield %'].fillna(0))/100 + (1/(x['Price to Earnings'].replace(0,np.nan))).fillna(0)
    x['quality_score'] = np.where(x['Earnings per Share'].fillna(0)>0,1,0)
    x['momentum_score'] = (x['Last Price'] - x['Average Cost $']).fillna(0)
    x['growth_score'] = np.where((x['Price to Earnings']>40) & (x['Dividend yield %'].fillna(0)<1),1,0)
    w = x['weight_%'].fillna(0)/100.0
    scores = {
        'Value': float((x['val_score']*w).sum()),
        'Quality': float((x['quality_score']*w).sum()),
        'Momentum': float((x['momentum_score']*w).sum()),
        'Growth': float((x['growth_score']*w).sum()),
    }
    st.bar_chart(pd.Series(scores))
    st.dataframe(x[['Security Code','Company Name','val_score','quality_score','momentum_score','growth_score','weight_%']])
