
To run this repository create an environment if not existing.

python -m venv env
.\env\Scripts\activate

load your azure openai credentials in .env file:

OPENAI_API_KEY= 'your_azure_openai_key_here'

OPENAI_API_TYPE= 'azure'.
OPENAI_API_VERSION= '2023-05-15' # adjust as neccesary.
OPENAI_API_BASE= 'your_azure_openai_endpoint_here'.
AZURE_OPENAI_SERVICE_NAME="your_azure_openai_service_name_here"
AZURE_OPENAI_EMBEDDING_MODEL="text-embedding-ada-002" # adjust as neccesary.
AZURE_SEARCH_SERVICE = "your_Azure_search_service_name_here".
AZURE_SEARCH_INDEX = "your_cognitive_search_index_here" # adjust as neccesary.
AZURE_SEARCH_API_VERSION = "2023-07-01-Preview" # adjust as neccesary.
AZURE_SEARCH_SERVICE_KEY="your_azure_cognitive_search_service_key_here".
AZURE_OPENAI_EMBEDDING_DEPLOYMENT="text-embedding-ada-002" # adjust as neccesary.

Install other dependencies if needed (langchain, flask, openai, python-dotenv etc)

Tu run the App:
run the script chatWeb.py and open link: http://localhost:8080

To process the catalogue:
Run script process-catalogo.py. It reads the json in 'datos' folder, then it splits the file into separate json for each phone model with embeddings added and store them in 'output' folder.