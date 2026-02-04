import streamlit as st
import requests
import pandas as pd
import pandas_ta as ta
import time
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
# --- 🧠 जार्विस सिग्नल इंजन (इसे price_val के नीचे पेस्ट करें) ---
try:
    # 1. डेटा लाना (इंडिकेटर्स के लिए)
    c_url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=50"
    c_res = requests.get(c_url, timeout=2).json()ो
    df = pd.DataFrame(c_res)
    df = df.iloc[:, [0, 1, 2, 3, 4, 5]] # सिर्फ ज़रूरी कॉलम चुनना
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df['Close'] = df['Close'].astype(float)
    
    # 2. जावेद (EMA 9/21) कैलकुलेट करना
    df['E9'] = ta.ema(df['Close'], length=9)
    df['E21'] = ta.ema(df['Close'], length=21)
    e9, e21 = df['E9'].iloc[-1], df['E21'].iloc[-1]
    
    # 3. सिग्नल और बॉक्स का रंग तय करना
    if e9 > e21:
        sig_text = "🟢 CALL (BUY)"
        box_color = "#00FF00"  # हरा
        font_color = "black"
    else:
        sig_text = "🔴 PUT (SELL)"
        box_color = "#FF0000"  # लाल
        font_color = "white"

    # 4. स्क्रीन पर बॉक्स दिखाना
    st.markdown(f"""
        <div style="background-color:{box_color}; padding:30px; border-radius:15px; text-align:center; border: 5px solid white; margin-top:15px;">
            <h1 style="color:{font_color}; margin:0; font-size:55px; font-weight:bold;">{sig_text}</h1>
            <p style="color:{font_color}; font-size:20px;">EMA 9: {round(e9,2)} | EMA 21: {round(e21,2)}</p>
        </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"सिग्नल इंजन में एरर: {e}")

if price_val > 0:
    # बिटकॉइन का चमकता हुआ भाव
    st.markdown(f"""
        <div style="background-color:#000; padding:20px; border-radius:15px; border:3px solid #F7931A; text-align:center;">
            <h2 style="color:#F7931A; margin:0;">BITCOIN LIVE PRICE</h2>
            <h1 style="color:#00FF00; font-size:65px; margin:10px;">${price_val:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

    # --- 🧠 जार्विस का दिमाग (टुकड़ा: सिग्नल बॉक्स) ---
    # चूँकि अभी हम डेटा चार्ट नहीं खींच रहे, हम एक 'प्राइस अलर्ट' बॉक्स जोड़ते हैं
    
    if price_val > 96500: # आप इस लेवल को अपने हिसाब से बदल सकते हैं
        sig = "🟢 CALL (BUY)"
        bg_color = "#00FF00"
        txt_color = "black"
        speak("राजवीर सर, बाज़ार ऊपर है, कॉल साइड देखें")
    else:
        sig = "🔴 PUT (SELL)"
        bg_color = "#FF0000"
        txt_color = "white"
        speak("राजवीर सर, बाज़ार नीचे है, पुट साइड देखें")

    # सिग्नल बॉक्स का डिस्प्ले
    st.markdown(f"""
        <div style="background-color:{bg_color}; padding:20px; border-radius:15px; text-align:center; border: 4px solid white; margin-top:10px;">
            <h1 style="color:{txt_color}; margin:0; font-size:40px;">{sig}</h1>
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
