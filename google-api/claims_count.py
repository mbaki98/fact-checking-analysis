"""
Counts the number of claims in the given json file
"""

import json

json_file = 'multiple.json'

f = open(json_file, encoding='utf-8')
data = json.load(f)

print(len(data))
