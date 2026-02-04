import streamlit as st
from engine import get_market_data
from streamlit_autorefresh import st_autorefresh

# 1000ms यानी ठीक 1 सेकंड में रिफ्रेश
st_autorefresh(interval=1000, key="turbo_refresh")

st.title("₿ JARVIS TURBO v1.8")

# इंजन से ताज़ा भाव लाना
ltp, df = get_market_data()

if ltp > 0:
    st.markdown(f"""
        <div style="background-color:#000; padding:20px; border-radius:15px; border:3px solid #F7931A; text-align:center;">
            <h2 style="color:#F7931A; margin:0;">BITCOIN INSTANT PRICE</h2>
            <h1 style="color:#00FF00; font-size:70px; margin:10px;">${ltp:,}</h1>
            <p style="color:gray;">Last Sync: {st.session_state.get('last_time', 'Just Now')}</p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.warning("📡 डेटा सिंक हो रहा है... रुकिए")
