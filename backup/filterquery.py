import json
import openai
import logging
import os
from dotenv import load_dotenv
from shared.util import call_semantic_function

load_dotenv()

import semantic_kernel as sk
import semantic_kernel.connectors.ai.open_ai as sk_oai
from semantic_kernel.connectors.ai.open_ai.semantic_functions.open_ai_chat_prompt_template import (
    OpenAIChatPromptTemplate,
)
from semantic_kernel.connectors.ai.open_ai.utils import (
    chat_completion_with_function_call,
    get_function_calling_object,
)

# logging level

logging.getLogger('azure').setLevel(logging.WARNING)
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)
myLogger = logging.getLogger(__name__)

# Env Variables
AZURE_OPENAI_CHATGPT_MODEL = os.environ.get("AZURE_OPENAI_CHATGPT_MODEL")
AZURE_OPENAI_TEMPERATURE = os.environ.get("AZURE_OPENAI_TEMPERATURE") or "0.17"
AZURE_OPENAI_TEMPERATURE = float(AZURE_OPENAI_TEMPERATURE)
AZURE_OPENAI_TOP_P = os.environ.get("AZURE_OPENAI_TOP_P") or "0.27"
AZURE_OPENAI_TOP_P = float(AZURE_OPENAI_TOP_P)
AZURE_OPENAI_RESP_MAX_TOKENS = os.environ.get("AZURE_OPENAI_MAX_TOKENS") or "1000"
AZURE_OPENAI_RESP_MAX_TOKENS = int(AZURE_OPENAI_RESP_MAX_TOKENS)
SYSTEM_MESSAGE_PATH = f"orc/prompts/system_message.prompt"

AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE")
OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def initialize_kernel():
    kernel = sk.Kernel(log=myLogger)
    openai.api_type = "azure"
    openai.api_base = os.environ.get("OPENAI_API_BASE")
    openai.api_version = os.environ.get("OPENAI_API_VERSION")
    openai.api_key =  os.environ.get("OPENAI_API_KEY")
    kernel.add_chat_service(
        "chat-gpt",
        sk_oai.AzureChatCompletion(AZURE_OPENAI_DEPLOYMENT, 
                                    OPENAI_API_BASE, 
                                    OPENAI_API_KEY, 
                                    api_version=OPENAI_API_VERSION,
                                    ad_auth=True), 
    )
    return kernel

def import_plugins(kernel, plugins_directory, filter_plugin_name):
    filter_plugin = kernel.import_semantic_skill_from_directory(plugins_directory, filter_plugin_name)
    return filter_plugin

def create_context(kernel, ask):
    context = kernel.create_new_context()
    context.variables["ask"] = ask
    return context

def get_filterQuery(filter_plugin, context):
    """
    This function is used to create a filter query string from the user ask to be used later in Azure Cognitive Searchfor filtering purposes.
    Data stored in Cognitive search are cellphone models and they have metadata values for 'performance_and_speed' 'camera_quality' and 'display_quality' with 'High' 'Medium' or 'Low' posible values.
    Users will use spanish and you should try to guess if a filter query string could be generated from the ask. 

    Synonyms of high: Alta, elevada, buena, caro, costoso etc
    Synonyms of Medium: Media, mediana, mediano, promedio etc
    Synonyms of Low: Baja, poca, bajo, poco, barato, malo, mala, economico etc

    Filter query string example N°1: (performance_and_speed eq 'Medium') and (camera_quality eq 'Medium') and (display_quality eq 'High')
    Filter query string example N°2: (performance_and_speed eq 'Medium') and (camera_quality eq 'Medium' or camera_quality eq 'Low') and (display_quality eq 'High' or display_quality eq 'Medium')

    If a filter query string could be infered from ask, a filter query string is generated to search for sources.
    If you think is not posible to infer a filter query string from the ask, leave the filte query string as an empty string ""

    synonyms of High: Alta, elevada, buena, bueno, lo mejor, tope de gama, top, gama alta.
    synonyms of Medium: Media, medio, promedio, mediana, gama media.
    synonyms of Low: Bajo, baja, barato, economico, gama baja.
   
    Returns:
    str: A string containing the filter query string. 
        'filterQuery' (str): The filter query string generated from ask. Defaults to '' if not posible to generate.
    """    
    filterQuery_response= {"filterQuery":  ""}
    sk_response = call_semantic_function(filter_plugin["filterQuery"], context)
    if context.error_occurred:
        logging.error(f"[code_orchestration] error when executing RAG flow (Triage). SK error: {context.last_error_description}")
        filterQuery_response["bypass"] = True
    try:
        sk_response_json = json.loads(sk_response.result)
    except json.JSONDecodeError:
        logging.error(f"[code_orchestration] error when executing RAG flow (Triage). Invalid json: {sk_response.result}")
        sk_response_json = {}        
    sk_response_json = json.loads(sk_response.result)
    filterQuery_response["filterQuery"] = sk_response_json.get('intent', 'none')
    return filterQuery_response

# initialize semantic kernel
def filterQuery (ask):
    kernel = initialize_kernel()
    filter_plugin = import_plugins(kernel, "plugins", "filterQuery")
    context = create_context(kernel, ask)
    filterQuery_response = get_filterQuery(filter_plugin, context)
    return filterQuery_response