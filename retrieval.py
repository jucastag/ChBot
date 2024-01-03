#from shared.util import get_secret, get_aoai_config
#from tenacity import retry, wait_random_exponential, stop_after_attempt
from dotenv import load_dotenv
import json
import logging
import openai
import os
import requests
import time

load_dotenv()

# Azure OpenAI Integration Settings
AZURE_OPENAI_EMBEDDING_MODEL = os.environ.get("AZURE_OPENAI_EMBEDDING_MODEL")

TERM_SEARCH_APPROACH='term'
VECTOR_SEARCH_APPROACH='vector'
HYBRID_SEARCH_APPROACH='hybrid'
AZURE_SEARCH_USE_SEMANTIC=os.environ.get("AZURE_SEARCH_USE_SEMANTIC")  or "false"
AZURE_SEARCH_APPROACH=os.environ.get("AZURE_SEARCH_APPROACH") or VECTOR_SEARCH_APPROACH

AZURE_SEARCH_SERVICE = os.environ.get("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX")
AZURE_SEARCH_API_VERSION = os.environ.get("AZURE_SEARCH_API_VERSION")
AZURE_SEARCH_SERVICE_KEY = os.environ.get("AZURE_SEARCH_SERVICE_KEY")
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

AZURE_SEARCH_OYD_USE_SEMANTIC_SEARCH = os.environ.get("AZURE_SEARCH_OYD_USE_SEMANTIC_SEARCH") or "false"
AZURE_SEARCH_OYD_USE_SEMANTIC_SEARCH = True if AZURE_SEARCH_OYD_USE_SEMANTIC_SEARCH == "true" else False
AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG = os.environ.get("AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG") or "my-semantic-config"
AZURE_SEARCH_SEMANTIC_SEARCH_LANGUAGE = os.environ.get("AZURE_SEARCH_SEMANTIC_SEARCH_LANGUAGE") or "en-US"
AZURE_SEARCH_ENABLE_IN_DOMAIN = os.environ.get("AZURE_SEARCH_ENABLE_IN_DOMAIN") or "true"
AZURE_SEARCH_ENABLE_IN_DOMAIN =  True if AZURE_SEARCH_ENABLE_IN_DOMAIN == "true" else False


#FILTER_QUERY = os.environ.get("FILTER_QUERY", "")
AZURE_SEARCH_TOP_K = os.environ.get("AZURE_SEARCH_CONTENT_COLUMNS") or "3"

def generate_embeddings(text):

    openai.api_type = "azure"
    openai.api_base = os.environ.get("OPENAI_API_BASE")
    openai.api_version = os.environ.get("OPENAI_API_VERSION")
    openai.api_key =  os.environ.get("OPENAI_API_KEY")

    response = openai.Embedding.create(
        input=text, engine=AZURE_OPENAI_EMBEDDING_DEPLOYMENT)
    embeddings = response['data'][0]['embedding']
    return embeddings

def retrieve_documents(input: str) -> str:
    search_results = []
    search_query = input
    try:
        filterQuery = "(performance_and_speed eq 'Medium') and (camera_quality eq 'Medium') and (display_quality eq 'High')"
        start_time = time.time()
        embeddings_query = generate_embeddings(search_query)
        response_time =  round(time.time() - start_time,2)
        logging.info(f"[function_retrieval] querying azure ai search. search query: {search_query}")

        # prepare body
        body = {
            "select": "modelo,marca,pantalla,resolucion_pantalla,procesador,memoria_ram,almacenamiento,camara_principal,camara_frontal,sistema_operativo,bateria,performance_and_speed,camera_quality,display_quality",
            "filter": filterQuery,
            "top": int(AZURE_SEARCH_TOP_K)
        }    
        if AZURE_SEARCH_APPROACH == TERM_SEARCH_APPROACH:
            body["search"] = search_query
        elif AZURE_SEARCH_APPROACH == VECTOR_SEARCH_APPROACH:
            body["vector"] = {
                "value": embeddings_query,
                "fields": "contentVector",
                "k": int(AZURE_SEARCH_TOP_K)
            }
        elif AZURE_SEARCH_APPROACH == HYBRID_SEARCH_APPROACH:
            body["search"] = search_query
            body["vector"] = {
                "value": embeddings_query,
                "fields": "contentVector",
                "k": int(AZURE_SEARCH_TOP_K)
            }
        if AZURE_SEARCH_USE_SEMANTIC == "true" and AZURE_SEARCH_APPROACH != VECTOR_SEARCH_APPROACH:
            body["queryType"] = "semantic"
            body["semanticConfiguration"] = AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG
            body["queryLanguage"] = AZURE_SEARCH_SEMANTIC_SEARCH_LANGUAGE

        headers = {
            'Content-Type': 'application/json',
            'api-key': AZURE_SEARCH_SERVICE_KEY
        }
        search_endpoint = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net/indexes/{AZURE_SEARCH_INDEX}/docs/search?api-version={AZURE_SEARCH_API_VERSION}"
                
        start_time = time.time()
        response = requests.post(search_endpoint, headers=headers, json=body)
        status_code = response.status_code
        if status_code >= 400:
            error_on_search = True
            error_message = f'Status code: {status_code}.'
            if response.text != "": error_message += f" Error: {response.text}."
            logging.error(f"[function_retrieval] error {status_code} when searching documents. {error_message}")
        else:
            if response.json()['value']:
                for doc in response.json()['value']:
                    phone_info = [f"{key}: {value}" for key, value in doc.items()]
                    phone_block = "\n".join(phone_info)
                    search_results.append(phone_block)

            # Return the concatenated key-value pairs for each phone
            return "\n".join(search_results)  
                        
        response_time =  round(time.time() - start_time,2)
        
        logging.info(f"[function_retrieval] searched documents. {response_time} seconds")
    except Exception as e:
        error_message = str(e)
        logging.error(f"[function_retrieval] error when getting the answer {error_message}")
        
    sources = ' '.join(search_results)
    logging.error(f"[function_retrieval] Sources {sources}")
    return sources
    response_data = {"sources": sources}
    return json.dumps(response_data)