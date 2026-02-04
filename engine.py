import pandas as pd
import pandas_ta as ta
import requests

def get_market_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    # SOURCE 1: Binance
    try:
        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=100"
        res = requests.get(url, timeout=3).json()
        df = pd.DataFrame(res, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVol', 'Trades', 'TakerBuyBase', 'TakerBuyQuote', 'Ignore'])
        df['Close'] = df['Close'].astype(float)
        df['Volume'] = df['Volume'].astype(float)
        df.index = pd.to_datetime(df['Time'], unit='ms')
        if not df.empty: return df[['Close', 'Volume']]
    except: pass

    # SOURCE 2: Coinbase (Backup)
    try:
        url = "https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=60"
        res = requests.get(url, timeout=3).json()
        df = pd.DataFrame(res, columns=['Time', 'Low', 'High', 'Open', 'Close', 'Volume'])
        df['Close'] = df['Close'].astype(float)
        df['Volume'] = df['Volume'].astype(float)
        df.index = pd.to_datetime(df['Time'], unit='s')
        return df[['Close', 'Volume']].sort_index()
    except: return pd.DataFrame()

# जावेद, न्यूज़ और व्हेल पॉइंट्स (वही रहेंगे)
def get_javed_signal(df):
    if df.empty or len(df) < 22: return "SYNCING", 0, 0
    df['E9'] = ta.ema(df['Close'], 9)
    df['E21'] = ta.ema(df['Close'], 21)
    sig = "LONG (BUY)" if df['E9'].iloc[-1] > df['E21'].iloc[-1] else "SHORT (SELL)"
    return sig, round(df['E9'].iloc[-1], 2), round(df['E21'].iloc[-1], 2)
