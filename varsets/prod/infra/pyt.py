import json

REMOVE_MARKER = "_REMOVE_"

def update_dict(d1, d2):
    """
    Recursively update dictionary d1 with values from dictionary d2.
    """
    keys_to_remove = []
    for key, value in d2.items():
        if value == REMOVE_MARKER:
            keys_to_remove.append(key)
        elif isinstance(value, dict):
            if key in d1 and isinstance(d1[key], dict):
                update_dict(d1[key], value)
            else:
                d1[key] = value
        elif isinstance(value, list):
            if key in d1 and isinstance(d1[key], list):
                d1[key] = update_list(d1[key], value)
            else:
                d1[key] = value
        else:
            d1[key] = value

    # Remove keys after iteration to avoid modifying the dictionary while iterating
    for key in keys_to_remove:
        if key in d1:
            del d1[key]
    return d1        
      

def update_list(l1, l2):
    """
    Update a list l1 with values from list l2.
    Handles merging lists and removing specific elements.
    """
    # Copy the original list to start with
    combined = l1.copy()

    # Process removal markers
    for item2 in l2:
        if isinstance(item2, dict) and REMOVE_MARKER in item2:
            item_to_remove = item2[REMOVE_MARKER]
            combined = [
                item for item in combined
                if not (
                    (isinstance(item, dict) and any(value == item_to_remove for value in item.values()))
                    or item == item_to_remove
                )
            ]

    # Merge or append items from l2 into combined list
    for item2 in l2:
        if isinstance(item2, dict) and REMOVE_MARKER in item2:
            continue  # Skip removal markers

        if isinstance(item2, dict):
            matched = False
            for i, item1 in enumerate(combined):
                if isinstance(item1, dict) and any(k in item1 for k in item2):
                    update_dict(item1, item2)
                    matched = True
                    break
            if not matched:
                combined.append(item2)
        elif item2 not in combined:
            combined.append(item2)

    return combined
# Load JSON data from files
with open(r'C:\Git\TeslaTask\varsets\prod\infra\infrav1.json', 'r') as file1:
    f1 = json.load(file1)

with open(r'C:\Git\TeslaTask\varsets\prod\infra\infrav2.json', 'r') as file2:
    f2 = json.load(file2)

# Update f1 with the changes from f2
print(update_dict(f1, f2))

# Save the updated data back to f1.json
with open('merged.json', 'w') as file1:
    json.dump(f1, file1)

print("f1 has been updated with the changes from f2.")