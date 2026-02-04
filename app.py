import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# 1. 1-सेकंड का हार्ड रिफ्रेश
st_autorefresh(interval=1000, key="jarvis_fix_v2")

st.title("₿ JARVIS CRYPTO v2.1")
st.write(f"Last Sync: {datetime.now().strftime('%H:%M:%S')}")

# 2. सुपर-फास्ट डेटा इंजन (Yahoo Finance)
def get_live_data():
    try:
        # सीधा बिटकॉइन का डेटा खींचना
        data = yf.download(tickers='BTC-USD', period='1d', interval='1m', progress=False)
        if not data.empty:
            # लेटेस्ट भाव
            price = data['Close'].iloc[-1]
            # जावेद (EMA 9/21)
            data['E9'] = ta.ema(data['Close'], length=9)
            data['E21'] = ta.ema(data['Close'], length=21)
            return price, data
        return 0.0, pd.DataFrame()
    except:
        return 0.0, pd.DataFrame()

# 3. जार्विस डिस्प्ले लॉजिक
price, df = get_live_data()

if price > 0:
    # बिटकॉइन का बड़ा और चमकता हुआ भाव
    st.markdown(f"""
        <div style="background-color:#111; padding:20px; border-radius:15px; border:2px solid #00FF00; text-align:center;">
            <h2 style="color:#00FF00; margin:0;">BITCOIN LIVE (USD)</h2>
            <h1 style="color:white; font-size:60px; margin:10px;">${price:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

    # जावेद सिग्नल चेक
    e9 = df['E9'].iloc[-1]
    e21 = df['E21'].iloc[-1]
    
    sig = "🟢 BUY CALL" if e9 > e21 else "🔴 BUY PUT"
    
    col1, col2 = st.columns(2)
    col1.metric("JAVED SIGNAL", sig)
    col2.metric("9/21 EMA GAP", f"{round(e9-e21, 2)}")

    if abs(e9-e21) > 50:
        st.success("🚀 बड़ा मूव आने वाला है, तैयार रहें!")
else:
    st.warning("📡 जार्विस डेटा खींचने की कोशिश कर रहा है... अगर यह 30 सेकंड से ज़्यादा ले, तो 'Reboot' दबाएँ।")

if st.button("🔄 FORCE RESET"):
    st.rerun()
