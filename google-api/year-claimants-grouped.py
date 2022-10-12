import json
import os
from pprint import pprint
from collections import defaultdict, Counter
from util.politics_claimant_categoriser import return_category, get_politician_list
from consistency import process_ratings
from fleiss_calc_combined import standardise_rating


'''
Output of this file: claimants-grouped.csv . A file which is split by year and contains every unique claimant and thier 
count for that year

This file runs the function split_by_year_v2(data, year_dict) from main. In main it loops through the /data folder which
contains all of the fact checking orgs fact checks pulled using the google API. In every file the function is called 
and given a dict (year_dict) and the file (data). It loops through all the claims in the file, and for every claim with
a claimant, runs it through the return_category(claimant) function to categorise the claimant and then adds it to the 
year_dict if it hasn't been added already or increments that claimants counter. 

Note: It splits by year by taking the 'reviewDate' from the claim
'''


def split_by_year_v2(data, year_dict, politicians: set):
    # for every claim in the file
    for claim in data['claims']:
        if 'claimant' in claim:
            claimant = claim['claimant']
        else:
            continue  # skip this one, move to next claim

        claimant = claimant.lower()
        claimant = return_category(claimant)

        for review in claim['claimReview']:
            if 'reviewDate' in review.keys():
                year = review['reviewDate'][0:4]
            else:
                continue  # skip this one, move to next claimReview

            rating = review['textualRating']
            rating = standardise_rating(process_ratings(rating.lower()))
            # print('claimant: ' + claimant)
            if year in year_dict:
                # print('\nif year in year_dict BEFORE: ')
                # pprint(year_dict)
                # print(year_dict[year].values())
                # print(year_dict[year].items())
                # print(year_dict[year].keys())
                if claimant in year_dict[year].keys():
                    # print('shud get here')
                    # print(year_dict[year][claimant].keys())
                    if rating in year_dict[year][claimant].keys():
                        year_dict[year][claimant][rating]['count'] += 1
                    else:
                        year_dict[year][claimant][rating] = {'count': 1}
                else:
                    year_dict[year][claimant] = {}
                    year_dict[year][claimant][rating] = {'count': 1}

                    # year_dict[year].update({'claimant': claimant, 'count': 1, "rating": rating})
                # print('if year in year_dict AFTER: ')
                pprint(year_dict)
            else:
                # print('\nif year not in year_dict BEFORE: ')
                # pprint(year_dict)
                year_dict[year] = {}
                year_dict[year][claimant] = {}
                year_dict[year][claimant][rating] = {'count': 1}
                # year_dict[year].update({'claimant': claimant, 'count': 1, "rating": rating})
                # print('if year not in year_dict AFTER: ')
                # pprint(year_dict)


            # if claimant in year_dict[year].keys():
            #     print('so shud this but its not')
            #     year_dict[year]['count'] += 1
            # else:
            #     print('this shud only print a handful of times')
            #     year_dict[year].update({'claimant': claimant, 'count': 1, "rating": rating})
            #     pprint(year_dict)


            # this doesnt work for some reason
            # if claimant in year_dict[year]:
            #     continue
            # else:
            #     year_dict[year][claimant] = {}

            # year_dict['year']['count'] += 1
            # year_dict['year'][rating] = 1

    return year_dict


def main():
    year_dict = {}
    politicians = get_politician_list()

    f = open('multiple_test.json', encoding='utf-8')
    data = json.load(f)

    year_dict = split_by_year_v2(data, year_dict, politicians)
    with open('multiple_claimant_ratings_grouped/test.json', 'w') as f:
        json.dump(year_dict, f)
    print('done')


if __name__ == "__main__":
    main()
