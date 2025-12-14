
import streamlit as st
import pandas as pd

df = st.session_state.get('portfolio_df')
st.header("Income Ladder & Franking")
if df is None:
    st.warning("Upload the holdings CSV in the Home page.")
else:
    x = df.copy()
    x['Dividend Cash $'] = (pd.to_numeric(x['Current Dividend c'], errors='coerce').fillna(0)/100.0) * x['Quantity'].fillna(0)
    x = x[x['Dividend Cash $']>0][['Company Name','Security Code','Dividend Cash $','Franking %']].sort_values('Dividend Cash $', ascending=False)
    if len(x)==0:
        st.info("No current dividend data in file or zero dividends.")
    else:
        st.bar_chart(x.set_index('Security Code')['Dividend Cash $'])
        st.dataframe(x)
