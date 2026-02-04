import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# 1. सुपर फ़ास्ट रिफ्रेश (1 सेकंड)
st_autorefresh(interval=1000, key="jarvis_final_fix")
# --- 🔊 जार्विस वॉइस इंजन (टुकड़ा #1) ---
def speak(text):
    if text:
        js = f"<script>window.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{text}'); m.lang='hi-IN'; window.speechSynthesis.speak(m);</script>"
        st.components.v1.html(js, height=0)
st.title("₿ JARVIS TURBO v2.5")
st.subheader("राजवीर सर, अब भाव और आवाज़ दोनों काम करेंगे!")

# 2. ताज़ा डेटा खींचने का सबसे हल्का इंजन
def get_btc_price():
    try:
        # सीधा कॉइनबेस से भाव उठाना (सबसे तेज़)
        url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
        res = requests.get(url, timeout=2).json()
        return float(res['data']['amount'])
    except:
        return 0.0

# 3. जार्विस डिस्प्ले लॉजिक
price_val = get_btc_price()

if price_val > 0:
    # बिटकॉइन का चमकता हुआ भाव
    st.markdown(f"""
        <div style="background-color:#000; padding:20px; border-radius:15px; border:3px solid #F7931A; text-align:center;">
            <h2 style="color:#F7931A; margin:0;">BITCOIN LIVE PRICE</h2>
            <h1 style="color:#00FF00; font-size:65px; margin:10px;">${price_val:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

    # पोर्टफोलियो अलर्ट (एक छोटा सा लॉजिक)
    if price_val > 97000:
        st.success("🚀 बिटकॉइन आसमान छू रहा है!")
else:
    st.info("📡 जार्विस भाव ढूँढ रहा है... कृपया 5 सेकंड रुकें।")

# 4. फोर्स रीबूट बटन
if st.button("🔄 REBOOT JARVIS"):
    st.rerun()
