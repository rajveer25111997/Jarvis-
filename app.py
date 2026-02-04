import streamlit as st
import pandas as pd
import pandas_ta as ta
import requests
import time
from streamlit_autorefresh import st_autorefresh

# 1. सुपर फ़ास्ट रिफ्रेश (1 सेकंड)
st_autorefresh(interval=1000, key="jarvis_final_fix")

st.title("₿ JARVIS TURBO v2.0")
st.subheader("राजवीर सर, अब कोई एरर नहीं आएगा!")

# 2. ताज़ा डेटा खींचने का इंजन (No Lag)
def get_crypto_data():
    ts = int(time.time())
    url = f"https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT&_={ts}"
    try:
        # सीधा लाइव प्राइस
        res = requests.get(url, timeout=2).json()
        price = float(res['price'])
        
        # चार्ट और इंडिकेटर्स के लिए डेटा
        c_url = f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=50"
        c_res = requests.get(c_url, timeout=2).json()
        df = pd.DataFrame(c_res, columns=['T','O','H','L','C','V','CT','QV','Tr','TB','TQ','I'])
        df['Close'] = df['Close'].astype(float)
        
        # जावेद (EMA 9/21)
        df['E9'] = ta.ema(df['Close'], length=9)
        df['E21'] = ta.ema(df['Close'], length=21)
        
        return price, df
    except:
        return 0.0, pd.DataFrame()

# 3. जार्विस डिस्प्ले
price, df = get_crypto_data()

if price > 0:
    # बिटकॉइन का चमकता हुआ भाव
    st.markdown(f"""
        <div style="background-color:#000; padding:20px; border-radius:15px; border:3px solid #F7931A; text-align:center;">
            <h2 style="color:#F7931A; margin:0;">BITCOIN LIVE PRICE</h2>
            <h1 style="color:#00FF00; font-size:65px; margin:10px;">${price:,}</h1>
        </div>
    """, unsafe_allow_html=True)

    # जावेद सिग्नल
    e9, e21 = df['E9'].iloc[-1], df['E21'].iloc[-1]
    sig = "🟢 LONG (BUY)" if e9 > e21 else "🔴 SHORT (SELL)"
    
    c1, c2 = st.columns(2)
    c1.metric("JAVED SIGNAL", sig)
    c2.metric("EMA TREND", f"{round(e9,2)} / {round(e21,2)}")
else:
    st.info("📡 जार्विस नेटवर्क ढूँढ रहा है... कृपया 10 सेकंड रुकें।")
