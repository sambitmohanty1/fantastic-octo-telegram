
import os
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portfolio + Signals (Merged)", layout="wide", initial_sidebar_state="expanded")
st.title("Portfolio + Signals (Merged)")
LIC_REQUIRED = st.toggle("Require license key (for paid users)", value=False)
if LIC_REQUIRED:
    lic = st.text_input("Enter license key", value=os.getenv("APP_LICENSE_KEY", ""), type="password")
    st.session_state['license_ok'] = bool(lic.strip())
else:
    st.session_state['license_ok'] = True
st.sidebar.success("Use pages to explore Signals and Advanced Portfolio dashboards.")
uploaded = st.file_uploader("Upload holdings CSV", type=["csv"], accept_multiple_files=False)
if uploaded:
    try:
        df = pd.read_csv(uploaded)
        df.columns = [c.strip() for c in df.columns]
        num_cols = ['Quantity','Last Price','Average Cost $','Cost Value $','Market Value $','Gain Loss $','Gain Loss %','% of Holdings','Price to Earnings','Earnings per Share','Current Dividend c','Franking %','Dividend yield %','Fx Rate']
        for c in num_cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce')
        total_mv = df['Market Value $'].fillna(0).sum()
        df['weight_%'] = df['Market Value $'].fillna(0)/total_mv*100 if total_mv>0 else 0
        st.session_state['portfolio_df'] = df
        st.success("Holdings loaded. Advanced pages are ready.")
    except Exception as e:
        st.error(f"Failed to parse CSV: {e}")
st.caption("Educational use only; not financial advice.")
