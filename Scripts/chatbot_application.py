import gradio as gr
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from gpt4all import GPT4All
import requests
import logging
from functools import lru_cache
from fuzzywuzzy import fuzz

@lru_cache(maxsize=100)
def cached_generate_response(prompt, mode="Detailed"):
    return generate_response(prompt, mode)


# Set up logging
logging.basicConfig(filename='query_logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load the embedding model
embedder = SentenceTransformer('all-MiniLM-L12-v2')  # Or any larger SentenceTransformer model

# Connect to Qdrant
qdrant_client = QdrantClient(host="localhost", port=6333)

# Load the GPT4All model
model_path = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"  # Update this path if needed
gpt4all_model = GPT4All(model_path)

collection_name = "network_security_knowledge"

SERPAPI_API_KEY = " "

relevance_threshold = 0.6 #choose relevance threshold to improve the output


def find_relevant_document(prompt):
    question_embedding = embedder.encode([prompt])[0]

    search_results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=question_embedding.tolist(),
        limit=10
    )

    relevant_pages = []
    for hit in search_results:
        payload = hit.payload
        score = fuzz.partial_ratio(prompt.lower(), payload["text"].lower())
        if score > 60:  # Adjust threshold for fuzzy matching
            relevant_pages.append({
                "document_name": payload["document"],
                "page_number": payload["page_number"],
                "reference": payload["text"]
            })

    return relevant_pages


def web_search(query):
    """Perform a web search using SerpAPI."""
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "engine": "google",
        "num" : 3
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        search_results = response.json().get('organic_results', [])
        # Extract the title and snippet from the search results
        message = ""
        for result in search_results:
            message +=f"{result['title']}-[URL:{result['link']}]\n"
            data = f"{result['snippet']}\n"
        return [data,message]
    else:
        print("Error with web search API:", response.status_code)
        return ["Internet Search Failure.","Error"]


def generate_response(prompt, mode="Concise"):
    relevant_pages = find_relevant_document(prompt)
    
    if relevant_pages:
        context_prompt = f"Answer the following question '{prompt}'\n\n from the below Context:\n"
        for i in relevant_pages:
            context_prompt += f"{i['reference']}\n\n"
        response = gpt4all_model.generate(context_prompt).strip()
        if mode == "Concise":
            response = response.split('\n')[0]  # Return only the first line
        source = "\n".join([f"Document: {page['document_name']}, Page: {page['page_number']}" for page in relevant_pages])
        
        #response += "\n\nReferences:\n" + "\n".join([f"[{index + 1}] {page['document_name']}, Page {page['page_number']}" for index, page in enumerate(relevant_pages)])
    else:
        source = "No relevant information found in the documents, Searching from Internet\n"
        resp1 = web_search(prompt)
        response = resp1[0]
        if mode == "Concise":
            response = response.split('\n')[0]  # Return only the first line
        source += resp1[1]

    return response, source

iface = gr.Interface(
    fn=lambda prompt, mode: cached_generate_response(prompt, mode),
    inputs=[gr.Textbox(label="Enter your Query?", lines=5), gr.Dropdown(["Concise", "Detailed"], label="Response Mode")],
    outputs=[gr.Textbox(label="Chatbot response", lines=30), gr.Textbox(label="Sources", lines=10)],
    title="On-Demand Professor Q&A Chatbot"
)


iface.launch()

