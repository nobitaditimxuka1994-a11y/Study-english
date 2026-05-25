from flask import Flask, render_template_string, jsonify
import urllib.parse

app = Flask(__name__)

# DỮ LIỆU TỪ PDF (Có thể mở rộng lên hàng trăm Unit)
data_lessons = {
    "unit1": {
        "title": "The Family",
        "words": [
            {"en": "Parents", "vi": "Bố mẹ", "ipa": "/ˈpeərənts/"},
            {"en": "Cousin", "vi": "Anh chị em họ", "ipa": "/ˈkʌzn/"}
        ]
    },
    "unit3": {
        "title": "Parts of the body",
        "words": [
            {"en": "Shoulder", "vi": "Vai", "ipa": "/ˈʃəʊldə/"},
            {"en": "Knee", "vi": "Đầu gối", "ipa": "/niː/"}
        ]
    }
}

# GIAO DIỆN HTML (Thiết kế chuẩn Mobile, mượt như app thật)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>English Pro</title>
    <style>
        body { font-family: sans-serif; background: #f0f2f5; margin: 0; padding: 20px; }
        .card { background: white; border-radius: 15px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .word { font-size: 1.2em; font-weight: bold; color: #1a73e8; }
        .ipa { color: #666; font-style: italic; }
        .vi { color: #2ecc71; margin-top: 5px; }
        button { background: #1a73e8; color: white; border: none; padding: 10px; border-radius: 8px; width: 100%; margin-top: 10px; cursor: pointer; }
        select { width: 100%; padding: 10px; border-radius: 8px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h2>📚 English Elementary</h2>
    <select onchange="location = this.value;">
        <option value="/">Chọn bài học...</option>
        {% for id, content in lessons.items() %}
            <option value="/lesson/{{id}}">{{content.title}}</option>
        {% endfor %}
    </select>

    {% if current_lesson %}
        <h3>{{ current_lesson.title }}</h3>
        {% for item in current_lesson.words %}
        <div class="card">
            <div class="word">{{ item.en }}</div>
            <div class="ipa">{{ item.ipa }}</div>
            <div class="vi">{{ item.vi }}</div>
            <button onclick="playAudio('{{ item.en }}')">🔊 Nghe phát âm</button>
        </div>
        {% endfor %}
    {% endif %}

    <script>
        function playAudio(text) {
            var url = "https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q=" + encodeURIComponent(text);
            var audio = new Audio(url);
            audio.play();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, lessons=data_lessons, current_lesson=None)

@app.route('/lesson/<unit_id>')
def lesson(unit_id):
    current = data_lessons.get(unit_id)
    return render_template_string(HTML_TEMPLATE, lessons=data_lessons, current_lesson=current)

if __name__ == '__main__':
    app.run(debug=True)
