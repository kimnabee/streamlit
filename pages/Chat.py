import streamlit as st
from openai import OpenAI

st.title("Chat")

api_key = st.session_state.api_key
client = OpenAI(api_key=api_key)

### 함수
def get_gpt_response(messages_list):
        response = client.responses.create(
        model="gpt-5-mini",
        input=messages_list)
        return response.output_text

### 메모리 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []


### clear 버튼
def clear_chat_history():
    st.session_state.messages = []

st.button("Clear", on_click=clear_chat_history)
st.markdown("---")


### 저장한 메세지 구분 출력
for msg in st.session_state.messages:
 with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


 ### 사용자 입력과 LLM 응답
if prompt := st.chat_input("여기에 메시지를 입력하세요..."):
    # 사용자 메시지 보여주기
    st.chat_message("user").markdown(prompt)
    # 메모리에 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    # LLM 응답 가져오는 기능 추가 필요
    response = f"Echo: {prompt}"
    # LLM 응답 보여주기
    with st.chat_message("assistant"):
        st.markdown(response)
    # 메모리에 LLM 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": response})