import streamlit as st
import json

# 1. Cấu hình giao diện tối ưu cho di động (Centered giúp gom cụm nội dung)
st.set_page_config(page_title="Học Tiếng Anh", page_icon="🇬🇧", layout="centered")

# CSS chuyên biệt cho di động: Phóng to nút bấm, căn giữa nội dung và ẩn menu thừa
mobile_style = """
    <style>
    /* Ẩn các thành phần thừa để tăng không gian hiển thị trên màn hình nhỏ */
    减轻 không gian hiển thị {display: none;}
    .stAppDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Phóng to font chữ toàn app cho dễ đọc trên điện thoại */
    html, body, [data-testid="stWidgetLabel"] p {
        font-size: 18px !important;
    }
    
    /* Làm các nút bấm to hơn, dễ dùng ngón tay ấn (Touch-friendly) */
    .stButton>button {
        width: 100% !important;
        height: 55px !important;
        font-size: 18px !important;
        border-radius: 12px !important;
        margin-bottom: 10px !important;
    }
    
    /* Định dạng khung Flashcard nổi bật */
    .flashcard-box {
        background-color: #f0f2f6;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #ddd;
        margin-bottom: 20px;
    }
    </style>
    """
st.markdown(mobile_style, unsafe_allow_html=True)

# 2. Dữ liệu bài học
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
            "question": "Complete: 'She was ______ to text him back because she was busy.'",
            "options": ["reluctant", "eager", "happy", "excited"],
            "answer": "reluctant"
        }
    ]
}

# Khởi tạo trạng thái bộ nhớ cho app
if 'current_flashcard' not in st.session_state:
    st.session_state.current_flashcard = 0
if 'show_meaning' not in st.session_state:
    st.session_state.show_meaning = False

st.title("🎯 English Mobile Hub")

# Sử dụng Selectbox thay vì Tabs vì giao diện tab trên điện thoại rất dễ bị tràn và mất chữ
choice = st.selectbox("Chọn phần học:", ["🗂️ Từ Vựng (Flashcard)", "📝 Trắc Nghiệm (Quiz)", "🔊 Luyện Nghe"])

st.write("---")

# --- PHẦN 1: FLASHCARD TỪ VỰNG ---
if choice == "🗂️ Từ Vựng (Flashcard)":
    vocab_list = DATA_SAMPLE["vocabulary"]
    idx = st.session_state.current_flashcard
    
    st.caption(f"Tiến độ: {idx + 1} / {len(vocab_list)}")
    
    # Giao diện thẻ từ vựng bo góc, chữ to
    if not st.session_state.show_meaning:
        st.markdown(f'<div class="flashcard-box"><h2>🔤 {vocab_list[idx]["word"]}</h2><p>({vocab_list[idx]["type"]})</p><br><p>💡 <i>Chạm "Lật Thẻ" để xem nghĩa</i></p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="flashcard-box" style="background-color: #e8f5e9; border-color: #a5d6a7;"><h2>🔤 {vocab_list[idx]["word"]}</h2><p><b>Nghĩa:</b> {vocab_list[idx]["meaning"]}</p><p style="font-size: 15px; color: #555;"><b>Ví dụ:</b> {vocab_list[idx]["example"]}</p></div>', unsafe_allow_html=True)
        
    # Hệ thống nút bấm xếp dọc hoàn toàn để không bị thu nhỏ trên điện thoại
    if st.button("🔄 LẬT THẺ"):
        st.session_state.show_meaning = not st.session_state.show_meaning
        st.rerun()
        
    if st.button("⏩ TỪ TIẾP THEO"):
        st.session_state.current_flashcard = (idx + 1) % len(vocab_list)
        st.session_state.show_meaning = False
        st.rerun()
        
    if st.button("⏪ TỪ TRƯỚC ĐÓ"):
        st.session_state.current_flashcard = (idx - 1) % len(vocab_list)
        st.session_state.show_meaning = False
        st.rerun()

# --- PHẦN 2: TRẮC NGHIỆM ---
elif choice == "📝 Trắc Nghiệm (Quiz)":
    st.header("Bài Kiểm Tra Ngắn")
    quizzes = DATA_SAMPLE["quiz"]
    
    score = 0
    with st.form("quiz_form"):
        user_answers = []
        for i, q in enumerate(quizzes):
            st.markdown(f"**Câu {i+1}: {q['question']}**")
            # Thiết kế ô chọn đáp án thưa ra để ngón tay dễ bấm không bị nhầm
            ans = st.radio(f"Chọn đáp án {i+1}", q["options"], key=f"q_{i}", label_visibility="collapsed")
            user_answers.append(ans)
            st.write("")
            
        # Nộp bài bằng nút bấm lớn ở cuối
        submit_quiz = st.form_submit_button("🔥 NỘP BÀI KIỂM TRA")
        
        if submit_quiz:
            for i, q in enumerate(quizzes):
                if user_answers[i] == q["answer"]:
                    score += 1
            if score == len(quizzes):
                st.balloons()
                st.success(f"🎉 Xuất sắc! Điểm của bạn: {score}/{len(quizzes)}")
            else:
                st.warning(f"📱 Bạn đúng: {score}/{len(quizzes)}. Thử lại nhé!")

# --- PHẦN 3: LUYỆN NGHE ---
elif choice == "🔊 Luyện Nghe":
    st.header("Luyện Phát Âm TTS")
    st.write("Nhập câu tiếng Anh vào ô dưới để nghe máy đọc:")
    
    text_to_speak = st.text_area("Nhập văn bản tại đây:", "Hello! Welcome to your mobile English app.", height=100)
    
    if st.button("🔊 PHÁT ÂM NGAY"):
        tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={text_to_speak.replace(' ', '+')}"
        # Trình phát nhạc tự động co giãn vừa vặn chiều ngang điện thoại
        st.audio(tts_url, format="audio/mp3")
