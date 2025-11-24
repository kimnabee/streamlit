import streamlit as st
from openai import OpenAI

st.title("Chat")

client = st.session_state.get('openai_client', None)

if client is None:
    st.error("API 키가 설정되지 않았습니다. 먼저 API 키를 입력하세요.")
    st.stop()



def get_gpt_response(prompt):
    response=client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )
    return response.output_text


if "messages" not in st.session_state:
    st.session_state.messages = []


if st.button("Clear"):
    del st.session_state["messages"]


st.markdown("---")


for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])



if prompt := st.chat_input("여기에 메시지를 입력하세요..."):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user","content": prompt})

    response_text = get_gpt_response(st.session_state.messages)

    with st.chat_message("assistant"):
        st.markdown(response_text)

    st.session_state.messages.append({"role": "assistant","content": response_text})