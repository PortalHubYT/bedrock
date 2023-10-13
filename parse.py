# parse.py
import sys

import yaml

if len(sys.argv) < 2:
    print("Usage: parse.py <section>")
    sys.exit(1)

with open('config.yaml', 'r') as file:
    data = yaml.safe_load(file)

section = sys.argv[1]
if section not in data:
    print(f"Section '{section}' not found!")
    sys.exit(2)

for key, value in data[section].items():
    if isinstance(value, dict):  # Check if the value is a nested dictionary
        for inner_key, inner_value in value.items():
            if isinstance(inner_value, bool):
                inner_value = 'true' if inner_value else 'false'
            print(f"{inner_key.upper()}={inner_value}")
    else:
        if isinstance(value, bool):
            value = 'true' if value else 'false'
        print(f"{key.upper()}={value}")
