import os
import time
from flask import Flask, render_template, request
from langchain.chat_models import AzureChatOpenAI
from scripts.retrieval import retrieve_documents
from dotenv import load_dotenv
from scripts.filterQuery import generate_filter_query
import speech_recognition as sr

app = Flask(__name__)

load_dotenv()

os.environ['AZURE_SEARCH_SERVICE'] = os.getenv("AZURE_SEARCH_SERVICE")
os.environ['AZURE_SEARCH_INDEX'] = os.getenv("AZURE_SEARCH_INDEX")
os.environ['AZURE_SEARCH_API_VERSION'] = os.getenv("AZURE_SEARCH_API_VERSION")
os.environ['AZURE_SEARCH_SERVICE_KEY'] = os.getenv("AZURE_SEARCH_SERVICE_KEY")

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY_2'] = os.getenv("OPENAI_API_KEY_2")
os.environ['OPENAI_API_TYPE'] = os.getenv("OPENAI_API_TYPE")
os.environ['OPENAI_API_VERSION'] = os.getenv("OPENAI_API_VERSION")
os.environ['OPENAI_API_BASE'] = os.getenv("OPENAI_API_BASE")
os.environ['AZURE_OPENAI_EMBEDDING_MODEL'] = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL")
os.environ['AZURE_OPENAI_DEPLOYMENT'] = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        question = r.recognize_google(audio, language="es-ES")  # Specify language if needed
        return question
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"Speech Recognition request failed: {e}")
        return ""

def cargar_datos(pregunta, Sources):

    llm = AzureChatOpenAI(
        deployment_name="chat",
        model_name="gpt-35-turbo-16k",
        temperature=0.0
    )
        
    from langchain.schema import (
        SystemMessage,
        HumanMessage,
        AIMessage
    )

    # Agregar el catálogo al prompt
    messages = [
        SystemMessage(content=f"""You are a cellphone salesperson, and you should respond in Spanish. Provide explanations for the decisions and why that particular model is recommended, using colloquial language without overly technical terms, along with other alternatives in case the user wants options. Only recommend phone models that are available in the sources below. If there are no phone models in the sources, inform the user that no matching models were found for their search.
        Sources:
        {Sources}
        """)
    ]

    messages.append(
        HumanMessage(
            content=pregunta
        )
    )

    AIMessage = llm(messages)

    return AIMessage

@app.route('/')
def index():
    chatbot_name = 'Chatcel' # reemplaza esto con el nombre de tu chatbot
    timestamp = int(time.time())
    return render_template('index.html', chatbot_name=chatbot_name, timestamp=timestamp)

@app.route('/openai') # type: ignore
def query():
    pregunta = request.args.get('pregunta')
    
    if not pregunta or pregunta.strip() == "." or pregunta.strip() == "":
        return "Por favor, haz una pregunta válida referida al catálogo de celulares."
    print(f"pregunta: {pregunta}")
    # Generate filter query
    #filter_query = generate_filter_query(pregunta)
    #print(f"Filter Query: {filter_query}")

    try:
        if pregunta == "speech":
            pregunta = recognize_speech()
            if not pregunta:
                return "No se pudo reconocer la pregunta de audio."

        relevant_documents = retrieve_documents(pregunta)
        print(f"Sources: {relevant_documents}")
        Sources = str(relevant_documents)
        respuesta = str(cargar_datos(pregunta, Sources))
        print(f"Respuesta: {respuesta}")
        respuesta = respuesta.replace('\\n\\n', '<br><br>')
        respuesta = respuesta.replace('\'', '')
        respuesta = respuesta.replace('content=', '')
        respuesta = respuesta.replace('additional_kwargs={} example=False', '')
        return respuesta
    
    except Exception as e:
        print(f"Error: {e}")
        return f"Ocurrió un error al procesar la solicitud: {str(e)}"

if __name__ == '__main__':
    app.run(debug=False, host='localhost',port= 8080)