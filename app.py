import streamlit as st
import urllib.parse

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="English Vocabulary In Use", layout="wide")

# --- GIAO DIỆN CSS (Tối ưu cho điện thoại) ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stSelectbox [data-testid="stMarkdownContainer"] { font-weight: bold; color: #1E1E1E; }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background-color: #2E7D32; color: white; font-weight: bold; border: none;
    }
    .word-card {
        background: white; padding: 15px; border-radius: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 10px;
        border-left: 5px solid #2E7D32;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DỮ LIỆU TỪ PDF (Đã chia nhỏ theo từng Unit) ---
COURSE_DATA = {
    "Unit 1: The Family (Gia đình)": [
        {"en": "Parents", "ipa": "/ˈpeərənts/", "vi": "Bố mẹ"},
        {"en": "Husband and wife", "ipa": "/ˈhʌzbənd ænd waɪf/", "vi": "Chồng và vợ"},
        {"en": "Daughter and son", "ipa": "/ˈdɔːtə ænd sʌn/", "vi": "Con gái và con trai"},
        {"en": "Grandparents", "ipa": "/ˈɡrænpeərənts/", "vi": "Ông bà"},
        {"en": "Aunt and uncle", "ipa": "/ɑːnt ænd ˈʌŋkl/", "vi": "Cô/dì và chú/bác"},
        {"en": "Niece and nephew", "ipa": "/niːs ænd ˈnefjuː/", "vi": "Cháu gái và cháu trai"}
    ],
    "Unit 3: Parts of the body (Cơ thể)": [
        {"en": "Shoulder", "ipa": "/ˈʃəʊldə/", "vi": "Vai"},
        {"en": "Knee", "ipa": "/niː/", "vi": "Đầu gối"},
        {"en": "Chest", "ipa": "/tʃest/", "vi": "Ngực"},
        {"en": "Blood", "ipa": "/blʌd/", "vi": "Máu"},
        {"en": "Heart", "ipa": "/hɑːt/", "vi": "Trái tim"},
        {"en": "Brain", "ipa": "/breɪn/", "vi": "Não"}
    ],
    "Unit 4: Appearance (Ngoại hình)": [
        {"en": "Tall and slim", "ipa": "/tɔːl ænd slɪm/", "vi": "Cao và mảnh khảnh"},
        {"en": "Overweight", "ipa": "/ˌəʊvəˈweɪt/", "vi": "Thừa cân"},
        {"en": "Good-looking", "ipa": "/ˌɡʊd ˈlʊkɪŋ/", "vi": "Ưa nhìn/Đẹp trai"},
        {"en": "Straight hair", "ipa": "/streɪt heə/", "vi": "Tóc thẳng"},
        {"en": "Curly hair", "ipa": "/ˈkɜːli heə/", "vi": "Tóc xoăn"}
    ]
}

# --- MENU CHÍNH ---
choice = st.selectbox("🎯 CHỌN CHẾ ĐỘ HỌC", ["📚 Bài học từ PDF", "🔊 Luyện Phát Âm TTS", "📝 Kiểm tra"])

# --- PHẦN 1: BÀI HỌC TỪ PDF ---
if choice == "📚 Bài học từ PDF":
    unit_choice = st.selectbox("Chọn bài học:", list(COURSE_DATA.keys()))
    
    st.markdown(f"### 📖 {unit_choice}")
    
    for item in COURSE_DATA[unit_choice]:
        with st.container():
            st.markdown(f"""
            <div class="word-card">
                <span style="font-size: 1.2em; font-weight: bold; color: #2E7D32;">{item['en']}</span><br>
                <span style="color: #666;">{item['ipa']}</span><br>
                <span style="font-size: 1.1em;">{item['vi']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Nút bấm phát âm nhanh cho từng từ
            if st.button(f"🔊 Nghe: {item['en']}", key=item['en']):
                safe_text = urllib.parse.quote(item['en'])
                tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={safe_text}"
                st.audio(tts_url, format="audio/mp3")

# --- PHẦN 2: LUYỆN PHÁT ÂM ---
elif choice == "🔊 Luyện Phát Âm TTS":
    st.title("🔊 Luyện Nghe & Nói")
    st.info("Nhập bất kỳ câu nào từ sách để luyện nghe chuẩn.")
    
    input_text = st.text_area("Nhập văn bản tiếng Anh:", height=100)
    
    if st.button("🚀 PHÁT ÂM"):
        if input_text:
            try:
                safe_text = urllib.parse.quote(input_text)
                tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={safe_text}"
                st.audio(tts_url, format="audio/mp3")
                st.success("Đã tải xong âm thanh!")
            except Exception:
                st.error("Mạng 4G yếu, vui lòng thử lại.")

# --- PHẦN 3: KIỂM TRA (Dựa trên dữ liệu PDF) ---
elif choice == "📝 Kiểm tra":
    st.title("📝 Quiz theo bài học")
    unit_quiz = st.selectbox("Chọn bài để kiểm tra:", list(COURSE_DATA.keys()))
    
    with st.form("quiz_form"):
        score = 0
        questions = COURSE_DATA[unit_quiz]
        user_ans = []
        
        for i, q in enumerate(questions[:3]): # Lấy 3 câu hỏi ngẫu nhiên
            st.write(f"Câu {i+1}: Nghĩa của từ **'{q['en']}'** là gì?")
            ans = st.radio("Chọn đáp án:", [q['vi'], "Sai 1", "Sai 2"], key=f"quiz_{i}")
            user_ans.append(ans)
        
        if st.form_submit_button("NỘP BÀI"):
            for i, q in enumerate(questions[:3]):
                if user_ans[i] == q['vi']:
                    score += 1
            st.metric("Điểm của bạn", f"{score}/3")
            if score == 3: st.balloons()

# --- FOOTER ---
st.markdown("<br><hr><center><small>Dữ liệu: English Vocabulary in Use (Elementary)</small></center>", unsafe_allow_html=True)
