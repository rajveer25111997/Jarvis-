import streamlit as st
from engine import get_market_data, get_news_impact, get_whale_radar, get_javed_signal
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=1000, key="crypto_sync")

st.title("₿ CRYPTO JARVIS COMMANDER v1.5")
st.subheader("राजवीर सर, अब हम बिटकॉइन के राजा हैं!")

df = get_market_data()

if not df.empty:
    atr, news_stat = get_news_impact(df)
    whale_active, vol = get_whale_radar(df)
    sig, e9, e21 = get_javed_signal(df)
    ltp = df['Close'].iloc[-1]
    
    # डैशबोर्ड - क्रिप्टो स्टाइल
    c1, c2, c3 = st.columns(3)
    c1.metric("BITCOIN (BTC/USDT)", f"${ltp}")
    c2.metric("VOLATILITY (ATR)", f"{atr}", delta=news_stat)
    c3.metric("JAVED SIGNAL", f"{sig}", delta=f"9EMA: {e9}")

    if whale_active:
        st.error("🚨 WHALE ALERT: क्रिप्टो की बड़ी शार्क बाज़ार में है!")
    
    if sig == "LONG (BUY)" and news_stat == "HIGH":
        st.success("🚀 CRYPTO JACKPOT: बिटकॉइन ऊपर उड़ने वाला है!")
else:
    st.info("📡 बाइनेंस (Binance) से लाइव क्रिप्टो डेटा कनेक्ट कर रहा हूँ...")
