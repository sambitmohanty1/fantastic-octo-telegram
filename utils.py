
import pandas as pd
import numpy as np
from typing import Dict, Tuple

THEMES = {
    'AI/Data Center': ['NVDA:US','MU:US','AVGO:US','GOOGL:US','META:US','NXT'],
    'Cybersecurity': ['HACK'],
    'Gold': ['GOLD'],
    'Crypto Innovators': ['CRYP'],
    'Energy': ['PDN','STO'],
    'Health & Insurers': ['CSL','RMD','UNH:US','MPL'],
}

SECTOR_NORMALIZE = {
    'Information Technology': 'Technology',
    'Consumer, Non-cyclical': 'Health/Staples',
}

def load_portfolio(file) -> pd.DataFrame:
    df = pd.read_csv(file)
    df.columns = [c.strip() for c in df.columns]
    num_cols = ['Quantity','Last Price','Average Cost $','Cost Value $','Market Value $','Gain Loss $','Gain Loss %','% of Holdings','Price to Earnings','Earnings per Share','Current Dividend c','Franking %','Dividend yield %','Fx Rate']
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    total_mv = df['Market Value $'].fillna(0).sum()
    df['weight_%'] = df['Market Value $'].fillna(0) / total_mv * 100 if total_mv>0 else 0
    df['Sector'] = df['Sector'].replace(SECTOR_NORMALIZE)
    return df

def kpis(df: pd.DataFrame) -> Dict:
    total_cost = float(df['Cost Value $'].fillna(0).sum())
    total_mv = float(df['Market Value $'].fillna(0).sum())
    total_pnl = float(df['Gain Loss $'].fillna(0).sum())
    pnl_pct = (total_pnl/total_cost*100) if total_cost>0 else np.nan
    usd_weight = float(df.loc[df['Currency'].fillna('AUD')=='USD','weight_%'].sum())
    aud_weight = float(df.loc[df['Currency'].fillna('AUD')!='USD','weight_%'].sum())
    w = (df['weight_%']/100).fillna(0)
    hhi = float(np.sum(w**2))
    effective_n = (1/hhi) if hhi>0 else np.nan
    return {'total_cost': total_cost,'total_mv': total_mv,'total_pnl': total_pnl,'pnl_pct': pnl_pct,'usd_weight': usd_weight,'aud_weight': aud_weight,'hhi': hhi,'effective_n': effective_n}
