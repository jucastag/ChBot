import os
import openai
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, LLMPredictor, ServiceContext
from langchain.chat_models import ChatOpenAI
from flask import Flask, request
from flask import Flask, render_template
from config import OPENAI_API_KEY

app = Flask(__name__)

# Cambia esto por tu API de OpenAI
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
openai.api_key = os.environ.get('OPENAI_API_KEY') # Modifique para que tome automaticamente la Api key

#ahi hice un commit

def cargar_datos(pregunta):
    # Leer los PDFs
    pdf = SimpleDirectoryReader('datos').load_data()

    # Definir e instanciar el modelo
    modelo = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')) # type: ignore

    # Indexar el contenido de los PDFs
    service_context = ServiceContext.from_defaults(llm_predictor=modelo)
    index = GPTVectorStoreIndex.from_documents(pdf, service_context=service_context)
    #index.as_query_engine().query(pregunta)
    return index.as_query_engine().query(pregunta)

@app.route('/')
def index():
    chatbot_name = 'Chatcel' # reemplaza esto con el nombre de tu chatbot
    return render_template('index.html', chatbot_name=chatbot_name)

@app.route('/openai') # type: ignore
def query():
    pregunta = request.args.get('pregunta')
    
    if not pregunta or pregunta.strip() == "." or pregunta.strip() == "":
        return "Por favor, haz una pregunta válida referida al catálogo de celulares."

    pregunta += " Sos un vendedor de telefonos celulares y deberás responder en español. Dar explicaciones de las decisiones y por qué se recomienda ese modelo particular, en lenguaje coloquial y sin términos demasiado técnicos, junto con otras alternativas en caso de querer opciones"
    print(f"pregunta: {pregunta}")

    try:
        respuesta = cargar_datos(pregunta)
        print(f"Respuesta: {respuesta}")
        return respuesta.response # type: ignore
    except Exception as e:
        print(f"Error: {e}")
        return f"Ocurrió un error al procesar la solicitud: {str(e)}"

if __name__ == '__main__':
    app.run(debug=False, host='localhost',port= 8080)
