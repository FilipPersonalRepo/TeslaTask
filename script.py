import json
import yaml

# Read parameters from input.yml
with open('input.yml', 'r') as file:
    params = yaml.safe_load(file)

# Replace placeholders in run.json with parameters
with open('run.json', 'r') as file:
    data = json.load(file)

print(data)
def replace_placeholders(data, params):
    if isinstance(data, str):
        for key, value in params.items():
            data = data.replace(f"{{{{{key}}}}}", value)
        return data
    elif isinstance(data, dict):
        return {key: replace_placeholders(value, params) for key, value in data.items()}
    elif isinstance(data, list):
        return [replace_placeholders(item, params) for item in data]
    return data

updated_json_data = replace_placeholders(data, params)    
print(updated_json_data)
