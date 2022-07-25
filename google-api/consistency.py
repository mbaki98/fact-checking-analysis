"""
Use dictionary to store key value pairs. The keys will be tuples containing the websites,
e.g. a tuple with (politifact, snopes).
First, use a list to keep track of the current claims websites. Then convert the list into a tuple
Then use that tuple as a key. For the value, we have a dictionary of one website as a key, and the rating
as the value.

"""

import json
from pprint import pprint

import pandas
import pandas as pd

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

print(claim_counter)
# number of website combinations
print(claim_dict.__len__())
# list of website combinations
print(claim_dict.keys())
# pretty print dictionary
pprint(claim_dict)

consistency_dict = {}

for key in claim_dict.keys():
    for claim in claim_dict[key]:
        # in the case of only two websites fact checking a claim, check if they're consistant. Store as 1 or 0
        if len(claim) == 2:
            # if they're consistent set value to 1 for this item in the list of the tuple
            if claim[0][1] == claim[1][1]:
                print("The two claims are consistent", end=" - ")
                print(claim)
                if key not in consistency_dict:
                    consistency_dict[key] = [1]
                else:
                    consistency_dict[key].append(1)
            # if inconsistent set value to 0
            else:
                print("The two claims are inconsistent", end=" - ")
                print(claim)
                if key not in consistency_dict:
                    consistency_dict[key] = [0]
                else:
                    consistency_dict[key].append(0)
        elif len(claim) == 3:
            if claim[0][1] == claim[1][1] == claim[2][1]:
                print("The three claims are consistent", end=" - ")
                print(claim)
                if key not in consistency_dict:
                    consistency_dict[key] = [111]
                else:
                    consistency_dict[key].append(111)
            elif claim[0][1] == claim[1][1] != claim[2][1]:
                print("The first two claims are consistent", end=" - ")
                print(claim)
                new_key = (claim[0][1], claim[1][1])
                if key not in consistency_dict:
                    consistency_dict[key] = [110]
                else:
                    consistency_dict[key].append(110)

            elif claim[0][1] != claim[1][1] == claim[2][1]:
                print("The last two claims are consistent", end=" - ")
                print(claim)
                if key not in consistency_dict:
                    consistency_dict[key] = [11]
                else:
                    consistency_dict[key].append(11)
            elif claim[0][1] == claim[2][1] != claim[1][1]:
                print("The first and last claims are consistent", end=" - ")
                print(claim)
                if key not in consistency_dict:
                    consistency_dict[key] = [101]
                else:
                    consistency_dict[key].append(101)
            else:
                print("All three claims are inconsistent", end=" - ")
                print(claim)
                if key not in consistency_dict:
                    consistency_dict[key] = [0]
                else:
                    consistency_dict[key].append(0)
        # if length of items in the claim is 1, then it is a case where the same website fact checked info more than once, which in the current state of the script we're not taking into account
        elif len(claim) == 1:
            print("Invalid" + str(len(claim)))
        else:
            print("Unknown Error")

counter = 0
for key in consistency_dict.keys():
    print(key, consistency_dict[key])
    counter = counter + len(consistency_dict[key])

print(counter)

percentages_dict = {}
for key in consistency_dict.keys():
    counter = 0
    ab_counter = 0
    ac_counter = 0
    bc_counter = 0
    for claim in consistency_dict[key]:
        if claim == 1 or claim == 111:
            counter = counter + 1
            ab_counter = ab_counter + 1
            ac_counter = ac_counter + 1
            bc_counter = bc_counter + 1
        elif claim == 110:
            ab_counter = ab_counter + 1
        elif claim == 101:
            ac_counter = ac_counter + 1
        elif claim == 11:
            bc_counter = bc_counter + 1
    percentage = counter / len(consistency_dict[key]) * 100
    ab_percentage = ab_counter / len(consistency_dict[key]) * 100
    ac_percentage = ac_counter / len(consistency_dict[key]) * 100
    bc_percentage = bc_counter / len(consistency_dict[key]) * 100
    if len(key) == 2:
        percentages_dict[key] = percentage
    elif len(key) == 3:
        percentages_dict[key] = [percentage, key[0] + " " + key[1] + ": " + str(ab_percentage),
                                 key[0] + " " + key[2] + ": " + str(ac_percentage),
                                 key[1] + " " + key[2] + ": " + str(bc_percentage)]

for key in percentages_dict.keys():
    print(key, percentages_dict[key])
