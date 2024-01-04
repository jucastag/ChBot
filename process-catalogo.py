import json
import os
from embedder.text_embedder import TextEmbedder

# Load the catalog from the 'datos' folder
catalog_file_path = 'datos/catalogo.json'
with open(catalog_file_path, 'r', encoding='utf-8') as catalog_file:
    catalog = json.load(catalog_file)

# Create the 'output' folder if it doesn't exist
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

text_embedder = TextEmbedder()

# Iterate over each phone in the catalog
for phone_data in catalog:
    # Convert the phone data to a JSON-formatted string
    phone_content = json.dumps(phone_data, ensure_ascii=False)

    # Calculate embeddings for the phone content
    phone_embeddings = text_embedder.embed_content(phone_content)
    print(phone_content)

    # Add a new metadata field with the embeddings to the phone data
    phone_data["contentVector"] = phone_embeddings

    # Save the phone data with embeddings to a separate JSON file in the 'output' folder
    phone_model = phone_data["modelo"]
    output_file_path = os.path.join(output_folder, f"{phone_model}.json")
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        json.dump(phone_data, output_file, ensure_ascii=False, indent=2)

    print(f"Embeddings for {phone_model} saved to {output_file_path}")