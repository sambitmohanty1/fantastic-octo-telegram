
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

df = st.session_state.get('portfolio_df')
st.header("Benchmarking: Active Share & Tracking Error")
if df is None:
    st.warning("Upload the holdings CSV in the Home page.")
else:
    bench_symbols = st.text_input("Benchmark components (symbol:weight%)", value="VAS:40,VGS:40,IVV:20")
    parts = [p.strip() for p in bench_symbols.split(',') if p.strip()]
    bench = {}
    for p in parts:
        try:
            sym, w = p.split(':'); bench[sym.strip()] = float(w)
        except: pass
    pw = df.groupby('Security Code')['weight_%'].sum()
    bw = pd.Series(bench)
    idx = set(pw.index).union(set(bw.index))
    ascore = 0.5*np.sum(np.abs(pw.reindex(idx).fillna(0)/100.0 - bw.reindex(idx).fillna(0)/100.0))
    st.metric("Active Share", f"{ascore*100:.2f}%")
    use_yf = st.toggle("Fetch price history via yfinance", value=False)
    if use_yf:
        try:
            tickers = list(pw.index)
            data = yf.download(tickers, period='6mo', interval='1d', group_by='ticker', auto_adjust=True, progress=False)
            rets = []
            for t in tickers:
                s = data[t]['Close'].pct_change().dropna(); rets.append(s.rename(t))
            ret_df = pd.concat(rets, axis=1).dropna()
            w = pw.reindex(ret_df.columns).fillna(0)/100.0
            port_ret = (ret_df * w.values).sum(axis=1)
            bdata = yf.download(list(bench.keys()), period='6mo', interval='1d', auto_adjust=True, progress=False)
            brets = []
            for t in bench.keys():
                s = bdata[t]['Close'].pct_change().dropna(); brets.append(s.rename(t))
            bret_df = pd.concat(brets, axis=1).dropna()
            bw_series = pd.Series(bench); bw_norm = bw_series/bw_series.sum()
            bench_ret = (bret_df * bw_norm.values).sum(axis=1)
            active = (port_ret - bench_ret).dropna()
            te = np.std(active)*np.sqrt(252)
            st.metric("Tracking Error (annualised)", f"{te:.2%}")
            st.line_chart(pd.DataFrame({'Portfolio':port_ret, 'Benchmark':bench_ret}).cumsum())
        except Exception as e:
            st.error(f"Price fetch failed: {e}")
