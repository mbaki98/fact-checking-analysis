"""
Use dictionary to store key value pairs. The keys will be tuples containing the websites,
e.g. a tuple with (politifact, snopes).
First, use a list to keep track of the current claims websites. Then convert the list into a tuple
Then use that tuple as a key. For the value, we have a dictionary of one website as a key, and the rating
as the value.

"""

import json
import os

# parse initial file so that future data could be appended
f = open('multiple.json', encoding='utf-8')
data = json.load(f)

claim_dict = {}

claim_counter = 0

for claim in data:
    website_list = []
    for review in claim['claimReview']:
        if review['publisher']['name'] not in website_list:
            website_list.append(review['publisher']['name'])
    print(website_list)
    if len(website_list) < 2:
        claim_counter = claim_counter + 1

print(claim_counter)
