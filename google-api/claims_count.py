"""
Counts the number of claims in the given json file
"""

import json
import os
from util.claimant_categoriser import return_category, get_politician_list


def count_multiple_json():
    json_file = 'multiple.json'
    f = open(json_file, encoding='utf-8')
    data = json.load(f)
    print(len(data))


# counts claims not separate fact checks
def count_all_claims():
    directory = 'data'
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        # checking if it is a file and excluding initial file
        if os.path.isfile(file):
            f = open(file, encoding='utf-8')
        else:
            continue

        data = json.load(f)
        print(f'Number of claims in {filename}: {len(data["claims"])}')


def count_by_region():
    return


def count_by_language():
    directory = 'data'
    language_counter_dict = {}
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        # checking if it is a file and excluding initial file
        if os.path.isfile(file):
            f = open(file, encoding='utf-8')
        else:
            continue

        data = json.load(f)

        for claim in data['claims']:
            for claim_review in claim['claimReview']:
                language_code = claim_review['languageCode']
                if language_code not in language_counter_dict:
                    language_counter_dict[language_code] = 1
                else:
                    language_counter_dict[language_code] += 1

    for language, count in language_counter_dict.items():
        print(f"Number of fact checks in {language} is: {count}")


def count_missing_claimant_field():
    directory = 'data'
    claimant_dict = {'present': 0, 'absent': 0}
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        # checking if it is a file and excluding initial file
        if os.path.isfile(file):
            f = open(file, encoding='utf-8')
        else:
            continue

        data = json.load(f)

        for claim in data['claims']:
            if 'claimant' in claim.keys():
                claimant_dict['present'] += 1
            else:
                claimant_dict['absent'] += 1

    for presence, count in claimant_dict.items():
        print(f"Claimant {presence}: {count}")


def count_claimants(politicians: set):
    directory = 'data'
    claimant_dict = {}
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        # checking if it is a file and excluding initial file
        if os.path.isfile(file):
            f = open(file, encoding='utf-8')
        else:
            continue

        data = json.load(f)

        for claim in data['claims']:
            # make sure the 'claimant' field isn't empty in json
            if 'claimant' in claim.keys():
                claimant = claim['claimant']
            else:
                continue

            claimant = claimant.lower()
            claimant = return_category(claimant, politicians, claim)
            if claimant not in claimant_dict:
                claimant_dict[claimant] = 1
            else:
                claimant_dict[claimant] += 1

    print(f'Total claimants: {len(claimant_dict.keys())}')
    other = 0
    for claimant, count in claimant_dict.items():
        if count < 50:
            other += 1
        else:
            print(f'{claimant}: {count}')

    print(f'Claimants appearing less than 50 times: {other}')



def main():
    politicians = get_politician_list()
    # try sort to display in descending order by values https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    count_all_claims()
    print("-----")
    count_multiple_json()
    print('-----')
    count_by_language()
    print('-----')
    count_missing_claimant_field()
    print('-----')
    count_claimants(politicians)
    print('-----')


if __name__ == "__main__":
    main()
