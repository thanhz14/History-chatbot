from flask import Flask, request, jsonify, render_template
import spacy
import json

# Tải mô hình spaCy (tiếng Anh ở đây, có thể thay bằng tiếng Việt)
nlp = spacy.load("en_core_web_sm")  # Hoặc vi_core_news_lg cho tiếng Việt

## Tải dữ liệu lịch sử
def load_history_data(file_name="lich_su_partial.json"):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            history_data = json.load(f)
        return history_data
    except FileNotFoundError:
        return {}

# Hàm nhận diện thực thể trong câu hỏi
def extract_entity_from_question(question):
    doc = nlp(question)
    entities = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities.append(ent.text)
    return entities

# Hàm trả lời câu hỏi dựa trên dữ liệu lịch sử
def answer_question(question, history_data):
    entities = extract_entity_from_question(question)
    
    if not entities:
        return "Xin lỗi, tôi không nhận diện được tên người trong câu hỏi."

    for entity in entities:
        if entity in history_data:
            return history_data[entity]
    
    return "Xin lỗi, tôi chưa có thông tin về câu hỏi này."

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# Dữ liệu lịch sử
history_data = load_history_data()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Lấy câu hỏi từ người dùng
    data = request.get_json()
    question = data.get('question', '')
    
    if question.lower() == 'thoát':
        return jsonify({"response": "Tạm biệt!"})
    
    # Trả lời câu hỏi
    answer = answer_question(question, history_data)
    
    return jsonify({"response": answer})

# Chạy ứng dụng
if __name__ == '__main__':
    app.run(debug=True)
