"""
Creates json file containing only english fact checks
"""

import json
import os

# parse initial file so that future data could be appended
f = open('short.json', encoding='utf-8')
data = json.load(f)

english_claims = []

for claim in data['claims']:
    # iterate over a copy of the list since you can't remove elements while iterating over a list in python
    for review in claim['claimReview'][:]:
        if review['languageCode'] != 'en':
            claim['claimReview'].remove(review)

    # ensure you don't add claims that now have no fact checks since non english claimReviews were removed
    if len(claim['claimReview']) > 0:
        english_claims.append(claim)

with open('english.json', 'w', encoding='utf-8') as outfile:
    json.dump(english_claims, outfile, indent=2, ensure_ascii=False)
