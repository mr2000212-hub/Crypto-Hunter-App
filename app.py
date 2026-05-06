import streamlit as st
import google.generativeai as genai

# إعداد واجهة تطبيق صائد العملات
st.set_page_config(page_title="Crypto Hunter MAX", page_icon="💰")

# مفاتيح التشغيل
GEMINI_KEY = "AIzaSyCdwMonB0QOgpoIbunpVGWvZ32ixbo-HkI"
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("💰 صائد ومحلل العملات - MAX")

menu = st.sidebar.selectbox("اختر المهمة:", ["تحليل عملة", "تتبع محفظة"])

if menu == "تحليل عملة":
    coin = st.text_input("أدخل رمز العملة (مثلاً BTC أو SOL):")
    if st.button("بدء التحليل"):
        with st.spinner("جاري التحليل الفني..."):
            res = model.generate_content(f"أعطني تحليلاً لمستقبل عملة {coin} لعام 2026")
            st.success("النتيجة:")
            st.write(res.text)

elif menu == "تتبع محفظة":
    wallet = st.text_input("عنوان المحفظة:")
    st.info(f"المحفظة {wallet} قيد المراقبة الآن.")
