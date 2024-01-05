from langchain.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
from dotenv import load_dotenv
import os
from langchain.chains import LLMChain

load_dotenv() 
api_key = os.getenv('OPENAI_API_KEY_2')
model = AzureChatOpenAI(temperature=0, deployment_name="chat")

template = """
## Task Goal
The task is to generate a filter query string from the input. If you think is not posible to generate a filter query string from the input, generate the filter query string as an empty string ""
Evaluation features: 'performance_y_velocidad', 'camara_calidad', 'pantalla_calidad'
Posible values for each feature: 'Alta', 'Media', 'Baja'.

For example N°1: "Necesito un celular economico para usar en el trabajo" 
Expected filter query string example N°1: "(performance_y_velocidad eq 'Baja') and (camara_calidad eq 'Baja') and (pantalla_calidad eq 'Baja')"

For example N°2: "Necesito un celular para usar en el trabajo" 
Expected filter query string example N°2: "". #Feature valuation not posible

For example N°3: "Busco un celular iPhone de gama media pero con display de alta calidad"
Expected filter query string example N°3: "(performance_y_velocidad eq 'Media') and (camara_calidad eq 'Media') and (pantalla_calidad eq 'Alta')"

input example N°4: "Hola, busco un celular samsung que tenga camara frontal" 
Expected filter query string example N°4: "". #Feature valuation not posible

For example N°5: "Busco celulares con android de gama media. la camara y pantalla pueden ser de menor calidad tambien" 
Expected filter query string example N°5: "(performance_y_velocidad eq 'Media') and (camara_calidad eq 'Media' or camara_calidad eq 'Baja') and (pantalla_calidad eq 'Baja' or pantalla_calidad eq 'Media')"

Use these synonyms as a guide to interpret the input to generate the values for 'performance_y_velocidad', 'camara_calidad' and 'pantalla_calidad' of the filter query string:
synonyms of Alta: High, Alta, elevada, buena, bueno, lo mejor, el mejor, tope de gama, top, gama alta, alta calidad, caro, costoso.
synonyms of Media: Medio, promedio, mediana, gama media, calidad media.
synonyms of Baja: Baja, barato, economico, gama baja, calidad baja.

- The output is a string object with the generated filter query string.
- Do not generate code. The only output should be the generated filter query string object.
- Do not include 'Expected filter query string:' at begginning of the output.
- The output should not include the word ANSWER.
- If feature valuation is not fully interpretable return an empty string object "".

input: {input}
"""

def generate_filter_query(input_text):
    prompt = PromptTemplate(
        input_variables=['input'],
        template=template
    )
    chain = LLMChain(prompt=prompt, llm=model, verbose=False)
    output = chain.run(input=input_text)
    output = output.strip('\"')
    return output