from flask import Flask, request, jsonify, render_template
from pyvi import ViTokenizer
import unicodedata
import json

app = Flask(__name__)

# Load dữ liệu lịch sử
def load_history_data(file_name="english_history_partial.json"):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Chuẩn hóa văn bản
def normalize_text(text):
    return unicodedata.normalize('NFKC', text).lower()

# Trích xuất thực thể
def extract_entity_from_question(question, known_entities):
    question_norm = normalize_text(ViTokenizer.tokenize(question))
    return [entity for entity in known_entities if normalize_text(entity) in question_norm]

# Trả lời câu hỏi
def answer_question(question, history_data):
    entities = extract_entity_from_question(question, history_data.keys())
    if not entities:
        return " Xin lỗi, tôi không nhận diện được thực thể nào trong câu hỏi."
    answers = [f" {entity}:\n{history_data[entity]}" for entity in entities if entity in history_data]
    return "\n\n".join(answers) if answers else " Xin lỗi, tôi chưa có thông tin về thực thể này."

# Nạp dữ liệu
history_data = load_history_data()

@app.route('/')
def home():
    return render_template('index.html')  # Dùng template bạn đã có

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question', '')
    if question.lower().strip() == 'thoát':
        return jsonify({"response": "Tạm biệt!"})
    answer = answer_question(question, history_data)
    return jsonify({"response": answer})

if __name__ == '__main__':
    app.run(debug=True)
