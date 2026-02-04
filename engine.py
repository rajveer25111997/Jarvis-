import pandas as pd
import pandas_ta as ta
import requests
import time # टाइम जोड़ना ज़रूरी है

def get_market_data():
    # यूआरएल के अंत में टाइम जोड़ रहे हैं ताकि डेटा 1 सेकंड में ताज़ा आए
    ts = int(time.time())
    url = f"https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT&_={ts}"
    
    try:
        # सिर्फ भाव लाने के लिए सबसे तेज़ रास्ता (Ticker Price)
        res = requests.get(url, timeout=1).json()
        ltp = float(res['price'])
        
        # कैंडल डेटा (चार्ट के लिए)
        chart_url = f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=50&_={ts}"
        chart_res = requests.get(chart_url, timeout=2).json()
        df = pd.DataFrame(chart_res, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVol', 'Trades', 'TakerBuyBase', 'TakerBuyQuote', 'Ignore'])
        df['Close'] = df['Close'].astype(float)
        
        return ltp, df
    except:
        return 0.0, pd.DataFrame()
🚀 Step 2: app.py (Instant Refresh)

# जावेद, न्यूज़ और व्हेल पॉइंट्स (वही रहेंगे)
def get_javed_signal(df):
    if df.empty or len(df) < 22: return "SYNCING", 0, 0
    df['E9'] = ta.ema(df['Close'], 9)
    df['E21'] = ta.ema(df['Close'], 21)
    sig = "LONG (BUY)" if df['E9'].iloc[-1] > df['E21'].iloc[-1] else "SHORT (SELL)"
    return sig, round(df['E9'].iloc[-1], 2), round(df['E21'].iloc[-1], 2)
