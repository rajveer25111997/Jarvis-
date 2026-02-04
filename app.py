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
# app.py में Point A और Point B का संगम
import streamlit as st
from engine import get_market_data, get_news_impact, get_whale_radar # नया इंपोर्ट

st.title("🏛️ JARVIS SUPREME v1.2")

df = get_market_data()

if not df.empty:
    atr_val, news_stat = get_news_impact(df)
    whale_active, vol_val = get_whale_radar(df) # व्हेल रडार कॉल किया
    
    c1, c2, c3 = st.columns(3)
    c1.metric("NIFTY LIVE", f"₹{df['Close'].iloc[-1]}")
    c2.metric("NEWS FLOW (ATR)", f"{atr_val}", delta=news_stat)
    
    # व्हेल रडार का डिस्प्ले
    whale_msg = "🚨 WHALE DETECTED!" if whale_active else "🐟 SMALL TRADERS"
    c3.metric("WHALE RADAR", f"{vol_val}", delta=whale_msg)
    
    if whale_active and news_stat == "HIGH":
        st.error("🔥 जैकपॉट अलर्ट: न्यूज़ और ऑपरेटर्स दोनों एक साथ बाज़ार में हैं!")
        # यहाँ हम आवाज़ भी जोड़ सकते हैं
else:
    st.info("📡 जार्विस व्हेल और न्यूज़ को सिंक कर रहा है...")
