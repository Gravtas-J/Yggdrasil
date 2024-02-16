
import streamlit as st
from dotenv import load_dotenv
import os
import openai
from time import time
from dotenv import load_dotenv
from PIL import Image
from datetime import datetime, timedelta
import time
import random

def ensure_userprofile_exists(filepath):
    # Check if the file exists
    if not os.path.exists(filepath):
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # Create the file since it doesn't exist
        with open(filepath, 'w', encoding='utf-8') as f:
            # You can initialize the file with default content if necessary
            f.write('')  # Write an empty string or initial content
        

        

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()
    
def chatbotGPT4(conversation, model="gpt-4", temperature=0, max_tokens=4000):
    response = openai.ChatCompletion.create(model=model, messages=conversation, temperature=temperature, max_tokens=max_tokens)
    text = response['choices'][0]['message']['content']
    return text, response['usage']['total_tokens']


def chatbotGPT3(conversation, model="gpt-3.5-turbo-0125", temperature=0, max_tokens=4000):
    response = openai.ChatCompletion.create(model=model, messages=conversation, temperature=temperature, max_tokens=max_tokens)
    text = response['choices'][0]['message']['content']
    return text, response['usage']['total_tokens']

# Streamed response emulator for a dynamic chat experience
def response_generator(msg_content):
    for word in msg_content.split():
        yield word + " "
        time.sleep(0.1)

def append_to_chatlog(message):
    # Check if the chatlog file exists, create it if it doesn't
    try:
        open("chatlog.txt", "r").close()
    except FileNotFoundError:
        open("chatlog.txt", "w").close()
    
    with open("chatlog.txt", "a") as chatlog_file:
        chatlog_file.write(message + "\n")
#=================================================================#

load_dotenv()

ensure_userprofile_exists(os.path.join('Memories', 'user_profile.txt'))
openai.api_key = os.getenv("OPENAI_API_KEY")
Update_user = os.path.join('system prompts', 'User_update.md')
# mem_long=os.path.join('System_prompts', 'system_01_intake.md')
# mem_recall=os.path.join('System_prompts', 'System_02_Risk.md')
Persona=os.path.join('Personas', 'persona.md')
userprofile=os.path.join('Memories', 'user_profile.txt')
portrait_path = os.path.join('Portrait', 'Emily.png')
prompt = st.chat_input()
Profile_update = open_file(Update_user)
persona_content = open_file(Persona)
User_pro = open_file(userprofile)
Content = persona_content + User_pro
Profile_check = Profile_update+User_pro

#=================================================================#


if st.sidebar.button("Clear History"):
    # Reset the messages list and chat_log string
    st.session_state['messages'] = []
    st.session_state["chat_log"] = ""
    st.rerun()  # Rerun the app to reflect changes
# Initialize or ensure the 'messages' list is in the session state for storing chat messages.
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if "chat_log" not in st.session_state:
    st.session_state["chat_log"] = ""
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        # For assistant messages, use the custom avatar
        with st.chat_message("assistant", avatar=portrait_path):
            st.write(msg["content"])
    else:
        # For user messages, display as usual
        with st.chat_message(msg["role"]):
            st.write(msg["content"])


if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user",):
        st.write(prompt)

    # Prepare the list of messages to send to the API, starting with the system prompt for context,
    # followed by the actual chat messages exchanged in the session.
    system_prompt = {
        "role": "system",
        "content": Content  
    }
    messages_for_api = [system_prompt] + st.session_state.messages
    
    # Call the OpenAI API with the prepared messages, including the hidden system prompt.
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=messages_for_api
    )
    msg_content = response.choices[0].message["content"]
    
    # Display assistant response in chat message container with streamed output
    with st.chat_message("assistant", avatar=portrait_path):
        st.write_stream(response_generator(msg_content))
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": msg_content, })


        # Convert the chat log into a string, store it in the session state.
    chat_log = "<<BEGIN CHATLOG>>" +"\n".join([f"{msg['role'].title()}: {msg['content']}" for msg in st.session_state.messages])+ "<<END CHATLOG>>"
    st.session_state['chat_log'] = chat_log
    
    Update_user_profile = [{'role': 'system', 'content': Profile_check}, {'role': 'user', 'content': st.session_state.get('chat_log', '')}]
    User_profile_updated, tokens_risk = chatbotGPT4(Update_user_profile)   
    with open(userprofile, "w") as file:
        file.write(User_profile_updated)

    # Append the latest user and assistant messages to the chatlog file
    append_to_chatlog(f"User: {prompt}")
    append_to_chatlog(f"Assistant: {msg_content}")
