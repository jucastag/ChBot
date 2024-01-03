import os
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
endpoint=OPENAI_API_BASE
deployment_name=AZURE_OPENAI_DEPLOYMENT
api_key=OPENAI_API_KEY

kernel = sk.Kernel()

deployment, api_key, endpoint = AZURE_OPENAI_DEPLOYMENT, OPENAI_API_KEY, OPENAI_API_BASE
azure_chat_service = AzureChatCompletion(deployment_name="chat", endpoint=endpoint, api_key=api_key)   # set the deployment name to the value of your chat model
kernel.add_chat_service("chat_completion", azure_chat_service)

sk_prompt = """
{{$input}}

## Task Goal

The task is to generate a filter query string from the input. If you think is not posible to generate a filter query string from the input, generate the filter query string as an empty string "empty_string"

## Task instructions

This function is used to create a filter query string from the input.
Data to be filtered are cellphone models and they have filterable fields for 'performance_and_speed' 'camera_quality' and 'display_quality' with 'High' 'Medium' or 'Low' posible values.
Users will use spanish and you will try to generate a filter query string. 

synonyms of High: Alta, elevada, buena, bueno, lo mejor, el mejor, tope de gama, top, gama alta, alta calidad.
synonyms of Medium: Media, medio, promedio, mediana, gama media, calidad media.
synonyms of Low: Bajo, baja, barato, economico, gama baja, calidad baja.

Use these synonyms as a guide to interpret the input to generate the values for 'performance_and_speed', 'camera_quality' and 'display_quality' of the filter query string

input example N°1: "Busco un celular de gama media pero con display de alta calidad"
Expected filter query string example N°1: "(performance_and_speed eq 'Medium') and (camera_quality eq 'Medium') and (display_quality eq 'High')"

input example N°2: Busco celulares de gama media. la camara y pantalla pueden ser de menor calidad tambien" 
Expected filter query string example N°2: "(performance_and_speed eq 'Medium') and (camera_quality eq 'Medium' or camera_quality eq 'Low') and (display_quality eq 'Low' or display_quality eq 'Medium')"

input example N°3: Necesito un celular economico para usar en el trabajo" 
Expected filter query string example N°3: "(performance_and_speed eq 'Low') and (camera_quality eq 'Low') and (display_quality eq 'Low')"

If a filter query string could be infered from input, a filter query string is generated to be used later to search for sources.
If you think is not posible to infer a filter query string from the input, leave the filte query string as an empty string "Empty_string"

- The output is a string object with the generated filter query string.
- Do not generate code. Only generate the filter query string object.
- Do not include the word string at begginning of the output.
- The output should not include the word ANSWER.

"""

text = """
    Hola, busco un celular que sea el mejor
"""

tldr_function = kernel.create_semantic_function(prompt_template=sk_prompt, max_tokens=2048, temperature=0, top_p=0.5)

summary = tldr_function(text)

print(f"Output: {summary}") # Output: Robots must not harm humans.