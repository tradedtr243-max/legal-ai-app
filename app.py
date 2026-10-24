import streamlit as st
import google.generativeai as genai
import pypdf
import time

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="المحلل القانوني الذكي | LegalAI Pro",
    page_icon="⚖️",
    layout="wide"
)

# --- تنسيق CSS مخصص للواجهة ---
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    .risk-box { padding: 15px; border-radius: 10px; margin-bottom: 15px; }
    .pay-card { background-color: #1e222d; padding: 20px; border-radius: 12px; border: 1px solid #f0b90b; }
</style>
""", unsafe_allow_html=True)

# --- الشريط الجانبي: الضبط ومفتاح API ---
st.sidebar.title("⚙️ الإعدادات")
api_key = st.sidebar.text_input("أدخل مفتاح Google Gemini API:", type="password")

st.sidebar.markdown("---")
st.sidebar.info("💡 **طريقة العمل:** رفع العقد 👈 اختيار الخدمة 👈 إتمام الدفع بـ Binance Pay 👈 عرض التحليل الفوري.")

# --- عنوان التطبيق الرئيسي ---
st.title("⚖️ المحلل القانوني الذكي (LegalAI Pro)")
st.caption("أداة تحليل العقود والمستندات الذكية: كشف الثغرات، حساب المخاطر، واستراتيجيات التفاوض")

# --- محفظة باينانس الخاصة بك لاستلام الأموال ---
BINANCE_PAY_ID = "YOUR_BINANCE_ID_HERE"  # استبدل هذا بـ Binance ID أو عنوان محفظتك
PRICE_USDT = 1.00  # سعر التحليل 1 دولار

# --- قسم رفع الملفات ---
uploaded_file = st.file_uploader("📄 قم برفع العقد أو المستند (صيغة PDF)", type=["pdf"])

if uploaded_file is not None:
    # قراءة النص من الـ PDF
    pdf_reader = pypdf.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    st.success(f"✅ تم تحميل المستند بنجاح! (عدد الصفحات: {len(pdf_reader.pages)})")

    # اختيار الخدمة المطلوب إجراؤها
    st.subheader("🎯 اختر نوع التحليل المطلوب:")
    service_option = st.radio(
        "",
        [
            "🚨 كشف المخاطر والبنود الفخ (Risk Score & Trap Detector)",
            "📊 التلخيص الشامل ومؤشر أمان العقد",
            "💡 محاكي الأسئلة الصعبة ورسالة التفاوض جاهزة"
        ]
    )

    st.markdown("---")

    # --- بوابـة الدفـع عبر باينانس (Paywall) ---
    st.subheader("💳 إتمام عملية الدفع للحصول على التقرير")
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"""
        <div class="pay-card">
            <h3 style="color:#f0b90b;">🟡 Binance Pay</h3>
            <p>سعر التحليل الفوري: <b>{PRICE_USDT} USDT</b></p>
            <p><b>رقم Pay ID للحساب:</b> <code>{BINANCE_PAY_ID}</code></p>
            <hr>
            <small>قم بتحويل المبلغ عبر تطبيق باينانس ثم ضع رقم العملية (TxID) في الحقل المقابل لتفعيل التقرير.</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        tx_id = st.text_input("🔑 أدخل رقم المعاملة (TxID / Order ID) للتأكيد:")
        confirm_pay = st.button("🚀 تأكيد الدفع واستخراج التقرير")

    # --- معالجة الطلب والتحليل عند الدفع ---
    if confirm_pay:
        if not api_key:
            st.error("⚠️ يرجى إدخال مفتاح Gemini API في الشريط الجانبي أولاً!")
        elif len(tx_id.strip()) < 5:
            st.warning("⚠️ يرجى إدخال رقم معاملة صحيح من باينانس للتحقق.")
        else:
            # إعداد نموذج الذكاء الاصطناعي
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            with st.spinner("⏳ جاري قراءة العقد وتحليله باستخدام الذكاء الاصطناعي..."):
                time.sleep(1) # محاكاة معالجة صغيرة

                # بناء التوجيه (Prompt) بناءً على نوع الخدمة المختارة
                if "كشف المخاطر" in service_option:
                    prompt = f"""
                    أنت خبير قانوني ومحامٍ محترف. قم بتحليل العقد التالي باللغة العربية:
                    1. إعطاء درجة أمان العقد كنسبة مئوية (مثال: 70%).
                    2. استخراج أهم 3 إلى 5 بنود مجحفة أو مخاطر قانونية (بنود فخ) قد تضر بالمستخدم.
                    3. اقتراح صياغة بديلة آمنة لكل بند خطير.
                    
                    نص العقد:
                    {text[:8000]}
                    """
                elif "التلخيص الشامل" in service_option:
                    prompt = f"""
                    أنت خبير قانوني. ملخص شامل وواضح للعقد التالي باللغة العربية:
                    1. ملخص تنفيذي في 4 أسطر.
                    2. حقوق وواجبات كل طرف بشكل نقاط محددة.
                    3. الشروط المالية والعقوبات إن وجدت.
                    
                    نص العقد:
                    {text[:8000]}
                    """
                else:
                    prompt = f"""
                    أنت استشاري تفاوض عقود. بناءً على هذا العقد:
                    1. ما هي أهم 5 أسئلة ذكية يجب أن يطرحها العميل على الطرف الآخر قبل التوقيع؟
                    2. اكتب رسالة إيميل/واتساب احترافية يمكن للعميل نسخها وإرسالها للتفاوض على التعديلات.
                    
                    نص العقد:
                    {text[:8000]}
                    """

                try:
                    response = model.generate_content(prompt)
                    st.balloons()
                    st.success("🎉 تم استخراج التحليل بنجاح!")
                    st.markdown("### 📋 التقرير القانوني المخصص:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
                  
