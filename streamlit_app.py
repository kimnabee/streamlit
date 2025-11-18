import streamlit as st
import openai
from openai import OpenAI
import base64

st.write("Hello World")

api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")


prompt_t = st.text_input("텍스트 프롬프트를 입력하세요")

if st.button("실행"):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-5-mini",  
        messages=[
                {"role": "user", "content": prompt_t}
                ]
                )
    response_text = completion.choices[0].message.content
    st.write(response_text)


st.markdown("---")


prompt_i = st.text_input("이미지 프롬프트를 입력하세요")

if st.button("이미지 생성"):
    client = OpenAI(api_key=api_key)
    img = client.images.generate(
    model="gpt-image-1-mini",
    prompt=prompt_i)

    image_bytes = base64.b64decode(img.data[0].b64_json)
    st.success("완성된 이미지:")
    st.image(image_bytes)