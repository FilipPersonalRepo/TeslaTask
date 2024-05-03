import yaml

# Read parameters from input.yml
with open('input.yml', 'r') as file:
    params = yaml.safe_load(file)
print("CHEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEECK")
print(params)

# Replace placeholders in run.json with parameters
with open('run.json', 'r') as file:
    data = json.load(file)
    for key, value in params.items():
        data[key] = value

with open('run.json', 'w') as file:
    json.dump(data, file, indent=4)
