import json

# Specify the full path to the JSON file
file_path = r'B:\Script\schema_report.json.json'  # Update this path

# Load the JSON file
with open(file_path, 'r') as file:
    schema = json.load(file)

# Extract domains
domains = {domain['name']: domain for domain in schema.get('domains', [])}

# Generate nodeDataArray and linkDataArray
nodeDataArray = []
linkDataArray = []

# Track datasets and their primary keys
dataset_keys = {}

for dataset in schema.get('datasets', []):
    dataset_name = dataset['name']
    items = []
    primary_key = None

    # Extract fields
    for field in dataset.get('fields', {}).get('fieldArray', []):
        field_info = {
            "name": field['name'],
            "type": field['type'],
            "iskey": field['name'] == "OBJECTID" or field.get('aliasName') == "Primary Key",  # Mark OBJECTID or primary key
            "figure": "Decision",
            "color": "green" if field['name'] == "OBJECTID" or field.get('aliasName') == "Primary Key" else "blue"
        }
        # Add domain information if the field uses a domain
        if 'domain' in field:
            domain_name = field['domain']['domainName']
            if domain_name in domains:
                field_info['domain'] = domains[domain_name]
        items.append(field_info)

        # Identify primary key
        if field['name'] == "OBJECTID" or field.get('aliasName') == "Primary Key":
            primary_key = field['name']

    # Add dataset to nodeDataArray
    nodeDataArray.append({
        "key": dataset_name,
        "location": {"x": 0, "y": 0},  # Adjust positions later
        "items": items,
        "inheritedItems": []
    })

    # Track primary key for relationships
    dataset_keys[dataset_name] = primary_key

    # Check for foreign key relationships
    for field in dataset.get('fields', {}).get('fieldArray', []):
        if field.get('aliasName') == "Support FK" or field.get('aliasName') == "Foreign Key":  # Identify foreign key fields
            related_table = field.get('modelName', '').replace('_guid', '')  # Guess related table name
            if related_table in dataset_keys:
                linkDataArray.append({
                    "from": dataset_name,
                    "to": related_table,
                    "text": "1",  # Assuming 1-to-many relationship
                    "toText": "0..N"
                })

# Combine into the final structure
output = {
    "nodeDataArray": nodeDataArray,
    "linkDataArray": linkDataArray
}

# Save the output to a new JSON file
with open('gojs_data.json', 'w') as file:
    json.dump(output, file, indent=2)

print("GoJS data generated successfully!")
