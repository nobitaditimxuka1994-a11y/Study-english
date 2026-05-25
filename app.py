from flask import Flask, render_template
import os

app = Flask(__name__)

# DỮ LIỆU CHUẨN
lessons_data = {
    "unit1": {
        "title": "Parts of the body",
        "words": [
            {"en": "Shoulder", "vi": "Vai", "ipa": "/ˈʃəʊldə/"},
            {"en": "Knee", "vi": "Đầu gối", "ipa": "/niː/"}
        ]
    }
}

@app.route('/')
def index():
    # Quan trọng: Truyền biến lessons_data vào
    return render_template('index.html', lessons=lessons_data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
