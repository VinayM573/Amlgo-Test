import streamlit as st
import requests
import json

API_URL = "http://localhost:8000/get_response" 
INFO_URL="http://localhost:8000/get_info"

info = requests.get(INFO_URL)
info_details = info.json()
st.set_page_config(page_title="AI Chatbot", layout="wide")
st.title("AI Chatbot using Streamlit + FastAPI")

with st.sidebar:
    st.markdown(f"## Model Info : <span style='color:green'>{info_details['model_name']}</span>",unsafe_allow_html=True)
    # st.write(info_details["model_name"])
    
    st.markdown(f"## Total Chunks: <span style='color:blue'>{info_details['total_chunks']}</span>",unsafe_allow_html=True)
    # st.write(info_details["total_chunks"])
       
    if st.button("Clear Chat"):
        st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Type your question here...")
if query:
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            response = requests.post(API_URL, json={"query": query}, stream=True)
            for chunk in response.iter_lines():
                if chunk:
                    token = chunk.decode("utf-8")
                    full_response += token
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Streaming failed: {e}")

    try:
        sources = response.headers.get("X-Sources")
        if sources:
            with st.expander("📚 Source Texts Used"):
                st.markdown(sources.replace("\\n", "\n"))
    except:
        pass
