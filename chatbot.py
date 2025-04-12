import json
import spacy

# Tải mô hình spaCy tiếng Anh
nlp = spacy.load("en_core_web_sm")

# Hàm tải dữ liệu lịch sử từ file JSON
def load_history_data(file_name="lich_su_partial.json"):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            history_data = json.load(f)
        return history_data
    except FileNotFoundError:
        print("File dữ liệu lịch sử không tồn tại.")
        return {}

# Hàm nhận diện thực thể trong câu hỏi
def extract_entity_from_question(question):
    doc = nlp(question)
    entities = []
    for ent in doc.ents:
        # Lấy những thực thể có thể là tên người
        if ent.label_ in ["PERSON"]:
            entities.append(ent.text)
    return entities

# Hàm trả lời câu hỏi dựa trên dữ liệu lịch sử
def answer_question(question, history_data):
    entities = extract_entity_from_question(question)
    
    if not entities:
        return "Xin lỗi, tôi không nhận diện được tên người trong câu hỏi."

    for entity in entities:
        # Kiểm tra tên thực thể có trong dữ liệu lịch sử không
        if entity in history_data:
            return history_data[entity]
    
    return "Xin lỗi, tôi chưa có thông tin về câu hỏi này."

# Hàm chính chatbot
def main():
    print("🤖 Chatbot Lịch Sử Việt Nam (dùng spaCy) - Gõ 'thoát' để kết thúc.")
    history_data = load_history_data()

    while True:
        question = input("Bạn: ")
        
        if question.lower() == 'thoát':
            print("Bot: Tạm biệt!")
            break

        # Trả lời câu hỏi dựa trên dữ liệu lịch sử
        answer = answer_question(question, history_data)
        print(f"Bot: {answer}")

# Chạy chatbot
if __name__ == "__main__":
    main()
