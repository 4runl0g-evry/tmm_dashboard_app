from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv

def chatbot_text():
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        
    st.title("An AI assistant")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How may I assist you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        client = OpenAI(api_key=OPENAI_API_KEY)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)