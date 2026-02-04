import streamlit as st
from engine import get_market_data, get_news_impact
from streamlit_autorefresh import st_autorefresh

# 1 सेकंड का रिफ्रेश (No-Blink Point)
st_autorefresh(interval=1000, key="jarvis_sync")

st.title("🏛️ JARVIS SUPREME v1.0")

df = get_market_data()

if not df.empty:
    atr_val, news_stat = get_news_impact(df)
    
    col1, col2 = st.columns(2)
    col1.metric("NIFTY LIVE", f"₹{df['Close'].iloc[-1]}")
    col2.metric("NEWS FLOW (ATR)", f"{atr_val}", delta=news_stat)
    
    if news_stat == "HIGH":
        st.warning("🚨 ALERT: न्यूज़ की वजह से हलचल तेज़ है!")
else:
    st.info("📡 जार्विस डेटा सिंक कर रहा है...")
