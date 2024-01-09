import csv
import json
import os

# Input and output file paths
csv_file_path = 'datos/movistar_products_export.csv'
json_output_path = 'output/movistar_products_export.json'

# CSV headers
csv_headers = ["name", "type", "code", "price", "precio_de_oferta", "visibility", "estado", "in_stock_configurable",
               "another_deposit_stock", "business_b2b", "store", "source", "in_stock_default", "default_qty",
               "Default_salable_qty", "terminals_source", "in_stock_terminals", "terminals_qty", "terminals_salable_qty",
               "enabled_discount_i_am_movistar"]

# Read CSV and convert to JSON
result_json = []
with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # Print CSV headers for verification
    headers = next(csv_reader)
    print(f"CSV Headers: {headers}")
    
    for row in csv_reader:
        # Print each row for verification
        print(f"CSV Row: {row}")
        
        item = {}
        for i, header in enumerate(csv_headers):
            if i < len(row):
                item[header] = row[i].strip()
            else:
                item[header] = None
        result_json.append(item)

# Write JSON to output file
output_folder = os.path.dirname(json_output_path)
os.makedirs(output_folder, exist_ok=True)
with open(json_output_path, 'w', encoding='utf-8') as json_file:
    json.dump(result_json, json_file, indent=2, ensure_ascii=False)

print(f"Conversion completed. JSON file saved at: {json_output_path}")