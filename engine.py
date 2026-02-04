import pandas as pd
import pandas_ta as ta
import requests

# --- क्रिप्टो डेटा इंजन (Binance API) ---
def get_market_data():
    try:
        # बिटकॉइन (BTC/USDT) का 1 मिनट का डेटा
        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=100"
        res = requests.get(url, timeout=5).json()
        df = pd.DataFrame(res, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVol', 'Trades', 'TakerBuyBase', 'TakerBuyQuote', 'Ignore'])
        
        df['Close'] = df['Close'].astype(float)
        df['Volume'] = df['Volume'].astype(float)
        df.index = pd.to_datetime(df['Time'], unit='ms')
        return df[['Close', 'Volume']]
    except:
        return pd.DataFrame()

# --- न्यूज़ इम्पैक्ट (ATR) ---
def get_news_impact(df):
    if df.empty or len(df) < 15: return 0.0, "WAITING"
    df['ATR'] = ta.atr(df['Close'], df['Close'], df['Close'], length=14)
    val = round(df['ATR'].iloc[-1], 2)
    return val, ("HIGH" if val > 15.0 else "NORMAL")

# --- व्हेल रडार ---
def get_whale_radar(df):
    if df.empty: return False, 0.0
    avg_vol = df['Volume'].tail(15).mean()
    current_vol = df['Volume'].iloc[-1]
    return (current_vol > avg_vol * 1.5), round(current_vol, 2)

# --- जावेद (EMA 9/21) ---
def get_javed_signal(df):
    if df.empty or len(df) < 22: return "WAITING", 0, 0
    df['E9'] = ta.ema(df['Close'], length=9)
    df['E21'] = ta.ema(df['Close'], length=21)
    e9, e21 = df['E9'].iloc[-1], df['E21'].iloc[-1]
    sig = "LONG (BUY)" if e9 > e21 else "SHORT (SELL)"
    return sig, round(e9, 2), round(e21, 2)
