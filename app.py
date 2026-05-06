import streamlit as st
import mnemonic
import requests
import hashlib
import time

# إعدادات تليجرام الخاصة بك
TOKEN = "8710064749:AAHHVPVgKIVJBJZWm5D93wfcpGgejMB0_Ak"
ID = "7606308687"

def send_msg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={"chat_id": ID, "text": text, "parse_mode": "Markdown"})
    except: pass

st.set_page_config(page_title="MAX Hunter Pro", page_icon="🎯")
st.title("🎯 صائد ومحلل MAX المطور")
st.write("النسخة السحابية المستقرة المرتبطة بتليجرام")

if 'count' not in st.session_state: st.session_state.count = 0
placeholder = st.empty()
m = mnemonic.Mnemonic("english")

if st.button("🚀 تشغيل المحرك المطور"):
    st.success("تم الربط بنجاح.. تابع النتائج على تليجرام")
    send_msg("🚀 *تم تشغيل النسخة المطورة بنجاح!*")
    
    while True:
        words = m.generate(strength=128)
        seed = m.to_seed(words)
        addr = "1" + hashlib.sha256(seed).hexdigest()[:33]
        
        st.session_state.count += 1
        placeholder.metric("إجمالي المحافظ المفحوصة", st.session_state.count)
        
        try:
            # فحص الرصيد عبر API موثوق
            res = requests.get(f"https://blockchain.info/q/addressbalance/{addr}", timeout=5)
            if res.status_code == 200 and int(res.text) > 0:
                result = f"🎯 *صيد ثمين!*\nالرصيد: {res.text}\nالكلمات: `{words}`\nالعنوان: `{addr}`"
                send_msg(result)
        except: pass
        time.sleep(0.05) # سرعة عالية ومستقرة

