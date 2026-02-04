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
# --- Point B: Whale Radar (Operator Entry) ---
def get_whale_radar(df):
    """
    यह फंक्शन वॉल्यूम के ज़रिए बड़े खिलाड़ियों की एंट्री पकड़ता है।
    """
    if df.empty or 'Volume' not in df.columns:
        return False, 0.0
    
    # पिछली 15 कैंडल्स का औसत वॉल्यूम
    avg_vol = df['Volume'].tail(15).mean()
    current_vol = df['Volume'].iloc[-1]
    
    # अगर अभी का वॉल्यूम औसत से 1.5 गुना ज़्यादा है, तो व्हेल की एंट्री है
    is_whale = current_vol > (avg_vol * 1.5)
    
    return is_whale, round(current_vol, 0)
