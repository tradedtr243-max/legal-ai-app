import streamlit as st
import google.generativeai as genai
import pypdf

st.set_page_config(
    page_title="المحلل القانوني الذكي (LegalAI Pro)",
    page_icon="⚖️",
    layout="wide"
)

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ يرجى التأكد من ضبط GEMINI_API_KEY في Streamlit Secrets.")

st.sidebar.title("💳 خطة الاشتراك والدفع")
st.sidebar.info(
    """
    **رسوم الخدمة:** $1 (USDT) لكل تحليل عقد.
    
    **طريقة الدفع (Cwallet - USDT TRC20):**
    يرجى تحويل مبلغ 1 USDT إلى عنوان محفظتك التالي:
    
    `TARHeCaPUGGe3CHhuPMxtxvC2STNx6U6yr`
    
    *(تأكد من الإرسال عبر شبكة TRC20 حصراً)*
    """
)

st.sidebar.subheader("🔒 تأكيد عملية الدفع")
tx_id = st.sidebar.text_input("أدخل رقم المعاملة (Transaction Hash / ID):")

st.title("⚖️ المحلل القانوني الذكي (LegalAI Pro)")
st.write("أداة تحليل العقود والمستندات الذكية: كشف الثغرات، حساب المخاطر، واستراتيجيات التفاوض.")

uploaded_file = st.file_uploader("(PDF صيغة) قم برفع العقد أو المستند", type=["pdf"])

if uploaded_file is not None:
    if not tx_id.strip():
        st.warning("⚠️ يرجى إدخال رقم المعاملة (Transaction ID) في القائمة الجانبية لتأكيد الدفع وتفعيل التحليل.")
    else:
        st.success("✅ تم استلام رقم المعاملة وجاري معالجة العقد...")
        
        pdf_reader = pypdf.PdfReader(uploaded_file)
        text_content = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text_content += extracted + "\n"

        if text_content.strip():
            st.info("📄 تم قراءة المستند بنجاح. جاري التحليل بواسطة الذكاء الاصطناعي...")
            
            prompt = f"""
            أنت مستشار قانوني خبير وخبير تفاوض. قم بتحليل المستند القانوني التالي بدقة:
            
            1. **ملخص شامل:** الأطراف المعنية والهدف الأساسي من العقد.
            2. **الثغرات والمخاطر:** كشف الشروط المجحفة، الثغرات القانونية، والعموميات المريبة.
            3. **تقييم درجة المخاطرة:** إعطاء نسبة مئوية للمخاطرة (مثال: مخاطرة منخفضة/متوسطة/عالية).
            4. **نصائح استراتيجية للتفاوض:** تعديلات مقترحة لبنود العقد لحماية حقوق المستخدم.

            نص العقد:
            {text_content}
            """
            
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                
                st.subheader("📊 نتيجة التحليل القانوني الشامل:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
        else:
            st.error("لم نتمكن من قراءة أي نص داخل ملف الـ PDF. تأكد أن الملف ليس عبارة عن صور فقط.")
            
