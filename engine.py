import pandas as pd
import pandas_ta as ta
import requests

# पॉइंट: डेटा बैकअप (Point 1)
def get_market_data():
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/^NSEI?interval=1m&range=1d"
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5).json()
        p = res['chart']['result'][0]['indicators']['quote'][0]['close']
        t = res['chart']['result'][0]['timestamp']
        return pd.DataFrame({'Close': p}, index=pd.to_datetime(t, unit='s')).dropna()
    except:
        return pd.DataFrame()

# पॉइंट 'A': न्यूज़ इम्पैक्ट (ATR Logic)
def get_news_impact(df):
    if df.empty or len(df) < 15: return 0.0, "WAITING"
    df['ATR'] = ta.atr(df['Close'], df['Close'], df['Close'], length=14)
    val = round(df['ATR'].iloc[-1], 2)
    status = "HIGH" if val > 5.0 else "NORMAL"
    return val, status
