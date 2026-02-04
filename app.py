import streamlit as st
import requests
import pandas as pd
import pandas_ta as ta
from streamlit_autorefresh import st_autorefresh

# 1. रिफ्रेश इंजन
st_autorefresh(interval=1000, key="jarvis_v2_8")

st.title("🛡️ JARVIS SUPREME v2.8")

# 2. लाइव भाव (Coinbase)
def get_btc_price():
    try:
        url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
        res = requests.get(url, timeout=2).json()
        return float(res['data']['amount'])
    except: return 0.0

price_val = get_btc_price()

if price_val > 0:
    st.markdown(f"<div style='background-color:#000; padding:20px; border-radius:15px; border:3px solid #F7931A; text-align:center;'><h1 style='color:#00FF00; font-size:60px; margin:0;'>${price_val:,.2f}</h1></div>", unsafe_allow_html=True)

    # 3. सिग्नल इंजन (Error Fixed)
    try:
        c_url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=50"
        c_res = requests.get(c_url, timeout=2).json()
        
        # यहाँ हमने इंडेक्स वाला झंझट खत्म कर दिया
        df = pd.DataFrame(c_res).iloc[:, :6]
        df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        df['Close'] = df['Close'].astype(float)
        
        # EMA 9/21
        df['E9'] = ta.ema(df['Close'], length=9)
        df['E21'] = ta.ema(df['Close'], length=21)
        e9, e21 = df['E9'].iloc[-1], df['E21'].iloc[-1]
        
        sig = "🟢 CALL (BUY)" if e9 > e21 else "🔴 PUT (SELL)"
        box_color = "#00FF00" if e9 > e21 else "#FF0000"
        txt_color = "black" if e9 > e21 else "white"

        st.markdown(f"<div style='background-color:{box_color}; padding:25px; border-radius:15px; text-align:center; border: 4px solid white; margin-top:15px;'><h1 style='color:{txt_color}; margin:0; font-size:50px; font-weight:bold;'>{sig}</h1></div>", unsafe_allow_html=True)
    except Exception as e:
        st.info(f"सिग्नल अपडेट हो रहा है...")
else:
    st.info("📡 जार्विस डेटा कनेक्ट कर रहा है...")
