import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API token from environment variable with explicit path
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

API_TOKEN = os.getenv("HF_API_TOKEN")
if not API_TOKEN:
    st.error("HF_API_TOKEN not found in environment variables. Please check your .env file.")
    st.stop()

# App configuration
st.set_page_config(
    page_title="Career Advisor Bot",
    page_icon="💼",
    layout="centered"
)

# Custom CSS to fix UI issues and improve chat display
st.markdown("""
<style>
.main {
    padding: 2rem;
}
.user-message {
    background-color: #007bff;
    color: white;
    padding: 12px 18px;
    border-radius: 18px 18px 0 18px;
    margin: 8px 0;
    max-width: 80%;
    margin-left: auto;
    display: inline-block;
}
.bot-message {
    background-color: #f0f2f6;
    color: #1e1e1e;
    padding: 12px 18px;
    border-radius: 18px 18px 18px 0;
    margin: 8px 0;
    max-width: 80%;
    margin-right: auto;
    display: inline-block;
}
.message-container {
    width: 100%;
    display: flex;
    margin-bottom: 10px;
}
.message-container.user {
    justify-content: flex-end;
}
.message-container.bot {
    justify-content: flex-start;
}
.chat-container {
    display: flex;
    flex-direction: column-reverse;
    height: 400px;
    overflow-y: auto;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 15px;
    background-color: white;
    margin-bottom: 20px;
}
.stTextInput > div > div > input {
    padding: 12px 15px;
    border-radius: 20px;
    border: 1px solid #e0e0e0;
}
.stButton > button {
    border-radius: 20px;
    padding: 5px 20px;
}
div.row-widget.stRadio > div {
    flex-direction: row;
}
</style>
""", unsafe_allow_html=True)

# FIXED: Hugging Face API interaction with better error handling
def get_career_advice(prompt, api_token):
    API_URL = "https://api-inference.huggingface.co/models/gpt2"  # Changed to a more accessible model
    headers = {"Authorization": f"Bearer {api_token}"}
    
    career_prompt = f"""As an experienced career advisor, provide professional guidance based on industry best practices. 
Focus on actionable advice for this question: {prompt}

Consider these aspects in your response:
- Current job market trends
- Professional development opportunities
- Practical next steps
- Industry-specific insights

Response:"""
    
    payload = {
        "inputs": career_prompt,
        "parameters": {
            "max_length": 200,
            "temperature": 0.7,
            "top_p": 0.9,
            "repetition_penalty": 1.2
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
        # Check for authentication errors
        if response.status_code == 403:
            return "Authentication Error: Please check if your Hugging Face API token is valid. Make sure you've entered the correct token in the sidebar."
        
        # Check if the response is valid
        if response.status_code != 200:
            return f"API Error: Received status code {response.status_code}. Please try again later or try with a different question."
            
        # Try to parse the JSON response
        result = response.json()
        
        # Check if the response has the expected structure
        if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            generated_text = result[0]["generated_text"]
            # Extract only the response part
            if "Response:" in generated_text:
                return generated_text.split("Response:")[1].strip()
            return generated_text.replace(career_prompt, "").strip()
        else:
            # Alternative format handling
            if isinstance(result, dict) and "generated_text" in result:
                return result["generated_text"].replace(career_prompt, "").strip()
            
            # Fallback to a simple model
            return get_career_advice_alt(prompt, api_token)
            
    except Exception as e:
        print(f"Error details: {str(e)}")
        # Try alternative model on error
        return get_career_advice_alt(prompt, api_token)

# Alternative model as backup
def get_career_advice_alt(prompt, api_token):
    API_URL = "https://api-inference.huggingface.co/models/distilgpt2"  # Changed to a more accessible model
    headers = {"Authorization": f"Bearer {api_token}"}
    
    payload = {
        "inputs": f"Give me career advice about {prompt}",
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code != 200:
            return f"I'm having trouble connecting to my knowledge base. Please try again later."
            
        result = response.json()
        
        if isinstance(result, dict) and "generated_text" in result:
            return result["generated_text"]
        else:
            return "I'm currently having difficulty generating specific career advice. Please try asking in a different way."
    except Exception as e:
        return "I'm experiencing technical difficulties. Please try again in a moment."

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! I'm your Career Advisor. How can I help with your career questions today?"}
    ]

# App header
st.title("💼 Career Advisor Bot")
st.subheader("Get personalized career advice powered by AI")

# Remove the API token input from sidebar
with st.sidebar:
    st.header("About")
    st.write("This chatbot uses AI to provide career advice. The responses are generated using advanced language models.")

# Input section FIRST (reversed order)
st.markdown("### Ask Your Question")
input_placeholder = st.empty()
button_placeholder = st.empty()

# Chat display AFTER input
st.markdown("### Conversation")
chat_placeholder = st.container()

# Process new messages
user_input = input_placeholder.text_input("Type your career question here:", key="input_field")
submit_button = button_placeholder.button("Get Advice")

if submit_button and user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get bot response
    with st.spinner("Thinking..."):
        bot_response = get_career_advice(user_input, API_TOKEN)
        
    # Add bot response to history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    # Clear the input (need to rerun)
    st.experimental_rerun()

# Display messages (in correct order)
with chat_placeholder:
    for message in reversed(st.session_state.messages):
        if message["role"] == "user":
            st.markdown(f'<div class="message-container user"><div class="user-message">{message["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-container bot"><div class="bot-message">{message["content"]}</div></div>', unsafe_allow_html=True)

# Clear chat button
if st.button("Clear Chat History"):
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! I'm your Career Advisor. How can I help with your career questions today?"}
    ]
    st.experimental_rerun()