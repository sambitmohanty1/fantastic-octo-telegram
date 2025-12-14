
import streamlit as st
import plotly.express as px

df = st.session_state.get('portfolio_df')
st.header("Allocation: Sector/Currency & Concentration")
if df is None:
    st.warning("Upload the holdings CSV in the Home page.")
else:
    sec = df.groupby('Sector')['weight_%'].sum().reset_index().sort_values('weight_%', ascending=False)
    fig_sec = px.treemap(sec, path=['Sector'], values='weight_%', title='Sector Allocation')
    st.plotly_chart(fig_sec, use_container_width=True)
    cur = df.groupby(df['Currency'].fillna('AUD'))['weight_%'].sum().reset_index()
    fig_cur = px.pie(cur, names='Currency', values='weight_%', title='Currency Exposure')
    st.plotly_chart(fig_cur, use_container_width=True)
    top = df.sort_values('weight_%', ascending=False).head(15)
    fig_bar = px.bar(top, x='Company Name', y='weight_%', title='Top 15 Holdings (Weight %)', text='weight_%')
    fig_bar.update_layout(xaxis_tickangle=-60)
    st.plotly_chart(fig_bar, use_container_width=True)
