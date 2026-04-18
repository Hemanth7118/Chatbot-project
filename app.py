import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- PAGE SETUP ---
st.set_page_config(page_title="Gemini AI Assistant", page_icon="🤖", layout="wide")

# --- INITIALIZATION & API CHECK ---
load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    st.error("API Key not found. Please check your .env file.")
    st.stop()

genai.configure(api_key=api_key)

# --- FUNCTION TO GET MODELS ---
@st.cache_resource # This prevents re-fetching every time you type
def get_available_models():
    try:
        models = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        return models
    except Exception as e:
        st.error(f"Failed to fetch models: {e}")
        return ["gemini-3-flash-preview"] # Fallback

# --- SIDEBAR: MODEL SELECTION ---
with st.sidebar:
    st.title("⚙️ Settings")
    available_models = get_available_models()
    
    # Dropdown to select the model
    selected_model_name = st.selectbox(
        "Select Model:",
        options=available_models,
        index=0 # Defaults to the first one in the list
    )
    
    st.divider()
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CHAT INTERFACE ---
st.title("🤖 My AI Chatbot")
st.caption(f"Currently talking to: **{selected_model_name}**")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT LOGIC ---
if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Initialize the model based on the sidebar selection
        model = genai.GenerativeModel(selected_model_name)
        
        try:
            # Prepare the history format for Gemini
            formatted_history = [
                {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} 
                for m in st.session_state.messages
            ]
            
            response = model.generate_content(formatted_history)
            full_response = response.text
            
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"AI Error: {e}")