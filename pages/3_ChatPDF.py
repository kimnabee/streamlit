import streamlit as st
from openai import OpenAI

st.header("ChatPDF")

def show_message(msg):
    with st.chat_message(msg['role']):
        st.markdown(msg["content"])

client = st.session_state.get('openai_client', None)

if client is None:
    st.error("API 키가 설정되지 않았습니다. 먼저 API 키를 입력하세요.")
    st.stop()


pdf_file = st.file_uploader("PDF 파일을 업로드하세요", type=['pdf'])
if pdf_file is not None:
    vector_store = client.vector_stores.create(name="ChatPDF")
    file_batch = client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files=[pdf_file]
    )
    st.session_state.vector_store = vector_store

if 'vector_store' not in st.session_state:
    st.markdown("PDF 파일을 업로드하세요.")
    st.stop()


if "chatpdf_messages" not in st.session_state:
    st.session_state.chatpdf_messages = []


col1, col2 = st.columns(2)
with col1:
    if st.button("Clear chat"):
        st.session_state.chatpdf_messages = []

with col2:
    if st.button("Clear Vector store"):
        st.session_state.chatpdf_messages = []
        client.vector_stores.delete(st.session_state.vector_store.id)
        del st.session_state.vector_store


for msg in st.session_state.chatpdf_messages:
    show_message(msg)

if prompt := st.chat_input("여기에 메시지를 입력하세요..."):
    msg = {"role":"user", "content":prompt}
    show_message(msg)
    st.session_state.chatpdf_messages.append(msg)

    response = client.responses.create(
        model="gpt-5-mini",
        input=st.session_state.chatpdf_messages,
        tools=[
            {
                "type":"file_search",
                "vector_store_ids": [st.session_state.vector_store.id]
            }
        ]
    )
    msg = {"role":"assistant", "content":response.output_text}
    show_message(msg)
    st.session_state.chatpdf_messages.append(msg)