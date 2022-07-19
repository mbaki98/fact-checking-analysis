"""
Creates json file containing only the multiple claims
"""

import json
import os

# parse initial file so that future data could be appended
f = open('english.json', encoding='utf-8')
data = json.load(f)

multiple_claims = []


for claim in data:
    if len(claim['claimReview']) > 1:
        multiple_claims.append(claim)

# this works for original file strucure that had claims nested object, the other structure goes into list right away
"""for claim in data['claims']:
    if len(claim['claimReview']) > 1:
        multiple_claims.append(claim)"""


with open('multiple.json', 'w', encoding='utf-8') as outfile:
    json.dump(multiple_claims, outfile, indent=2, ensure_ascii=False)