# Loading the functions from the differnet scripts
from langchain.globals import set_llm_cache
from helpers.tools import ASK_Question_On_Your_Documents_, company_contact_details, aptus_data_labs_introduction, schedule_appointment
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from IPython.display import Image, display, Markdown
from langchain_openai import OpenAIEmbeddings
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import RemoveMessage

# Defining the LLM to be used for bot interactions
# Sources : https://github.com/langchain-ai/langchain-academy/blob/main/module-2/trim-filter-messages.ipynb - trimming of the messages
#           https://github.com/langchain-ai/langchain-academy/tree/main/ - Understanding of the langgraph



def filter_messages(state: MessagesState):
    '''This function is used for trimm the messages in the chat history   
    This function needs to be updated as it is throwing an error:    
    Error code: 400 - {'error': {'message': "Invalid parameter: messages with role 'tool' must be a response to a 
    preceeding message with 'tool_calls'.", 'type': 'invalid_request_error', 'param': 'messages.[1].role', 'code': None}}
    This error means am sending a message list where a message doesn't have a user_query probably because of the direct trimming.
    '''

    
    # Delete all but the 3 most recent messages pair
    filtered_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-6]]
    return {"messages": filtered_messages}

def filter_messages2(state: MessagesState):
    '''This function is used for trimmer the messages in the chat history   
    This function needs to be updated as it is throwing an error:    
    Error code: 400 - {'error': {'message': "Invalid parameter: messages with role 'tool' must be a response to a 
    preceeding message with 'tool_calls'.", 'type': 'invalid_request_error', 'param': 'messages.[1].role', 'code': None}}
    This error means am sending a message list where a message doesn't have a user_query probably because of the direct trimming.
    '''


    messages = state["messages"]
    filtered_messages = []
    human_message_count = 0

    for message in reversed(messages):
        filtered_messages.append(message)

        if isinstance(message, HumanMessage):
            human_message_count += 1
        if human_message_count == 3:
            break

    filtered_messages.reverse()

    # print(f"Filtered messages (at least 3 pairs): {filtered_messages}")
    return {"messages": filtered_messages}

# Here we are setting the model to be used for the interaction with the user.   
# Note: This llm is different from the llm used in the tools

key = os.getenv(key="OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=4)

# System message
sys_msg = SystemMessage(content="You are a helpful AI assistant named: Aptus Buddy at Aptus's website and a part of Aptus. Only English langauge is acceptable.")


# Node
tools = [ASK_Question_On_Your_Documents_,company_contact_details,aptus_data_labs_introduction, schedule_appointment]
llm_with_tools = llm.bind_tools(tools)

# Node
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


############# New graph ##############################




# Build graph
builder = StateGraph(MessagesState)
builder.add_node("filter", filter_messages2)
builder.add_node("Assistant", tool_calling_llm)
builder.add_node("tools", ToolNode([ASK_Question_On_Your_Documents_,company_contact_details,aptus_data_labs_introduction,schedule_appointment]))
builder.add_edge(START, "filter")
builder.add_edge("filter", "Assistant")
builder.add_conditional_edges(
    "Assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", END)
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)


# View
# display(Image(graph.get_graph().draw_mermaid_png()))



################---------------THIS WAS MY OLD GRAPHG STRUCTURE -----------------#######################
# # Build graph
# builder = StateGraph(MessagesState)
# builder.add_node("Assistant", tool_calling_llm)
# builder.add_node("tools", ToolNode([ASK_Question_On_Your_Documents_,company_contact_details]))
# builder.add_edge(START, "Assistant")
# builder.add_conditional_edges(
#     "Assistant",
#     # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
#     # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
#     tools_condition,
# )
# builder.add_edge("tools", END)
# memory = MemorySaver()
# graph = builder.compile(checkpointer=memory)
# # View
# display(Image(graph.get_graph().draw_mermaid_png()))

# I will be sending this graph object to the main script for interaction
