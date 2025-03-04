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

# Track relationships
relationships = []

# Process datasets
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

# Process relationships
for dataset in schema.get('datasets', []):
    if dataset.get('datasetType') == 'esriDTRelationshipClass':
        relationship = {
            "origin": dataset.get('originClassNames', [{}])[0].get('name'),
            "destination": dataset.get('destinationClassNames', [{}])[0].get('name'),
            "cardinality": dataset.get('cardinality'),
            "forwardPathLabel": dataset.get('forwardPathLabel'),
            "backwardPathLabel": dataset.get('backwardPathLabel')
        }
        relationships.append(relationship)

# Create links based on relationships
for rel in relationships:
    if rel['origin'] in dataset_keys and rel['destination'] in dataset_keys:
        linkDataArray.append({
            "from": rel['origin'],
            "to": rel['destination'],
            "text": "1" if rel['cardinality'] == 'esriRelCardinalityOneToMany' else "1",
            "toText": "0..N" if rel['cardinality'] == 'esriRelCardinalityOneToMany' else "1"
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