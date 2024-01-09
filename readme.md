# chat

## Installation

1) Create an environment if it doesn't exist.

```sh
python -m venv env
.\env\Scripts\activate
```

2) load your azure openai credentials in .env file

3) Install other dependencies if needed (langchain, flask, openai, python-dotenv etc)

```sh
pip install -r requirements.txt
```

## Run the app

1) run the script chatWeb.py 

2) open link: http://localhost:8080

## Process the catalogue:

Run script process-catalogo.py. 
It reads the json in 'datos' folder, then it splits the file into separate json for each phone model with embeddings added and store them in 'output' folder.

## Deploy in GCP

The following setup is required:

* An active GCP account with billing enabled
* A project created within GCP
* The Google SDK installed locally

Once these requirements are met, follow these steps:

* Run:

```sh
gcloud init 
```

Then, select the created project.

* Run:

```sh
gcloud app deploy
```

This will deploy the application based on the configurations specified in the app.yaml file, and files listed in the .gcloudignore file will be ignored.
The chatWeb_gcp.py file will be considered as the main file. Please ensure that the following section is commented out (as Gunicorn in App Engine handles it):

```py
Copy code
if __name__ == '__main__':
    app.run(debug=False, host='localhost',port= 8080)
```
