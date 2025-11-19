import streamlit as st
from openai import OpenAI

st.title("Chat")

api_key = st.session_state.get("api_key", None)

if not api_key:
    st.error("API 키가 설정되지 않았습니다. 먼저 API 키를 입력하세요.")
    st.stop()

client = OpenAI(api_key=api_key)

### GPT 호출 함수
def get_gpt_response(messages_list):
    conversation = ""
    for msg in messages_list:
        conversation += f"{msg['role']}: {msg['content']}\n"

    response = client.responses.create(
        model="gpt-5-mini",
        input=conversation
    )

    return response.output_text



### 메모리 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []


### clear 버튼
def clear_chat_history():
    st.session_state.messages = []

st.button("Clear", on_click=clear_chat_history)
st.markdown("---")


### 저장한 메세지 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


### 사용자 입력
if prompt := st.chat_input("여기에 메시지를 입력하세요..."):

    # UI에 사용자 메시지 출력
    st.chat_message("user").markdown(prompt)

    # 메모리 저장 (올바른 구조)
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # GPT 응답 받기
    response_text = get_gpt_response(st.session_state.messages)

    # UI 출력
    with st.chat_message("assistant"):
        st.markdown(response_text)

    # 메모리에 assistant 답변 저장
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })
