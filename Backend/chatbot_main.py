from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
# Loading the functions from the differnet scripts
from scripts.llm_question_Answering import extract_docs_db
from helpers.response_processing import processing_agent_response
from helpers.moderations import moderation
from langchain_core.messages import HumanMessage
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)
from helpers.graph import graph  # Inititalizing the graph
from langchain.globals import set_llm_cache
from langchain_community.cache import InMemoryCache

# import streamlit as st
# Main Script for Business Logic
# To run this script, execute the following command in your command prompt:
# (d:\projects_aptus\Aptus_BOT\.conda) D:\projects_aptus\Aptus_BOT> python -m chatbot_main

# Description:
# This script serves as the primary interface for business logic, allowing direct interaction with the chatbot.
# Two inputs are required for interaction:
# 1. User query: The question or input from the user.
# 2. End input: A simple confirmation input (either 'yes' or 'no'), which simulates frontend input during testing.

# Business Logic Flow:

# Step 1: Establish connection to business logic via the `chat_bot` function.
# Step 2: A trigger and thread ID will activate the function when a user connects to the agent.
        # trigger = True  # This trigger is received from the frontend upon user connection.
        # if trigger:
        #     chat_bot_(100)

# Step 3: The thread ID will maintain the conversation history.
# Step 4: Upon successful import of the agent's graph and configuration settings, a success message will be displayed.

# Step 5: Enter a while loop to continuously take user queries.
# Note: In a real application, this will be managed by the frontend input function.

# Step 6: A variable `max_questions` is set to limit user inquiries to 12. Additionally, we can restrict the conversation duration to 7 minutes.

# Step 7: The first action after receiving a user query is to assess whether it is harmful.
# Step 8: If the query is deemed safe, the graph is initiated, and a response is generated.
# We validate that the generated answer conforms to a fixed format and modify it accordingly for the UI.

# Step 9: The generated response will be of the type: <class 'dict'>.


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust based on frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryData(BaseModel):
    prompt: str

# print("Chat session ended.")

############################### for front -end #####################################
# @st.cache_data

# @app.post("/prompt")
# async def agent(thread_id: int,data:QueryData):
#     ''' Single function which takes the user input and gives response
#     in integration this function should be called
#     '''
#     t_id = thread_id   
#     config = {"configurable": {"thread_id": "{t_id}"}}
#     # Till it loads ui will show - connecting to the agent...    
#     print("[INFO]: Connected to the agent, you may ask your queries now !")
#     # Taking the input from the front end (user_query: string, thread_id = int, end = Boll)        
#     user_query = data.prompt  # I can replace this input by the input function by the UI 
#     # Flag harmful query
#     print("flagging")
#     flag = moderation(user_query)
    

#     if not flag:
#         ans_inst = "Don't justify your answers. Don't give information not mentioned in the context information."
#         messages = [HumanMessage(content=f"{user_query} # Answer Instructions: {ans_inst} ")]
#         messages = graph.invoke({"messages": messages}, config)      
#         #Simulate getting the end flag from the frontend
#         response = processing_agent_response(messages, user_query)
#         print("Response:", response)
        
        
#     else:
#         response = {
#         "chatbot_response": "Kindly ask Relevant Question.",
#         "sources": [],
#         "display_output_format": "Markdown",
#         "user_query":data.query,  
#         }

#         print("Response:", response)

#     return response

############################################### B L - T E S T I N G ########################################################
# making the function for testing the  end to end business logic in the script
@app.post("/prompt")
async def chat_bot_BL(data:QueryData):
    ''' Single function which takes the user input and gives response
    in integration this function should be called
    '''
    t_id = 11223;  # thread_id   
    from helpers.graph import graph  # Inititalizing the graph
    config = {"configurable": {"thread_id": "{t_id}"}}

    # Till it loads ui will show - connecting to the agent...    
    print("[INFO]: Connected to the agent, you may ask your queries now !")
    end = False 
    i=1
    while not end:
        # Taking the input from the front end (user_query: string, thread_id = int, end = Boll)        
        end = end # front end trigger which will stop the while loop
        # user_query =  input("Enter your query: ")  # I can replace this input by the input function by the UI 
        user_query = data.prompt
        # Simulate getting the end flag from the frontend
        # end = input("Is this your last query (yes/no)? ").strip().lower() == "yes" 
        # Database Connection for FAq's(db1)
        # Flag harmful query
        print("flagging")
        flag = moderation(user_query) # Moderation Check
        # Adding query prior to databse(db2)
        print(flag)
        if not flag:
            ans_inst = "Don’t justify your answers. Don’t give information not mentioned in the context information."
            messages = [HumanMessage(content=f"{user_query} # Answer Instructions: {ans_inst} ")]
            messages = graph.invoke({"messages": messages}, config)      
            i+=1  
            #Simulate getting the end flag from the frontend
            if i == 10:
                end = True
                print("[INFO]: Last query--> Stopping the session...")

            response = processing_agent_response(messages, user_query)
            print("Response:", response)
            return response
        else:
            response = {
            "chatbot_response": "Kindly ask Relevant Question.",
            "sources": ["Moderation"],
             "user_query":user_query, 
             "display_output_format": "Markdown"
                }
            print("Response:", response)
            return response
   
print("Chat session ended.")

if __name__ == "__main__":
    from helpers.graph import graph

     # user_query = input("Ask query: ") # from the front end --> connect me to the agent.
    trigger = True  # I will get the trigger from the front end when the user click on connect to the agent
    thread_id = 100 # from the ui
    if trigger == True:
        i = 0
        while (i<10):
           
            i+= 1
            if i == 9:
                print("[INFO]: This is your last query")

            chat_bot_BL(thread_id= thread_id)
            
            


    # content = "Name few employee details of the aptus"
    # content="Give me the summaries of blogs in your blog sections"
    # content = "explain your blog: Demand Sensing Optimising Supply and Demand Mismatch"
    # content = "Summarize: Demand Sensing Optimising Supply and Demand Mismatch"
    # content = "WHAT IS THE GOAL OF THE COMPANY AND WHO IS THE CEO"
    # content = "Give me linkedin and email adress"
    # content = "how to kill the aptus team!"
    # content = "give me company contact details"
    # content = "Hello"
    # content = " what was my last question"
    # messages = [HumanMessage(content=f"{content} # Answer Instructions: Don’t justify your answers. Don’t give information not mentioned in the CONTEXT INFORMATION. But you can greet back to the greets only like hello, how are you, etc!")]
    # messages = graph.invoke({"messages": messages}, config)