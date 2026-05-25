import streamlit as st
import requests
import urllib.parse

# Cấu hình cực nhẹ để không tốn băng thông 4G
st.set_page_config(page_title="Học Tiếng Anh", layout="centered")

# Tối ưu hóa bộ nhớ: Lưu dữ liệu vào cache để không phải load lại nhiều lần
@st.cache_data
def get_vocabulary():
    # Dữ liệu mẫu từ PDF (Bạn có thể thêm tiếp vào đây)
    return {
        "Unit 1: Family": [
            {"en": "Parents", "vi": "Bố mẹ"},
            {"en": "Grandparents", "vi": "Ông bà"}
        ],
        "Unit 3: Body": [
            {"en": "Head", "vi": "Đầu"},
            {"en": "Shoulder", "vi": "Vai"}
        ]
    }

def main():
    try:
        st.title("🚀 English Pro Mobile")
        data = get_vocabulary()
        
        menu = st.selectbox("Menu chính", ["Học từ vựng", "Luyện nghe"])
        
        if menu == "Học từ vựng":
            unit = st.selectbox("Chọn bài học:", list(data.keys()))
            for item in data[unit]:
                with st.expander(f"Từ vựng: {item['en']}"):
                    st.write(f"Nghĩa: {item['vi']}")
                    # Dùng link trực tiếp để máy khách (điện thoại) tự tải, server không phải tải
                    q = urllib.parse.quote(item['en'])
                    audio_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={q}"
                    st.audio(audio_url)
                    
        elif menu == "Luyện nghe":
            text = st.text_area("Nhập văn bản:", "Hello")
            if st.button("Phát âm"):
                q = urllib.parse.quote(text)
                st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={q}")

    except Exception as e:
        # Nếu có lỗi, hiện thông báo tiếng Việt thay vì lỗi 500 của hệ thống
        st.error("Mạng yếu hoặc có lỗi xảy ra. Hãy vuốt màn hình xuống để tải lại trang.")

if __name__ == "__main__":
    main()
