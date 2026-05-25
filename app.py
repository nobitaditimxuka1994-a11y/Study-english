import streamlit as st
import urllib.parse

# 1. Cấu hình trang tối giản (Chống giật lag cho mobile)
st.set_page_config(page_title="Học từ vựng - In Use", layout="centered")

# 2. CSS làm đẹp giao diện chuyên nghiệp
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .unit-title { color: #1e88e5; font-weight: bold; border-bottom: 2px solid #1e88e5; padding-bottom: 5px; }
    .word-card {
        background: white; 
        padding: 15px; 
        border-radius: 12px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 12px;
        border-left: 6px solid #1e88e5;
    }
    .phonetic { color: #666; font-style: italic; font-size: 0.9em; }
    .meaning { color: #2e7d32; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

# 3. DỮ LIỆU TRÍCH XUẤT TỪ FILE PDF (Học liệu chính)
# Tôi đã chia nhỏ để bạn không phải gọi file PDF nặng nề
DATA = {
    "Unit 1: The Family": [
        {"en": "Grandparents", "ipa": "/ˈɡrænpeərənts/", "vi": "Ông bà"},
        {"en": "Uncle", "ipa": "/ˈʌŋkl/", "vi": "Chú, bác trai"},
        {"en": "Aunt", "ipa": "/ɑːnt/", "vi": "Cô, dì, bác gái"},
        {"en": "Cousin", "ipa": "/ˈkʌzn/", "vi": "Anh chị em họ"},
        {"en": "Niece", "ipa": "/niːs/", "vi": "Cháu gái"},
        {"en": "Nephew", "ipa": "/ˈnefjuː/", "vi": "Cháu trai"}
    ],
    "Unit 3: Parts of the body": [
        {"en": "Shoulder", "ipa": "/ˈʃəʊldə/", "vi": "Vai"},
        {"en": "Stomach", "ipa": "/ˈstʌmək/", "vi": "Bụng/Dạ dày"},
        {"en": "Knee", "ipa": "/niː/", "vi": "Đầu gối"},
        {"en": "Thumb", "ipa": "/θʌm/", "vi": "Ngón tay cái"},
        {"en": "Toes", "ipa": "/təʊz/", "vi": "Các ngón chân"}
    ],
    "Unit 4: Appearance": [
        {"en": "Fair hair", "ipa": "/feə heə/", "vi": "Tóc vàng nhạt"},
        {"en": "Overweight", "ipa": "/ˌəʊvəˈweɪt/", "vi": "Thừa cân"},
        {"en": "Good-looking", "ipa": "/ˌɡʊd ˈlʊkɪŋ/", "vi": "Ưa nhìn"},
        {"en": "Slim", "ipa": "/slɪm/", "vi": "Mảnh khảnh"}
    ]
}

def main():
    st.title("📚 Vocabulary In Use")
    
    # Menu chọn bài học
    unit_list = list(DATA.keys())
    selected_unit = st.selectbox("📖 Chọn bài học hôm nay:", unit_list)

    st.markdown(f"<h2 class='unit-title'>{selected_unit}</h2>", unsafe_allow_html=True)

    # Hiển thị danh sách từ vựng dưới dạng Card
    for item in DATA[selected_unit]:
        with st.container():
            st.markdown(f"""
            <div class="word-card">
                <div style="font-size: 1.2em; font-weight: bold;">{item['en']}</div>
                <div class="phonetic">{item['ipa']}</div>
                <div class="meaning">{item['vi']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Nút phát âm - Sử dụng URL trực tiếp từ Google TTS để tránh treo server
            word_encoded = urllib.parse.quote(item['en'])
            tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={word_encoded}"
            
            # Trình phát nhạc gọn nhẹ cho mobile
            st.audio(tts_url, format="audio/mp3")
            st.write("---")

    # Phần Luyện Nghe tự do
    st.sidebar.title("🔊 Luyện phát âm")
    text_input = st.sidebar.text_area("Nhập câu muốn nghe:", height=100)
    if st.sidebar.button("Nghe ngay"):
        if text_input:
            q = urllib.parse.quote(text_input)
            url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={q}"
            st.sidebar.audio(url)

if __name__ == "__main__":
    main()
