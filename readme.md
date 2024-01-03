
To run this repository create an environment:

python -m venv env
.\env\Scripts\activate

load your azure openai credentials in .env file:

OPENAI_API_KEY= 'your_azure_openai_api_key_here'
OPENAI_API_TYPE= 'azure'
OPENAI_API_VERSION= '2023-05-15' # adjust as neccesary
OPENAI_API_BASE= 'your_azure_openai_endpoint_here'

Install other dependencies if needed (langchain, flask, openai, python-dotenv etc)