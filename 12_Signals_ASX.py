
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

st.header("ASX Stock Signal Score Dashboard")
if 'license_ok' in st.session_state and not st.session_state['license_ok']:
    st.warning('License required for this page. Please enter a valid key on Home.')
    st.stop()

def calculate_signal_score(current_price, sma_200, cape_ratio, analyst_upside):
    sma_score = max(0, 100 - abs(current_price - (sma_200 if sma_200 else current_price)) / (sma_200 if sma_200 else current_price) * 100)
    cape_score = max(0, 100 - (cape_ratio if cape_ratio else 25.0) * 2)
    upside_score = min(100, analyst_upside if analyst_upside is not None else 0)
    return round((sma_score * 0.4 + cape_score * 0.3 + upside_score * 0.3), 2)

ticker_input = st.text_input("Enter ASX Stock Ticker Symbol (e.g., WTC.AX, NXT.AX)", "WTC.AX")
if ticker_input:
    try:
        ticker = yf.Ticker(ticker_input)
        hist = ticker.history(period="6mo")
        info = ticker.info
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        st.stop()
    if hist is not None and not hist.empty:
        hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
        hist['SMA_100'] = hist['Close'].rolling(window=100).mean()
        hist['SMA_200'] = hist['Close'].rolling(window=200).mean()
        current_price = float(hist['Close'].iloc[-1])
        sma_50 = float(hist['SMA_50'].iloc[-1]) if pd.notna(hist['SMA_50'].iloc[-1]) else None
        sma_100 = float(hist['SMA_100'].iloc[-1]) if pd.notna(hist['SMA_100'].iloc[-1]) else None
        sma_200 = float(hist['SMA_200'].iloc[-1]) if pd.notna(hist['SMA_200'].iloc[-1]) else None
        cape_ratio = info.get('trailingPE', 25.0)
        target_price = info.get('targetMeanPrice', current_price)
        analyst_upside = max(0, (target_price - current_price) / current_price * 100) if current_price else 0
        signal_score = calculate_signal_score(current_price, sma_200, cape_ratio, analyst_upside)
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Current Price", f"${current_price:.2f}")
        c2.metric("SMA 50", f"${sma_50:.2f}" if sma_50 else "NA")
        c3.metric("SMA 100", f"${sma_100:.2f}" if sma_100 else "NA")
        c4.metric("SMA 200", f"${sma_200:.2f}" if sma_200 else "NA")
        c5.metric("PE (proxy)", f"{cape_ratio:.2f}")
        c6.metric("Analyst Upside", f"{analyst_upside:.2f}%")
        st.metric("Signal Score", f"{signal_score}/100")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Close'))
        if hist['SMA_50'].notna().any():
            fig.add_trace(go.Scatter(x=hist.index, y=hist['SMA_50'], mode='lines', name='SMA 50'))
        if hist['SMA_100'].notna().any():
            fig.add_trace(go.Scatter(x=hist.index, y=hist['SMA_100'], mode='lines', name='SMA 100'))
        if hist['SMA_200'].notna().any():
            fig.add_trace(go.Scatter(x=hist.index, y=hist['SMA_200'], mode='lines', name='SMA 200'))
        fig.update_layout(title=f"{ticker_input.upper()} Price & SMA", xaxis_title="Date", yaxis_title="Price (AUD)", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        if sma_200 and current_price <= sma_200 * 1.05:
            st.success("✅ Near 200-day SMA — potential entry area (educational)")
        elif signal_score > 70:
            st.info("📈 Strong signal score — consider deeper analysis (educational)")
        else:
            st.warning("⚠️ Moderate score — review fundamentals & technicals (educational)")
    else:
        st.error("No historical data found for this ticker.")
