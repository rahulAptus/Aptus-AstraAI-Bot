import streamlit as st
from langchain.globals import set_llm_cache

from langchain_community.cache import InMemoryCache
from pymongo import MongoClient
import datetime
from chatbot_main import agent
import time
# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # Local MongoDB instance
db = client["chatbot_db"]
collection = db["chats"]


# Custom HTML and CSS for styling the spinner


# Function to create a new chat session and store it in the database
def create_new_chat():
    session_id = str(datetime.datetime.now().timestamp())  # Unique ID for the new session
    collection.insert_one({"session_id": session_id, "messages": []})
    return session_id

# Function to get chat sessions
def get_chat_sessions():
    sessions = collection.find()
    return [(session["session_id"], len(session["messages"])) for session in sessions]

# Function to get messages for a specific session
def get_chat_messages(session_id):
    session = collection.find_one({"session_id": session_id})
    return session["messages"] if session else []

# Function to save a message to a session
def save_message(session_id, user_message, bot_message):
    collection.update_one(
        {"session_id": session_id},
        {"$push": {"messages": {"user": user_message, "bot": bot_message}}}
    )

# Custom styling using markdown and HTML
st.markdown("""
    <style>
        .title {
            font-size: 40px;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
        }
        .subtitle {
            font-size: 24px;
            color: #888;
            text-align: center;
            font-style: italic;
        }
    </style>
""", unsafe_allow_html=True)

# set_llm_cache(InMemoryCache())

# Sidebar content
st.sidebar.header("Chatbot Sessions")

# Sidebar button for creating a new chat session
new_chat_button = st.sidebar.button("New Chat")
# st.title("Aptus Buddy!")
# st.subtitle("Your AI assistant from Aptus Labs. ")
# Title and subtitle with styles
# Title and subtitle with updated professional styles
st.markdown('<div class="title">Aptus Buddy</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your AI assistant from Aptus Labs.</div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session state for sources visibility if not already set
if "show_sources" not in st.session_state:
    st.session_state.show_sources = False

with st.chat_message("assistant"):
    time.sleep(0.1)
    st.write("Hello 👋 I’m here to assist you with all your needs.")

with st.chat_message("assistant"):
    time.sleep(0.1)
    st.write("Feel free to ask me anything, and I'll provide you with accurate and helpful information.")

# Display chat messages from history on app rerun
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        if message.get("display_output_format") == "HTML":
            st.html(message.get("content"))
            if message.get("sources"):
                # Show sources as a button to reveal them
                if st.button("Show Sources", key=f"button_{message['content']}_{idx}"):
                    sources = message.get("sources")
                    for source in sources:
                        st.write(source)
                
        else:
            st.markdown(message.get("content"))
            if message.get("sources"):
                # Show sources as a button to reveal them
                if st.button("Show Sources", key=f"button_{message['content']}_{idx}"):
                    sources = message.get("sources")
                    for source in sources:
                        st.write(source)
                    
                    
                

    # # Add a small light-colored line after the user message
    # if message["role"] == "user":
    #     st.markdown("<hr style='border: 1px solid #D3D3D3;'>", unsafe_allow_html=True)

# React to user input
# Set the input limit
max_length = 200

progress_text = "Operation in progress. Please wait."


# Create a text input field
if user_query := st.chat_input("Write your query (max 200 characters):", max_chars=max_length):

    # Provide feedback to the user
    if user_query and len(user_query) == max_length:
        st.warning(f"Maximum length of {max_length} characters reached!")
        # Display user message in chat message container
        
    with st.chat_message("user"):
        st.markdown(user_query)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})
    thread_id = 110101
    set_llm_cache(InMemoryCache())
    # with st.spinner(""):
    try:
        # Create a placeholder
        with st.spinner('Wait ...'):         
            
            response = agent(user_query, thread_id)

            if response:
                # Display assistant response in chat message container
                # Handle HTML response format
                if response.get("display_output_format") == "HTML":
                    with st.chat_message("assistant"):
                        st.html(response.get("chatbot_response"))
                        st.session_state.messages.append({"role": "assistant", "content": response.get("chatbot_response"), "display_output_format": "HTML", "sources": response.get("sources", None)})
                        if "sources" in response and isinstance(response["sources"], list) and len(response["sources"])>=1:  # Check if sources list is non-empty
                            if st.button("Show Sources", key=f"button_{message['content']}"):
                                sources = message.get("sources")
                                for source in sources:
                                    st.write(source)
                        else:
                            print("Sources data type is not a list.")
                        
                # Handle Markdown response format
                else:
                    with st.chat_message("assistant"):
                        st.markdown(response.get("chatbot_response"))
                        st.session_state.messages.append({"role": "assistant", "content": response.get("chatbot_response"), "display_output_format": "Markdown", "sources": response.get("sources", None)})                       
                        # Display sources if available and not empty
                        if "sources" in response and isinstance(response["sources"], list) and len(response["sources"])>=1:  # Check if sources list is non-empty
                            if st.button("Show Sources", key=f"button_{message['content']}"):
                                sources = message.get("sources")
                                for source in sources:
                                    st.write(source)

                        else:
                            print("Sources data type is not a list.")

    except Exception as e:
        print(f"[Error]: Could not generate the answer --> chat_bot_FE ---> throws an error {e}")
        with st.chat_message("assistant"):
            response_ = "Ups, I couldn't process it! Try again 😊"
            st.markdown(response_)
            st.session_state.messages.append({"role": "assistant", "content": response_ , "display_output_format": "HTML"})

