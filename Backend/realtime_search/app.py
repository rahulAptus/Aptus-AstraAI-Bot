
import streamlit as st
from googleapiclient.discovery import build
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, field_validator
from sentence_transformers import util
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import os
import time
import json
import re
import asyncio
import aiohttp
import yaml
import hashlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Pydantic model for structured validation
class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str
    image: Optional[str]
    date: Optional[str]
    formatted_url: Optional[str]
    
    @field_validator("snippet", mode="before")
    def validate_relevance(cls, snippet, values):
        query = st.session_state.get("query", "")
    
        # Ensure query and snippet are valid strings
        if not isinstance(query, str) or not isinstance(snippet, str):
            raise ValueError("Query or snippet must be a valid string.")

        # Generate embeddings for the query and the snippet
        query_response = client.embeddings.create(input=query, model="text-embedding-ada-002")
        snippet_response = client.embeddings.create(input=snippet, model="text-embedding-ada-002")

        query_embedding = query_response.data[0].embedding
        snippet_embedding = snippet_response.data[0].embedding

        # Calculate cosine similarity
        similarity_score = util.cos_sim(query_embedding, snippet_embedding).item()
        
        # Set a threshold for relevance
        relevance_threshold = 0.7
        if similarity_score < relevance_threshold:
            raise ValueError("Result not relevant.")

        return snippet
    
def parse_date_from_snippet(snippet: str) -> Optional[str]:
    date_match = re.search(r"\b(\w{3,9}\s\d{1,2},\s\d{4})\b", snippet)
    if date_match:
        return date_match.group(1)  
    return None

def load_config(file_path):
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    
    return config

# Function to perform Google Custom Search
async def google_search_async(session: aiohttp.ClientSession, query: str, api_key: str, cse_id: str, num_results: int) -> List[dict]:
    service = build("customsearch", "v1", developerKey=api_key)
    loop = asyncio.get_event_loop()
    results = await loop.run_in_executor(None, lambda: service.cse().list(q=query, cx=cse_id, num=num_results).execute())
    return results.get('items', [])

def contains_aptus_data_labs(result: Dict) -> bool:
        pattern = re.compile(r"\baptus data labs\b", re.IGNORECASE)
        return bool(pattern.search(result.get("title", "")) or pattern.search(result.get("link", "")) or pattern.search(result.get("snippet", "")))

async def validate_result(result: dict) -> Optional[SearchResult]:
    """Validates and converts a search result into a `SearchResult` object."""
    try: 
        if contains_aptus_data_labs(result):
            return SearchResult(
            title=result.get("title", "No title"),
            link=result.get("link", "No link"),
            snippet=result.get("snippet", "No snippet"),
            formatted_url=result.get("formattedUrl", "No formatted URL"),
            image=result.get("pagemap", {}).get("cse_image", [{}])[0].get("src", None),
            date=parse_date_from_snippet(result.get("snippet", ""))
        )
    except ValueError:
        return None  # Skip invalid results

# Function to validate and fetch relevant search results
async def fetch_search_data(user_query: str, api_key: str, cse_id: str, sources: List[str]) -> List[SearchResult]:
    async with aiohttp.ClientSession() as session:
        # Constructing async tasks for each source query
        start_time = time.time()
        tasks = []
        
        if sources.get("linkedin", False):
            tasks.append(google_search_async(session, f"{user_query} site:linkedin.com", api_key, cse_id, 4))
        if sources.get("instagram", False):
            tasks.append(google_search_async(session, f"{user_query} site:instagram.com", api_key, cse_id, 4))
        if sources.get("facebook", False):
            tasks.append(google_search_async(session, f"{user_query} site:facebook.com", api_key, cse_id, 4))
        
        # Await the completion of all tasks concurrently
        results = await asyncio.gather(*tasks)
        
        # Flattening the list of results as we have separate results for each source
        flattened_results = [item for sublist in results for item in sublist]

        validated_results = await asyncio.gather(*(validate_result(result) for result in flattened_results))

        # Remove any None values
        validated_results = [res for res in validated_results if res]
        end_time = time.time()
        fetching_time = end_time-start_time # Time taken to fetch the results from google api

        # Convert results to JSON format
        json_data = [res.model_dump() for res in validated_results]

        # Save to a JSON file
        json_filename = "google.json"
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)

        return validated_results, fetching_time

# LangChain setup for LLM response generation
response_prompt = ChatPromptTemplate.from_messages(
    [
        (

        "system",
        "You are Aptus Search, an intelligent AI assistant designed to assist users at AptusDataLabs.com. "
        "Ensure all user queries explicitly reference 'Aptus Data Labs'. "
        "If the user asks about 'you' or 'your company', rephrase it to clearly refer to 'Aptus Data Labs'. "
        "Use this normalized query for your response."

        "Your task is to process a provided set of sources, which may include irrelevant or unrelated information. "
        "Your goal is to filter through these sources and identify and extract only the most relevant and accurate information. "
        "Use the normalized query and the content of the sources to determine relevance."

        "To fetch relevant_sources Strictly follow these rules:\n"
        "1. Do NOT include unrelated or low-relevance sources.\n"
        "2. The relevant source's link or snippet must have the word 'Aptus Data Labs' in it.\n"
        "3. Prioritize sources that are directly connected to the query and the context.\n"
        "4. Do NOT add any explanation, summary, or extra text—only return a list of URLs.\n"
        "5. Maintain consistency: The same query should always return the same set of sources."

        "If the query is not related to Aptus Data Labs, respond with 'I can only provide information about Aptus Data Labs. Please ask a relevant question.' and return Null for relevant sources.\n"

        "### Response Format:\n"
            "Respond with a JSON object that includes the following keys:\n"
            "- response: A clear and concise paragraph based on the relevant context only \n"
            "- relevant_sources: A list of URLs of the sources that were used to gather the response."
        ),
        ("user", "Question: {query}\nRelevant Sources:\n{relevant_sources}")
    ]
)



def response_chain_function(inputs: Dict) -> str:
    prompt = response_prompt.format_messages(query=inputs["query"], relevant_sources=inputs["relevant_sources"])

    start_time = time.time()

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[{"role": "system", "content": prompt[0].content}, {"role": "user", "content": prompt[1].content}]
    )

    end_time = time.time()
    time_taken = end_time - start_time

    # Output is the response from the LLM, which is a string
    output = response.choices[0].message.content
    
    
    # Clean up the string to remove 'json' and any unwanted characters
    output_cleaned = output.strip().lstrip("json").strip().lstrip("{").rstrip("}")


    # Use regular expressions to extract the response and relevant sources
    try:
        # Extract the 'response' text
        response_match = re.search(r'"response":\s*"([^"]+)"', output_cleaned)
        response_text = response_match.group(1) if response_match else None

        # Extract the 'relevant_sources' URLs
        sources_match = re.findall(r'"(https?://[^\s]+)"', output_cleaned)
        
        if response_text and sources_match:
            return response_text, sources_match, time_taken
        elif not sources_match:
            return "I can only provide information about Aptus Data Labs. Please ask a relevant question.", [], time_taken
        else:
            return "Error: Missing response or relevant sources.", [], time_taken

    except Exception as e:
        return f"Error: Failed to extract data from the LLM output. {e}", [], time_taken


def normalize_query(query: str) -> str:
    """
    Checks if 'Aptus Data Labs' is present in the query.
    If not, it prefixes 'Aptus Data Labs' to the query.
    
    Args:
        query (str): The user's input query.
    
    Returns:
        str: The normalized query.
    """

    # Case-insensitive check for 'Aptus Data Labs' in the query
    if re.search(r'\baptus data labs\b', query, re.IGNORECASE):
        return query  
    
    return f"Aptus Data Labs: {query}"  # Prefix it if not present

# Function to match URLs in search data with the LLM response
def match_sources_with_llm(search_data: List[SearchResult], response_sources: List[str]) -> List[SearchResult]:
    # Filter the search data to match only those sources that are in the LLM's response
    matched_sources = [source for source in search_data if source.link in response_sources]
    
    return matched_sources

# Main streamlit logic
async def main():
    st.set_page_config(layout="wide")
    st.title("AptBuddy")

    config_file_path = "config.yaml"
    selected_sources = load_config(config_file_path)
    
    # Input field for user query
    user_query = st.text_input("Enter your search query")
    if user_query:
        st.session_state["query"] = user_query

    if st.button("Search and Analyze"):
        if not selected_sources:
            st.error("Please select at least one data source.")
            return
        if not user_query:
            st.error("Please enter a search query.")
            return
        else:
            normalized_query = normalize_query(user_query)
            with st.spinner("Fetching search results..."):
                search_data, fetching_time = await fetch_search_data(normalized_query, API_KEY, CSE_ID, selected_sources)
                st.write(f"time taken to fetch the sources: {fetching_time}")
            
            if search_data:
                initial_context = "\n\n".join(f"Title: {item.title}\nSnippet: {item.snippet}\nLink: {item.link}\nDate: {item.date}" for item in search_data)
                with st.spinner("Generating LLM response..."):
                    response,sources,time_taken = response_chain_function({"query": normalized_query, "relevant_sources": initial_context})
            
                if "I can only provide information about Aptus Data Labs. Please ask a relevant question." in response:
                    st.write("I can only provide information about Aptus Data Labs. Please ask a relevant question.")
                else:
                    st.subheader("Response Time")
                    st.write(f"Time taken for LLM response: {time_taken:.2f} seconds")

                    
                    matched_sources = match_sources_with_llm(search_data, sources)
                    
                    # Layout adjustment: Divide screen into two sections
                    col1, col2 = st.columns([3, 2])  # Adjusted columns for a wider left side

                    # Left Column: Display matched sources and images
                    with col1:
                        st.subheader("Response")
                        st.write(response)

                        unique_images = set()
                        filtered_sources = []

                        for source in matched_sources:
                            image_url = source.image if source.image else ""
    
                            if image_url:
                                image_hash = hashlib.md5(image_url.encode()).hexdigest()  # Generate hash to remove duplicate images
                                if image_hash not in unique_images:
                                    unique_images.add(image_hash)
                                    filtered_sources.append(source)

                        
                        for source in filtered_sources:
                            if source.image and 'linkedin' in source.link:
                                st.image(source.image, width=400)

                    # Right Column: Display all sources or additional info
                    with col2:
                        with st.expander("🔍 View All Sources", expanded=False):
                            # CSS for hover effect on images
                            hover_style = """
                        <style>
                        .card {
                        border: 1px solid #e0e0e0;
                        border-radius: 8px;
                        padding: 15px;
                        margin: 10px;
                        transition: transform 0.2s;
                        cursor: pointer;
                        position: relative;
                        display: flex;
                        align-items: center;
                        }
                        .card img {
                        border-radius: 5px;
                        width: 100px;
                        height: 50px;
                        position: absolute;
                        top: 50%;
                        left: 10px;
                        transform: translateY(-50%);
                        opacity: 0;
                        transition: opacity 0.3s ease-in-out;
                        }
                        .card:hover img {
                            opacity: 1;
                        }
                        .card-content {
                        margin-left: 120px; /* Space for image */
                        }
                        </style>
                        """
                            st.markdown(hover_style, unsafe_allow_html=True)

                            DEFAULT_IMAGES = {
                            "linkedin": "https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png",
                            "instagram": "https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png",
                            "facebook": "https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg"
                            }

                            
                            
                            for source in matched_sources:
                                title = source.title
                                link = source.link
                                image_url = source.image 

                                lower_link = link.lower()
                                if "linkedin.com" in lower_link:
                                # Use actual image if valid; otherwise, use LinkedIn logo
                                    image_url = source.image if source.image else DEFAULT_IMAGES["linkedin"]
                                elif "instagram.com" in lower_link:
                                    image_url = DEFAULT_IMAGES["instagram"]
                                elif "facebook.com" in lower_link:
                                    image_url = DEFAULT_IMAGES["facebook"]

                                # Card layout for each source with clickable title and hover effect on image
                                card_content = f"""
                                <div class='card'>
                                <img src='{image_url}' alt='Image' />
                                <div>
                                    <strong>Title:</strong> <a href='{link}' target='_blank'>{title}</a>
                                </div>
                                </div>
                                """
                            
                                st.markdown(card_content, unsafe_allow_html=True)

                            if not matched_sources:
                                st.write("No sources found.")
                            

            else:
                st.write("No data found.")                
                
if __name__ == "__main__":
    asyncio.run(main())
