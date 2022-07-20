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

# should turn this into method and potentially run unit tests to make sure its working as expected. Also could write
# it in thesis

for claim in data:
    # list of the websites that have fact-checked each claim
    website_list = []
    website_ratings = []
    # iterate over the fact checks from different websites for each claim
    for review in claim['claimReview']:
        # if the website for current fact check isn't in list, then add it do I want to make multiple fact checks by same publisher its own category. E.g. Politifact Washington Post Politifact. Should that be same group as Politifact Washington Post? Should I remove duplicates? I feel like its ok to assume same website twice for some fact check is an error or duplicate and shouldn't need to be considered.
        # here I'm assuming if same website shows up twice its an error or duplicate and not being considered.
        if review['publisher']['name'] not in website_list:
            website_list.append(review['publisher']['name'])
            website_rating = (review['publisher']['name'], review['textualRating'])
            website_ratings.append(website_rating)

    website_list.sort()
    print(website_list)
    website_tuple = tuple(website_list)
    if website_tuple not in claim_dict.keys():
        fact_check_list = [website_ratings]
        claim_dict[website_tuple] = fact_check_list
    else:
        fact_check_list = claim_dict[website_tuple]
        fact_check_list.append(website_ratings)
    # need to add list of website lists to the dictionary with key as the tuple of websites. Need to make sure it is added and doesn't override it. Maybe I could get the existing website list then add this new list to it from within the dictionary.
    # if dict with tuple key exists
        # add website lists to existing list
    #else set value of dict with this tuple to

print(claim_counter)
# number of website combinations
print(claim_dict.__len__())
# list of website combinations
print(claim_dict.keys())
