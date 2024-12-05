import requests
import json
import tempfile
import pickle
import streamlit as st

api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
api_key = "AIzaSyB1Z8o2ipBbuuSJOI3a8okqkrSBs5_Tx28"
# api_key = "AIzaSyB-rs1m6IHd0Kdaf7Dno3TwTQGYMP9OGy8"

def google_gemini_translate(input_text, input_language=None, target_language_code=None):
    headers = {
        "Content-Type": "application/json"
    }   
    
    if target_language_code:
        text_request = f"Please translate this {input_text} into {target_language_code}. If the content is already in {target_language_code}, keep it as it is without any changes or suggestions. Keep the same semantic meaning as original input text. Return the output in paragraph form."
    elif input_language:
        text_request = f"Please translate this {input_text} from {input_language} into {target_language_code}. If the content is already in {target_language_code}, keep it as it is without any changes or suggestions. Keep the same semantic meaning as original input text. Return the output in paragraph form."
    else:
        text_request = input_text

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": text_request
                    }
                ]
            }   
        ]
    }
    
    params = {
        "key": api_key
    }
    
    try:
        response = requests.post(api_url, headers=headers, params=params, json=data)
        response.raise_for_status()
        result = response.json()

        print("API Response:", json.dumps(result, indent=2))

        if 'candidates' in result and len(result['candidates']) > 0:
            candidate = result['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                translated_text = ''.join(part['text'] for part in candidate['content']['parts'])
                return translated_text
        
        return input_text
    
    except requests.exceptions.RequestException as e:
        print(f"Error querying Gemini API: {e}")
        return None
    
# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role
    

# Hàm để gọi API Gemini và trả lời câu hỏi
def get_gemini_response_pdf(query, context):
    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
    
    data = {
        "contents": [
            {
                "parts": [
                    {"text": f"Answer the following question based on the context: {query} \nContext: {context}"}
                ]
            }
        ]
    }
    
    params = {
        "key": api_key
    }

    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(api_url, headers=headers, params=params, json=data)
        response.raise_for_status()
        result = response.json()

        # Trả về câu trả lời từ Gemini
        if 'candidates' in result and len(result['candidates']) > 0:
            candidate = result['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                translated_text = ''.join(part['text'] for part in candidate['content']['parts'])
                return translated_text
        return "Không có câu trả lời từ Gemini API."
    
    except requests.exceptions.RequestException as e:
        print(f"Error querying Gemini API: {e}")
        return "Lỗi khi gọi API Gemini."
    
def save_to_temp(chunks):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        pickle.dump(chunks, temp_file)
        temp_file.close()
    return temp_file.name

def load_from_temp(temp_file_path):
    with open(temp_file_path, "rb") as temp_file:
        return pickle.load(temp_file)
    
def update_chat_history(role, message):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []  # Khởi tạo lịch sử trò chuyện nếu chưa có
    st.session_state.chat_history.append({"role": role, "text": message})