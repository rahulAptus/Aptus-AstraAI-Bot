
from langchain.docstore.document import Document
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Extract the list part from the string
import re
from IPython.display import Image, display, Markdown

# from config import faiss_folder
import time

from langchain_core.messages import HumanMessage 
from operator import itemgetter


from dotenv import load_dotenv

load_dotenv(override=True)



def get_faiss_files(directory: str)-> list:

    '''This function will return all the files present in the directory folder
    ending with .faiss
    '''
    faiss_files = []
    
    try:
        # Iterate through the files in the specified directory
        for file_name in os.listdir(directory):
            # Check if the file starts with db_ ends with .faiss
            # if file_name.startswith("combined_") and file_name.endswith(".faiss"):
            if file_name.endswith(".faiss"):
                faiss_files.append(file_name)
                
        print(f"[INFO]: Found the following faiss indexes in the {directory} : [{faiss_files}]")
    except FileNotFoundError:
        print(f"Error: The directory '{directory}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied to access '{directory}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return faiss_files



def extract_docs_db(faiss_folder_path: str)-> list:
    """
    This function will extract all the faiss objects representing the document chunks from my vector store ( faiss_folder_path)
    
    """
    try:
        faiss_folder = faiss_folder_path
        vector_names = get_faiss_files(faiss_folder) # Extracting all the files present in the faiss folder
        

        # Handle the case when no vector files are found
        if not vector_names:
            print("No vector files found in the specified directory.")
            error_ = "[Error]: No faiss indexes found, Please try again or check if you have stored the data into vector store.! or Check if the faiss_folder_path is correct or not"
            return   error_# Return an empty list if no vector names are found

        loaded_relevant_dbs_name = [] # List of all the vector dbs present in VECTOR_STORE/faiss_store are loaded
        embeddings = OpenAIEmbeddings()

        for filename in vector_names: 
            if filename.endswith(".faiss"):
                index_name = filename[:-6]  # Remove '.faiss' for loading
                print("Loading index: ", index_name)
                try:
                    loaded_db = FAISS.load_local(folder_path = faiss_folder, index_name=index_name, embeddings=embeddings, allow_dangerous_deserialization=True)
                    loaded_relevant_dbs_name.append(loaded_db)
                    
                except FileNotFoundError:
                    print(f"[Error]: The file '{filename}' was not found.")
                except Exception as e:
                    print(f"[Error]: An error occurred while loading '{filename}': {e}")

        return loaded_relevant_dbs_name
    
    except Exception as e:
        print(f"[Error]: Could not extract the relevant vectors from the vector store: {e}")



def query_documents_context_extraction(query: str, combined_db: list, k_doc: int = 5, score_threshold: float = 0.65):
    """
    Extracts the most relevant chunks across multiple vector databases representing each uploaded file based on a the user query in the converstation.

    This function performs similarity searches on the provided 
    document-wise databases objetcs #langchain_community.vectorstores.faiss.FAISS
    for each query in sub_queries: this function retrieves the most relevant context (documents). 
    and filters the results based on a score threshold.

    Parameters:
        user_query (str): List of the search queries to be compared against the documents.
        combined_db (list): A list of document-wise faiss object to search through.
        k_doc (int): The number of top documents to retrieve from each database.
        score_threshold (float): The minimum score required for a document to be included in the results.

    Returns:
        list: A list of tuples containing the filtered documents and their scores.
              Each tuple is in the format (document, score).
    
    Example:
        results = compare_documents("example query", [Combined_DB.faiss], 5, 0.75)
    """
    
    try:
        results = [] 
        
        for db_ in combined_db:
            retriever = db_.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={"score_threshold": score_threshold,
                                "k": k_doc}    
            )
            
            
            docs_ = retriever.invoke(query)
            # print("DOCS_:", docs_)       
            results.extend(docs_)

        # Need to include this logic for removing any duplicates if present - not a issue of concern for now

        print("[INF0]: Successfully extracted the relevant chunks for answer generation")
        
        # return docs_without_duplicates
        return results
    except Exception as e:
        print(f"[ERROR]: Error occured during the chunks retreival.\n query_documents_context_extraction \ {e} ")

# creating individual chunks 

def ASK_Question_On_Your_Documents(user_queries, document_wise_dbs, model_name: str = "gpt-4o-mini"):

    '''This function is used to generate answer to the user query from the list of vector stores representing the context data for 
    generating answer to the user query.

    db_Aptusdatalabs.faiss which contains the combined data of all content present in the aptus website.
    The reason for giving a list of vector index is that in future more sources can be added like documents, texts, etc as the 
    data source for answering the user query

    Logic:
    1- Extracting all the faiss objects and loading it to the system.
    2- Taking the user query and run similarity search on all the vector stores. For now we have only one faiss store
    3- The retrieved chunks will be sent to the llm along with the sources
    4- The llm response will be returned in a format : answer = {"chatbot_response":"", source: []}
    Note: We are extracting the response in this format so that we can show the sources too in the response generated.

    Parameters:
    - user_query (str): The user query in the UI
    - document_wise_dbs: All the vector indexes found in the faiss folder
    - model_name: GPT Model to be used like gpt-3.5-turbo
    
    Returns:
    - Response (dict): The answer generated by the llm to the user query after taking the context. Format= {"chatbot_response":"", source: []}
 
    '''

     # Time calculation
    start_time = time.time()
    docs_ = query_documents_context_extraction(user_queries, document_wise_dbs, score_threshold=0.65) #extracting the relevant chunks to the query
    

    # Calling the llm for analysis
    # Post vector loading anc hunks extraction
    if not docs_:
        return "Sorry, I couldn't find any relevant information related to your query. Kindly contact the Aptus team!"
    else:
        print(f"[INFO]: No of chunks extracted: {len(docs_)}") 
        try:
            llm = ChatOpenAI(model = model_name)
            sources = []
            context_ = """ """
            for doc in docs_:
                # Adding only the page content into the context 
                sources.append(doc.metadata['source'])
                context_ += f"source:{doc.metadata['source']} {doc.page_content} \n\n"
            

            instructions = """ Provide a concise response to the user's query based solely on the information available about Aptus Data Labs given as context.
                             Avoid answering questions that fall outside this scope, keeping in mind that your knowledge is limited to Aptus Data Labs."""

            final_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You are Aptus Buddy, a virtual assistant on the Aptus website who talks in English only.
                           Your job is to provide short and clear answers to users. You can give more details if asked, but keep responses brief.
                           Always use Markdown to format your answers."""
                    ),
                    ("human", f"{instructions}"),    
                    ("human", f"{user_queries}"),                                 
                    ("human", "information: {input}"),
                ]
            )
            
            print("[INFO]: Generating answer to the given query.")

            chain = {"input": itemgetter("input")} | final_prompt | llm | StrOutputParser()

            ans = chain.invoke({"input": context_.strip()})
            # display(Markdown(ans))
            ans = {"chatbot_response":ans, "sources":sources, "user_query": user_queries,"display_output_format": "Markdown"}
            return ans
        
        except Exception as e:
            print("[ERROR]: Could not Generate answer to this question")
            return {"chatbot_response":f"<p style='color: red; font-weight: bold;'>I don't have answer to this question, Kindly ask again!</p>", "sources":[],
                    "user_query": user_queries, "display_output_format": "Markdown"}
        
   
# if __name__ == "__main__":
#     faiss_folder_path = "./VECTOR_STORE/faiss_store"
#     trigger = True
#     if trigger == True:
#         # Loading the vectors in the environment
#         document_wise_dbs = extract_docs_db(faiss_folder_path)
#         print("[INFO]: Successfully loaded the vector store in the system")

#         user_query = "Tell me about India and raghav magotra"
#         ans =  ASK_Question_On_Your_Documents(user_query, document_wise_dbs, "gpt-4o") 
#         print(ans)
