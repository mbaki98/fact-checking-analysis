import json
import os
from pprint import pprint
from collections import defaultdict, Counter
from util.politics_claimant_categoriser import return_category, get_politician_list

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

            year_dict[year][claimant] += 1

    return year_dict


def main():
    counter = 0
    year_dict = defaultdict(Counter)
    directory = 'data'
    politicians = get_politician_list()
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        # make sure its a file
        if os.path.isfile(file):
            print(filename)
            f = open(file, encoding='utf-8')
            counter += 1
        else:
            continue
        data = json.load(f)
        year_dict = split_by_year_v2(data, year_dict, politicians)

    pprint(year_dict)
    print('counter: ', counter)

    # with open('claimants-grouped.json', 'w') as write_file:
    #     json.dump(year_dict, write_file, indent=4, sort_keys=True)
    # print('done')

    # my_dict = year_dict
    # with open('test.csv', 'w') as f:
    #     for key in my_dict.keys():
    #         f.write("%s,%s\n" % (key, my_dict[key]))

    # politicians = get_politician_list()
    # split_by_year(politicians)


if __name__ == "__main__":
    main()
