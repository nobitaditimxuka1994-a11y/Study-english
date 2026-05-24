import streamlit as st
import json
import random

# 1. Cấu hình giao diện và ẩn Menu thừa giống như bạn yêu cầu
st.set_page_config(page_title="ENGLISH LEARNING HUB", page_icon="🇬🇧", layout="centered")

hide_style = """
    <style>
    .stAppDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_style, unsafe_allow_html=True)

# 2. Khởi tạo dữ liệu mẫu (Nếu không có file data.json)
DATA_SAMPLE = {
    "vocabulary": [
        {"word": "Abandon", "type": "v", "meaning": "Từ bỏ, ruồng bỏ", "example": "He abandoned his career to become a singer."},
        {"word": "Benevolent", "type": "adj", "meaning": "Nhân từ, rộng lượng", "example": "A benevolent old man donated all his money."},
        {"word": "Compel", "type": "v", "meaning": "Bắt buộc, cưỡng bách", "example": "The law will compel employers to provide health insurance."}
    ],
    "quiz": [
        {
            "question": "What is the meaning of 'Benevolent'?",
            "options": ["Cruel", "Kind/Generous", "Angry", "Lazy"],
            "answer": "Kind/Generous"
        },
        {
            "question": "Complete the sentence: 'She was ______ to text him back because she was busy.'",
            "options": ["reluctant", "eager", "happy", "excited"],
            "answer": "reluctant"
        }
    ]
}

# Quản lý trạng thái bằng Session State
if 'current_flashcard' not in st.session_state:
    st.session_state.current_flashcard = 0
if 'show_meaning' not in st.session_state:
    st.session_state.show_meaning = False
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0

# --- TIÊU ĐỀ ỨNG DỤNG ---
st.title("🎯 English Learning Hub")
st.write("Chào mừng bạn đến với ứng dụng luyện tiếng Anh thông minh!")

# Chia các tính năng thành các Tab
tab1, tab2, tab3 = st.tabs(["🗂️ Từ Vựng (Flashcard)", "📝 Trắc Nghiệm (Quiz)", "🎧 Tài Nguyên Học"])

# --- TAB 1: FLASHCARD TỪ VỰNG ---
with tab1:
    st.header("Flashcard Từ Vựng Thông Minh")
    vocab_list = DATA_SAMPLE["vocabulary"]
    idx = st.session_state.current_flashcard
    
    # Hiển thị thẻ từ vựng
    st.info(f"Từ số: {idx + 1} / {len(vocab_list)}")
    
    # Khung hiển thị Từ
    st.subheader(f"🔤 {vocab_list[idx]['word']} ({vocab_list[idx]['type']})")
    
    if st.session_state.show_meaning:
        st.success(f"💡 **Ý nghĩa:** {vocab_list[idx]['meaning']}")
        st.caption(f"✍️ **Ví dụ:** {vocab_list[idx]['example']}")
    else:
        st.write("--- Thẻ đang đóng. Nhấn 'Lật thẻ' để xem nghĩa ---")
        
    # Nút bấm tương tác
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⏪ Trước"):
            st.session_state.current_flashcard = (idx - 1) % len(vocab_list)
            st.session_state.show_meaning = False
            st.rerun()
    with col2:
        if st.button("🔄 Lật thẻ"):
            st.session_state.show_meaning = not st.session_state.show_meaning
            st.rerun()
    with col3:
        if st.button("Sau ⏩"):
            st.session_state.current_flashcard = (idx + 1) % len(vocab_list)
            st.session_state.show_meaning = False
            st.rerun()

# --- TAB 2: TRẮC NGHIỆM ---
with tab2:
    st.header("Bài Kiểm Tra Ngắn")
    quizzes = DATA_SAMPLE["quiz"]
    
    score = 0
    with st.form("quiz_form"):
        user_answers = []
        for i, q in enumerate(quizzes):
            st.markdown(f"**Câu {i+1}: {q['question']}**")
            ans = st.radio(f"Chọn đáp án cho câu {i+1}", q["options"], key=f"q_{i}", label_visibility="collapsed")
            user_answers.append(ans)
            st.write("")
            
        submit_quiz = st.form_submit_values("Nộp bài kiểm tra")
        
        if submit_quiz:
            for i, q in enumerate(quizzes):
                if user_answers[i] == q["answer"]:
                    score += 1
            st.session_state.quiz_score = score
            
            if score == len(quizzes):
                st.balloons()
                st.success(f"Tuyệt vời! Bạn đạt điểm tuyệt đối: {score}/{len(quizzes)}")
            else:
                st.warning(f"Kết quả của bạn: {score}/{len(quizzes)}. Thử lại nhé!")

# --- TAB 3: TÀI NGUYÊN HỌC ---
with tab3:
    st.header("Luyện Nghe qua Audio (TTS)")
    st.write("Nhập một đoạn văn tiếng Anh bất kỳ để luyện nghe phát âm chuẩn:")
    text_to_speak = st.text_area("Đoạn văn tiếng Anh:", "Practice makes perfect. Keep moving forward!")
    
    # Tích hợp phát âm cơ bản thông qua API trình duyệt hoặc liên kết đọc
    if st.button("🔊 Nghe phát âm"):
        # Cách đơn giản không cần cài thư viện nặng: Dùng Google TTS qua link markdown âm thanh
        tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={text_to_speak.replace(' ', '+')}"
        st.audio(tts_url, format="audio/mp3")
