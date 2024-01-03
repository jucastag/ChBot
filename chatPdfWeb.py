import os
import json
from flask import Flask, request
from flask import Flask, render_template
from langchain.chat_models import AzureChatOpenAI
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_TYPE'] = os.getenv("OPENAI_API_TYPE")
os.environ['OPENAI_API_VERSION'] = os.getenv("OPENAI_API_VERSION")
os.environ['OPENAI_API_BASE'] = os.getenv("OPENAI_API_BASE")

def cargar_datos(pregunta):
    # Leer los PDFs

    llm = AzureChatOpenAI(
        deployment_name="chat",
        model_name="gpt-35-turbo-16k"
    )

    # Carga del catálogo desde el archivo JSON
    catalog_path = os.path.join("datos", "catalogo.json")
    with open(catalog_path, "r", encoding="utf-8") as file:
        catalogo = json.load(file)
        
    from langchain.schema import (
        SystemMessage,
        HumanMessage,
        AIMessage
    )

    # Agregar el catálogo al prompt
    messages = [
        SystemMessage(content=f"""Sos un vendedor de telefonos celulares y deberás responder en español. Dar explicaciones de las decisiones y por qué se recomienda ese modelo particular, en lenguaje coloquial y sin términos demasiado técnicos, junto con otras alternativas en caso de querer opciones. Solo recomienda modelos de telefonos que esten disponibles en el catalogo. Los telefonos estan segmentados en 'performance_and_speed', 'camera_quality' y 'display_quality' (high, medium y low). Intenta identificar las caracteristicas deseadas por el usuario para dar recomendacion sobre modelos del catalogo.

        Catalogo    
        {json.dumps(catalogo, indent=4, ensure_ascii=False)}
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

    try:
        respuesta = str(cargar_datos(pregunta))
        print(f"Respuesta: {respuesta}")
        respuesta = respuesta[9:].replace('\\n\\n', '<br><br>')
        respuesta = respuesta[:-1]
        return respuesta
    
    except Exception as e:
        print(f"Error: {e}")
        return f"Ocurrió un error al procesar la solicitud: {str(e)}"

if __name__ == '__main__':
    app.run(debug=False, host='localhost',port= 8080)