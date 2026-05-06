import streamlit as st
import mnemonic
import requests
import hashlib
import time

# إعدادات تليجرام
TOKEN = "8710064749:AAHHVPVgKIVJBJZWm5D93wfcpGgejMB0_Ak"
ID = "7606308687"

def send_msg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={"chat_id": ID, "text": text, "parse_mode": "Markdown"})
    except: pass

st.title("🎯 صائد العملات MAX")
placeholder = st.empty()
m = mnemonic.Mnemonic("english")

if 'count' not in st.session_state: st.session_state.count = 0

if st.button("🚀 إطلاق محرك الصيد"):
    st.success("بدأ العمل.. تابع تليجرام!")
    send_msg("🔌 *المحرك بدأ الصيد الآن!*")
    while True:
        words = m.generate(strength=128)
        seed = m.to_seed(words)
        addr = "1" + hashlib.sha256(seed).hexdigest()[:33]
        st.session_state.count += 1
        placeholder.metric("محافظ مفحوصة", st.session_state.count)
        try:
            res = requests.get(f"https://blockchain.info/q/addressbalance/{addr}", timeout=2)
            if res.status_code == 200 and int(res.text) > 0:
                send_msg(f"🎯 *صيد ثمين!*\nالرصيد: {res.text}\nالكلمات: `{words}`")
        except: pass
        time.sleep(0.1)
