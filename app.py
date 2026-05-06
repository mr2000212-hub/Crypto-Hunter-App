import streamlit as st
import mnemonic
import requests
import time
import threading
import hashlib

# --- إعدادات التليجرام ---
TELEGRAM_TOKEN = "8710064749:AAHHVPVgKIVJBJZWm5D93wfcpGgejMB0_Ak"
CHAT_ID = "7606308687"

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, data=payload, timeout=5)
    except: pass

# --- واجهة التطبيق ---
st.set_page_config(page_title="صائد العملات MAX", page_icon="🎯")
st.title("🎯 صائد العملات الآلي - الإصدار السحابي")
st.write("المحرك يعمل الآن في الخلفية 24/7 على السيرفر.")

# استخدام Session State لحفظ العدادات
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'btc_found' not in st.session_state:
    st.session_state.btc_found = 0

col1, col2 = st.columns(2)
stat_attempts = col1.empty()
stat_found = col2.empty()

m = mnemonic.Mnemonic("english")

def start_hunting():
    while True:
        try:
            words = m.generate(strength=128)
            seed = m.to_seed(words)
            h = hashlib.sha256(seed).hexdigest()
            btc_addr = "1" + h[:33]

            # زيادة العداد
            st.session_state.attempts += 1
            
            # فحص سريع (استخدمنا API بديلة لتجنب الحظر)
            r_btc = requests.get(f"https://blockchain.info/q/addressbalance/{btc_addr}", timeout=5)
            
            if r_btc.status_code == 200 and int(r_btc.text) > 0:
                st.session_state.btc_found += 1
                send_telegram_msg(f"🎯 *صيد ثمين!*\nالرصيد: {r_btc.text}\nالكلمات: `{words}`\nالعنوان: `{btc_addr}`")
            
            # تحديث الواجهة كل 10 محاولات لتقليل الضغط
            if st.session_state.attempts % 10 == 0:
                stat_attempts.metric("إجمالي المحاولات", st.session_state.attempts)
                stat_found.metric("الكنوز المكتشفة", st.session_state.btc_found)
                
            time.sleep(0.1) 
        except:
            time.sleep(1)

# زر التشغيل
if st.button("إطلاق محرك الصيد"):
    st.success("تم تشغيل المحرك بنجاح!")
    send_telegram_msg("🚀 *تم إطلاق محرك الصيد السحابي بنجاح!*")
    start_hunting()
