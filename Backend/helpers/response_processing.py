# This function cleans and post-process the agent response in the format: 
# {  "chatbot_response": messages['messages'][-1].content,
            # "sources": ["LLM"],
            # "user_query": user_queries,"display_output_format": "Markdown"
        # }

import json
def processing_agent_response(messages: list, query: str):
    try:
        # Attempt to load the content as JSON
        ans = json.loads(messages['messages'][-1].content) if isinstance(messages['messages'][-1].content, str) else messages['messages'][-1].content
        return ans
    
    except (json.JSONDecodeError, SyntaxError):
        # If there's a syntax error, construct the fallback dictionary
        # print(f"An unexpected error occurred: {SyntaxError} | {json.JSONDecodeError}")
        ans = {
            "chatbot_response": messages['messages'][-1].content,
            "sources": [],
            "user_query":query, 
            "display_output_format": "Markdown"
        }

        return ans
    
    except Exception as e:
        # Catch any other exception and display it for debugging
        print(f"An unexpected error occurred: {e}")
        ans = {
            "chatbot_response": f"<p style='color: red; font-weight: bold;'> An error occurred while processing the response, Kindly ask again!</p>",            
            "sources": [],
            "user_query":query, 
            "display_output_format": "Markdown"
        }
        return ans