"""
Reads all files in data folder and adds them into one json file. Ensures duplicates are not added.
Need to specify one initial json file at the beginning.
"""

import json
import os

directory = 'data'
# parse initial file so that future data could be appended
f = open('data/aap.json', encoding='utf-8')
data = json.load(f)

# iterate over files in
# that directory
for filename in os.listdir(directory):
    file = os.path.join(directory, filename)
    # checking if it is a file and excluding initial file
    if os.path.isfile(file) and file != 'data\\aap.json':
        f = open(file, encoding='utf-8')
        new_data = json.load(f)
        # add claim to data except if it is a duplicate
        for claim in new_data['claims']:
            if claim not in data['claims']:
                data['claims'].append(claim)

with open('short.json', 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, ensure_ascii=False)

#with open('claims.json', 'w', encoding='utf-8') as outfile:
#    json.dump(data, outfile, ensure_ascii=False, indent=2)






