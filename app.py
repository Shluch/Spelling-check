import streamlit as st
import openai
from hugchat import hugchat
from hugchat.login import Login

# Initialize HugChat and log in
def initialize_hugchat(email, password):
    cookie_path_dir = "./cookies/"
    try:
        sign = Login(email, password)
        cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        return chatbot
    except Exception as e:
        st.error(f"Login failed: {str(e)}")
        return None

# Function to interact with OpenAI GPT-3.5 API
def get_openai_response(prompt, api_key):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Agent functions
def motivate_agent(api_key, user_query):
    prompt = f"Provide a motivational response to: {user_query}"
    return get_openai_response(prompt, api_key)

def depression_help_agent(api_key, user_query):
    prompt = f"Provide supportive advice for managing depression for the query: {user_query}"
    return get_openai_response(prompt, api_key)

# HugChat agent functions
def motivate_agent_hugchat(chatbot, user_query):
    prompt = f"Provide a motivational response to: {user_query}"
    return chatbot.chat(prompt)

def depression_help_agent_hugchat(chatbot, user_query):
    prompt = f"Provide supportive advice for managing depression for the query: {user_query}"
    return chatbot.chat(prompt)

# Streamlit app
st.title("Multi-Agent AI Assistant 🤖")

st.header("Welcome to the Multi-Agent AI Assistant!")
st.write("Please enter your OpenAI API key, Hugging Face email and password, and your query below.")

# Input fields
api_key = st.text_input("OpenAI API Key", type="password")
email = st.text_input("Hugging Face Email")
password = st.text_input("Hugging Face Password", type="password")
user_query = st.text_area("Your Query (Motivation or Help for Depression)")

# Initialize HugChat chatbot
chatbot = None
if email and password:
    chatbot = initialize_hugchat(email, password)

# Process the query with different agents
if st.button("Submit"):
    if api_key and user_query:
        st.subheader("Motivation Agent Response (OpenAI):")
        motivation_response = motivate_agent(api_key, user_query)
        st.write(motivation_response)
        
        st.subheader("Depression Help Agent Response (OpenAI):")
        depression_help_response = depression_help_agent(api_key, user_query)
        st.write(depression_help_response)

        if chatbot:
            st.subheader("Motivation Agent Response (HugChat):")
            motivation_response_hugchat = motivate_agent_hugchat(chatbot, user_query)
            st.write(motivation_response_hugchat)
            
            st.subheader("Depression Help Agent Response (HugChat):")
            depression_help_response_hugchat = depression_help_agent_hugchat(chatbot, user_query)
            st.write(depression_help_response_hugchat)
    else:
        st.error("Please enter the OpenAI API key, Hugging Face credentials, and a query.")
