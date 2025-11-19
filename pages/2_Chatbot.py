import streamlit as st
from openai import OpenAI

st.title("국립부경대학교 도서관 챗봇")

api_key = st.session_state.get("api_key", None)

if not api_key:
    st.error("API 키가 설정되지 않았습니다. 먼저 API 키를 입력하세요.")
    st.stop()

client = OpenAI(api_key=api_key)

### 파일 업로드 (1회만 실행)
if "pknu_file_id" not in st.session_state:

    uploaded_file = client.files.create(
        file=open("국립부경대학교 도서관 규정.txt", "rb"),
        purpose="user_data"
    )

    st.session_state.pknu_file_id = uploaded_file.id


### PKNU Response 함수
def PKNU_response(message):
    response = client.responses.create(
        model="gpt-5-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_file", "file_id": st.session_state.pknu_file_id},
                    {"type": "input_text", "text": message}
                ]
            }
        ]
    )
    return response.output_text


### 페이지 전용 대화 저장 공간
if "pkunulib_messages" not in st.session_state:
    st.session_state.pkunulib_messages = []

### 저장된 대화 출력
for msg in st.session_state.pkunulib_messages:
    with st.chat_message(msg["role]()_
