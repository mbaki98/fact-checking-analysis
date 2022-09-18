import json
import os
from pprint import pprint
from collections import defaultdict, Counter
from util.nofils_claimant_categoriser import return_category, get_politician_list
import operator


import csv

"""
Create empty dictionary called year_dict

Loop through claims in Politifact

for each claim
    look at the year
    
    if the year is NOT PRESENT in the year_dict
        add the year 
        add a tuple of the claimant and a counter incremeneted to 1
        
    if the year is PRESENT in the year_dict
        check if the claimant is already present
            if claimant has already been added 
                increment the counter
            if claimant has not been added
                add claimant and increment the counter to 1
                
                
4764/8762 in Politifact have a reviewDate
"""


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

'''
                Added two ways of doing it. First starts if year is present
                in dic. Second other way around. Pretty sure need to go
                with first route. 
                
                Check if it exists, if so then increment, if not then 
                add and increment
                
                needs to go:
                
                if year in dict:
                    if claimant already exists
                        increment
                    else
                        append to year
                        increment
                else
                    add year to dict
                    append claimant to year
                    increment
                    
                # if year not in year_dict:
                #     # if year is not in dic, add it with the claimant and the claimants counter
                #     year_dict[year] = [claimant, 1]
                # else:
                #     # if the year is already in the dic, find the claimant and increment its counter
                #     # not sure how to access the claimant
                #     counter += 1
                #     year_dict[year][1] += 1
'''

def split_by_year(politicians: set):
    year_dict = {}
    directory = 'data'
    counter = 0
    for filename in os.listdir(directory):
        counter += 1
        file = os.path.join(directory,filename)

        if os.path.isfile(file):
            f = open(file,encoding='utf-8')
        else:
            continue

        data = json.load(f)

        # for every claim in the file
        for claim in data['claims']:
            if 'claimant' in claim:
                claimant = claim['claimant']
            else:
                continue  # skip this one, move to next claim

            # fix claimant
            claimant = claimant.lower()
            claimant = return_category(claimant, politicians, claim)

            for review in claim['claimReview']:
                if 'reviewDate' in review.keys():
                    year = review['reviewDate'][0:4]
                else:
                    continue  # skip this one, move to next claimReview

                year_dict[year][claimant] += 1

    pprint(year_dict)
    print(counter)


def try2(politicians: set):
    year_dict = {}
    directory = 'data'
    counter = 0
    for filename in os.listdir(directory):
        counter += 1
        file = os.path.join(directory,filename)

        if os.path.isfile(file):
            f = open(file,encoding='utf-8')
        else:
            continue

        data = json.load(f)

        # for every claim in the file
        for claim in data['claims']:
            # placeholder for year & claimant
            year = ''
            claimant = ''
            if 'claimant' in claim:
                claimant = claim['claimant']
            # the reviewDate is in the review so we go into it
            for review in claim['claimReview']:
                # if the review date exists
                if 'reviewDate' in review.keys():
                    # get the year
                    year = review['reviewDate'][0:4]

                    #fix claimant and assign bucket
                    claimant = claimant.lower()
                    claimant = return_category(claimant, politicians, claim)

                    if year in year_dict:
                        # loop through to find the claimant

                        if claimant in year_dict[year]:
                            year_dict[year][1] += 1
                        else:
                            # if claimant doesnt exist
                            year_dict[year].append([claimant, 1])
                    else:
                        # if year not in year_dict
                        year_dict[year] = [claimant, 1]

    pprint(year_dict)
    print('counter: ', counter)




# f = open('data/politifact.json', encoding='utf-8')
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

    with open('claimants-grouped.json', 'w') as write_file:
        json.dump(year_dict, write_file, indent=4, sort_keys=True)
    print('done')

    # my_dict = year_dict
    # with open('test.csv', 'w') as f:
    #     for key in my_dict.keys():
    #         f.write("%s,%s\n" % (key, my_dict[key]))

    # politicians = get_politician_list()
    # split_by_year(politicians)



if __name__ == "__main__":
    main()
