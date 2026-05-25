import streamlit as st

# Tắt các tính năng kiểm tra mạng gây tốn tài nguyên
st.set_page_config(page_title="English In Use", layout="wide")

# Dùng cache để lưu dữ liệu vào RAM server, tránh đọc lại gây lỗi 500
@st.cache_data
def load_data():
    return {
        "Unit 1: Family": [
            {"en": "Parents", "vi": "Bố mẹ"},
            {"en": "Grandparents", "vi": "Ông bà"}
        ]
    }

def main():
    st.title("📚 English Elementary")
    
    # Hiển thị thông báo trạng thái mạng
    st.sidebar.success("Trạng thái: Đang chạy")
    
    data = load_data()
    unit = st.selectbox("Chọn bài học:", list(data.keys()))

    for item in data[unit]:
        with st.container():
            st.markdown(f"### {item['en']}")
            st.write(f"Nghĩa: {item['vi']}")
            # Không dùng tts_url phức tạp, chỉ hiện text trước để test ổn định
            st.write("---")

if __name__ == "__main__":
    main()
