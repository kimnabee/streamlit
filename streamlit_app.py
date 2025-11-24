import streamlit as st
import openai
from openai import OpenAI

st.title("GPT-5-Mini")

api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")

if api_key:
    st.session_state["API_KEY"] = api_key
    client = OpenAI(api_key=api_key) 
    st.session_state["openai_client"]=client



@st.cache_data
def generate_response(prompt):      
    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )
    st.write(response.output_text)


prompt_t=st.text_input("질문을 입력하세요")
if st.button("ask"):
    generate_response(prompt_t)