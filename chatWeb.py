import os
from flask import Flask, render_template, request
from langchain.chat_models import AzureChatOpenAI
from retrieval import retrieve_documents
from dotenv import load_dotenv
from filterQuery import generate_filter_query

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

def cargar_datos(pregunta, relevant_documents):

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
        SystemMessage(content=f"""Sos un vendedor de telefonos celulares y deberás responder en español. Dar explicaciones de las decisiones y por qué se recomienda ese modelo particular, en lenguaje coloquial y sin términos demasiado técnicos, junto con otras alternativas en caso de querer opciones. Solo recomienda modelos de telefonos que esten disponibles en el catalogo. Los telefonos estan segmentados en 'performance_y_velocidad', 'camara_calidad' y 'pantalla_calidad' con valores Alta, Media o Baja. Intenta identificar las caracteristicas deseadas por el usuario para dar recomendacion sobre modelos del catalogo.

        Telefonos seleccionados del Catalogo:    
        {str(relevant_documents)}

        No inventes modelos de telefonos. Usa exclusivamente los telefonos seleccionados del catalogo para dar tu recomendacion.
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
    return render_template('index.html', chatbot_name=chatbot_name)

@app.route('/openai') # type: ignore
def query():
    pregunta = request.args.get('pregunta')
    
    if not pregunta or pregunta.strip() == "." or pregunta.strip() == "":
        return "Por favor, haz una pregunta válida referida al catálogo de celulares."
    print(f"pregunta: {pregunta}")
    # Generate filter query
    filter_query = generate_filter_query(pregunta)
    print(f"Filter Query: {filter_query}")

    try:
        relevant_documents = retrieve_documents(pregunta, filter_query)
        print(f"Sources: {relevant_documents}")
        respuesta = str(cargar_datos(pregunta, relevant_documents))
        print(f"Respuesta: {respuesta}")
        respuesta = respuesta[9:].replace('\\n\\n', '<br><br>')
        respuesta = respuesta[:-1]
        return respuesta
    
    except Exception as e:
        print(f"Error: {e}")
        return f"Ocurrió un error al procesar la solicitud: {str(e)}"

if __name__ == '__main__':
    app.run(debug=False, host='localhost',port= 8080)