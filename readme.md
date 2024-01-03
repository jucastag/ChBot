
To run this repository create an environment if not existing.

python -m venv env
.\env\Scripts\activate

load your azure openai credentials in .env file:

Install other dependencies if needed (langchain, flask, openai, python-dotenv etc)

Tu run the App:
run the script chatWeb.py and open link: http://localhost:8080

To process the catalogue:
Run script process-catalogo.py. It reads the json in 'datos' folder, then it splits the file into separate json for each phone model with embeddings added and store them in 'output' folder.