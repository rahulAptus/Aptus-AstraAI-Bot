# We have a store of all the tools which will be integrated in the chatbot

from scripts.llm_question_Answering import extract_docs_db
from scripts.llm_question_Answering import ASK_Question_On_Your_Documents
# from constants import contact_widget2
from helpers.constants import contact_widget1


from langchain_core.tools import tool

# Loading the vectors in the environment
faiss_folder_path = "./VECTOR_STORE/faiss_store"
if faiss_folder_path:
    print("[INFO]: Successfully loaded the vector store in the system")
try:
    document_wise_dbs = extract_docs_db(faiss_folder_path)
except Exception as e:
    print(f"[Error]: Could not load the document vectors, {e}")





def ASK_Question_On_Your_Documents_(user_query: str):
    """ 
    This function provides an answer to the user's query based on the company's data documents.    
    It is designed to be used when the user asks a general question related to the company's data or information, 
    except for inquiries about contacting the company directly or basic introduction about aptus or comapny.
  
    """
    global document_wise_dbs
    print("[INFO]: User Query:", user_query)
    print(f"[INFO]: --> Tool call --> ASK_Question_On_Your_Documents_ running...")
    ans = ASK_Question_On_Your_Documents(user_queries= user_query, document_wise_dbs=document_wise_dbs, model_name= "gpt-4o-mini")
        # answer is in the format  {"chatbot_response":ans, "sources":sources, "user_query":query,  "display_output_format": "Markdown"}
    return ans



def aptus_data_labs_introduction(user_query: str):

    """ 
    This function provides responses to user queries specifically about Aptus Data Labs, 
    including questions related to the company's introduction or general information about what Aptus Data Labs is or summary of aptus .
    
    **Always use this function when the user asks about the company's introduction or seeks information about what Aptus Data Labs is, 
    its mission, services, or general background.
    Notes:
        - The function is intended for answering questions like "What is Aptus Data Labs?" or "Tell me about Aptus Data Labs." or " Essay on Aptus" , "Aptus data labs" , "Aptus background", etc
        - The response can include the company's mission, vision, services, history, or other introductory details.
    """
        
    print("[INFO]: User Query:", user_query)
    print(f"[INFO]: --> Tool call --> aptus_data_labs_introduction running...")

    return {'chatbot_response': ' The *Aptus Data Labs* specializes in tailored Data Science and AI solutions, transforming data into actionable insights to enhance business outcomes. They offer services in advisory, data engineering, artificial intelligence, and cloud solutions, among others. Their platforms include AptPlan.ai for supply chain planning, AptCheck for documentation evaluation, Aptveri5 for auditing, AptSpend for expense tracking, and AptGenAI for generative AI solutions. Located in Bengaluru, India, Aptus is committed to security and ongoing support for its clients.', 'sources': ['https://aptusdatalabs.com/maximizing-customer-value-for-customer-segmentation-and-lifetime-value-prediction/', 'https://aptusdatalabs.com/cash-flow-projections-for-a-consumer-financing-and-loan-servicing-company-in-the-usa/', 'https://aptusdatalabs.com/career/', 'https://aptusdatalabs.com/microsoft-azure/', 'https://aptusdatalabs.com/amazon-web-services/'], 'user_query': 'Tell me about Aptus.', 'display_output_format': 'Markdown'}

def company_contact_details(query: str):
    """ 
    This function gives contact details of the company 
    If input query is about company's contact details then always use this function.

    """
    print(f"[INFO]: --> Tool call --> company_contact_details running...")
    text_ = contact_widget1
    ans = {"chatbot_response":text_ ,"sources":["https://aptusdatalabs.com/contact-us/"], "user_query":query,  "display_output_format": "HTML"}
    return ans



# ans = ASK_Question_On_Your_Documents_("TELL ME ABOUT APTUS")
# print(ans)
