
# Streamlit Portfolio & Signals (Merged)

**What you get**
- Original ASX Signal Score dashboard (Signals page)
- Advanced Portfolio Intelligence pages: Concentration, FX, Scenarios, Valuation, Themes, Benchmarking, Factors, Income, Dividends & Events, Governance, Tax-Lots.
- Optional **license key gating** for paid users.

## Run locally
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## License gating (optional)
Set environment variable `APP_LICENSE_KEY` with a valid key (e.g., 'DEMO-EDU-1234'). In production, integrate a real key/stripe check.

## Notes
- Educational use only; not financial advice.
- External data (yfinance) may rate-limit; consider caching.
