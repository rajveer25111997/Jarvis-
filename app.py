import streamlit as st
from engine import get_market_data, get_javed_signal
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=1000, key="btc_fix")

st.title("₿ CRYPTO JARVIS v1.7 (FIXED)")

df = get_market_data()

if not df.empty:
    ltp = df['Close'].iloc[-1]
    sig, e9, e21 = get_javed_signal(df)
    
    # बड़ा डिस्प्ले ताकि भाव साफ़ दिखे
    st.markdown(f"""
        <div style="background-color:#1e1e1e; padding:20px; border-radius:15px; border:2px solid #F7931A; text-align:center;">
            <h2 style="color:#F7931A; margin:0;">BITCOIN LIVE PRICE</h2>
            <h1 style="color:white; font-size:50px; margin:10px;">${round(ltp, 2)}</h1>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.metric("SIGNAL", sig)
    c2.metric("EMA 9/21", f"{e9} / {e21}")
else:
    st.error("📡 डेटा सिंक नहीं हो रहा! इंटरनेट चेक करें या 'Reboot' दबाएँ।")

if st.button("🔄 FORCE REFRESH"):
    st.rerun()
