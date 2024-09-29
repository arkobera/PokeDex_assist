import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Set the path to your background image
background_img = r'C:\Users\91991\Desktop\Gemini\pokemon.jpg'  # Use raw string to handle backslashes

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Add CSS to set the background image
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url({background_img});
        background-size: cover;  /* Cover the entire screen */
        background-repeat: no-repeat;
        background-position: center;  /* Center the image */
        height: 100vh;  /* Full height */
        color: white;  /* Optional: change text color for contrast */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Display the chatbot's title on the page
st.title("🤖 PokeDex")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini-Pro's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
