import nest_asyncio
nest_asyncio.apply()
import pickle
from langchain_community.document_loaders.sitemap import SitemapLoader

import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

import os
from langchain.docstore.document import Document
from pathlib import Path
import json
import re
from uuid import uuid4
import tiktoken
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import Dict
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage





def remove_extra_newlines(text):

    if isinstance(text, str):
        return "\n\n".join([line.strip() for line in text.splitlines() if line.strip()])
    return text 



def filter_website_content_and_save_vectorstore(remove_links : list[str], documents: Document, embeddings, faiss_folder_path: str, index_name: "db_company_website"):
    """
    Removes extra newlines characters from the page_content of each document in the list of documents.
    Filters out document objects whose metadata source link is in the remove_links list, 
    creates a FAISS vector store, and saves it locally.

    Parameters:
    - remove_links (list): A list of links to remove.
    - documents (list): A list of document objects where each object has 'page_content' and 'metadata'.
                        'metadata' is a dictionary containing a 'source' key (link to the document).
    - embeddings: The embedding model to be used for creating vector embeddings.
    - folder_path_ (str): Path to save the FAISS index locally.
    - index_name (str): The name to use when saving the FAISS index.

    Returns:
    - filtered_documents (list): A list of document objects excluding those with links in remove_links.
    """ 

    valid_documents = [
        doc for doc in documents if hasattr(doc, 'metadata') and isinstance(doc.metadata, dict)
    ]
    
    for doc in valid_documents:
        if hasattr(doc, 'page_content'):
            doc.page_content = remove_extra_newlines(doc.page_content)

    # print(documents[0])

    filtered_documents = [
        doc for doc in valid_documents
        if doc.metadata.get('source') not in remove_links
    ]
    
    len(filtered_documents)
    
    embedding_dim = len(embeddings.embed_query("hello world"))  
    index = faiss.IndexFlatL2(embedding_dim)
    
    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),  
        index_to_docstore_id={},
    )
    
    uuids = [str(uuid4()) for _ in range(len(filtered_documents))]
    faiss_folder_name = f"{faiss_folder_path}/faiss_store"
    vector_store.add_documents(documents= filtered_documents, ids=uuids)
    vector_store.save_local(folder_path= faiss_folder_name, index_name= index_name)
    print("[INFO]: Successfully saved the scrapped content into the vector_store")
    return filtered_documents, vector_store




if __name__ == "__main__":
    ###########################  Important Notes ##################################################
    # Run this script to ingest the content from the website whenever you are updating the aptus website, 
    # (d:\projects_aptus\Aptus_BOT\.conda) D:\projects_aptus\Aptus_BOT>python -m VECTOR_STORE.webscrapped_data_ingest
    # This script saves the data extracted from the aptus website into a local faiss_store from where we will load the vectors during the 
    # person's interaction with the agent in the aptus website.

    embeddings = OpenAIEmbeddings()
    sitemap_loader = SitemapLoader(web_path= "https://aptusdatalabs.com/sitemap.xml")
    docs = sitemap_loader.load()
    print(docs[0])

    with open('doc_objects.pkl', 'wb') as file:
        pickle.dump(docs, file)

    print("pickle file made!!")
    list_of_sources = []

    for doc in docs:
        list_of_sources.append(doc.metadata['source'])

    print("list of sources made!!")
    #### 
    paths_to_remove = ['https://aptusdatalabs.com/enquiry-thank-you-page/',
                       'https://aptusdatalabs.com/terms-and-conditions/',
                       'https://aptusdatalabs.com/sign-in/',
                       'https://aptusdatalabs.com/features/',
                       'https://aptusdatalabs.com/sign-up/',
                       'https://aptusdatalabs.com/get-app/', 
                       'https://aptusdatalabs.com/terms-and-conditions/',
                       'https://aptusdatalabs.com/fun-fact/', 
                       'https://aptusdatalabs.com/gallery-3-columns/', 
                       'https://aptusdatalabs.com/gallery-2-columns/', 
                       'https://aptusdatalabs.com/supply-chain-test/',
                       'https://aptusdatalabs.com/data-and-ai-accelerators/',
                       ]
    remove_links = list_of_sources[80:190]
    remove_links2 = list_of_sources[192:218]
    paths_to_remove.extend(remove_links)
    paths_to_remove.extend(remove_links2)

    
    print("length of paths to remove --> ", len(paths_to_remove))
    
    
    print("calling the function for creating vectorstore and filtering documents")
    faiss_folder_path = "./VECTOR_STORE"
    company_name = "Aptusdatalabs"
    index_name = f"db_{company_name}"
    filtered_docs, vectorstore = filter_website_content_and_save_vectorstore(paths_to_remove, docs, embeddings= embeddings,faiss_folder_path=faiss_folder_path, index_name=index_name)
    print("filtered doc", len(filtered_docs))
    print("vectorstore made!")

