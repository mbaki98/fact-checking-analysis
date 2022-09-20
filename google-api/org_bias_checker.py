from util.nofils_claimant_categoriser import return_category, get_politician_list
import json
from collections import defaultdict, Counter
from pprint import pprint

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


# f = open('data/politifact.json', encoding='utf-8')
def main():
    directory = 'data'
    politicians = get_politician_list()

    f = open('data/testFile.json', encoding='utf-8')
    data = json.load(f)

    year_dict = defaultdict(Counter)
    year_dict = split_by_year_v2(data, year_dict, politicians)

    for year, (counter) in year_dict.items():
        print(year)
        for k, v in counter.items():
            print(k, v)
    # pprint(year_dict)

if __name__ == "__main__":
    main()
