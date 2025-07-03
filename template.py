import streamlit as st
import requests
import httpx

API_URL = "http://localhost:8000/get_response"
INFO_URL = "http://localhost:8000/get_info"

# Load model info from FastAPI
try:
    info = requests.get(INFO_URL)
    info_details = info.json()
except Exception as e:
    st.error(f"Failed to fetch model info: {e}")
    info_details = {"model_name": "Unknown", "total_chunks": "N/A"}

# Set up Streamlit page
st.set_page_config(page_title="AI Chatbot", layout="wide")
st.title("🧠 AI Chatbot (Streamlit + FastAPI)")

# Sidebar with model and chunk info
with st.sidebar:
    st.markdown(f"## Model Info: <span style='color:green'>{info_details['model_name']}</span>", unsafe_allow_html=True)
    st.markdown(f"## Total Chunks: <span style='color:blue'>{info_details['total_chunks']}</span>", unsafe_allow_html=True)

    if st.button("Clear Chat"):
        st.session_state.messages = []

# Initialize session messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
query = st.chat_input("Type your question here...")

if query:
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            spinner = st.spinner("Waiting for response...")
            spinner.__enter__()  # manually start spinner
            with httpx.stream("POST", API_URL, json={"query": query},timeout=300.0) as r:
                stream = r.iter_text()
                try:
                    first_chunk = next(stream)  # Get first chunk
                    full_response += first_chunk
                    message_placeholder.markdown(full_response)
                    spinner.__exit__(None, None, None)  # stop spinner after first token
                except StopIteration:
                    spinner.__exit__(None, None, None)  # no response, stop spinner
                    st.warning("No response received.")
                
                for chunk in r.iter_text():
                        full_response += chunk
                        message_placeholder.markdown(full_response)
                        spinner.__exit__(None, None, None)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

            sources = r.headers.get("X-Sources")
            if sources:
                with st.expander("📚 Source Texts Used"):
                    st.markdown(sources.replace("\\n", "\n"))

        except Exception as e:
            st.error(f"❌ Streaming failed: {e}")
