
import streamlit as st
import pandas as pd
import plotly.express as px

df = st.session_state.get('portfolio_df')
st.header("FX Exposure & Sensitivity (USD/AUD)")
if df is None:
    st.warning("Upload the holdings CSV in the Home page.")
else:
    shocks = st.multiselect("Select shock magnitudes (%)", [2,5,10], default=[2,5,10])
    total_mv = df['Market Value $'].fillna(0).sum()
    usd_mv = df.loc[df['Currency'].fillna('AUD')=='USD','Market Value $'].fillna(0).sum()
    rows = []
    for s in shocks:
        rows += [
            {'Shock': f'+{s}%', 'Impact % of Portfolio': round((usd_mv*(s/100))/total_mv*100,2)},
            {'Shock': f'-{s}%', 'Impact % of Portfolio': round((-usd_mv*(s/100))/total_mv*100,2)}
        ]
    fxdf = pd.DataFrame(rows)
    st.dataframe(fxdf)
    fig = px.bar(fxdf, x='Shock', y='Impact % of Portfolio', color='Shock', title='FX Shock Impact (% of portfolio)')
    st.plotly_chart(fig, use_container_width=True)
