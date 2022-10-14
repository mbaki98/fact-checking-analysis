"""
Use dictionary to store key value pairs. The keys will be tuples containing the websites,
e.g. a tuple with (politifact, snopes).
First, use a list to keep track of the current claims websites. Then convert the list into a tuple
Then use that tuple as a key. For the value, we have a dictionary of one website as a key, and the rating
as the value.

"""
import csv
import os
import re
import sys

from sklearn.metrics import cohen_kappa_score
import json
from pprint import pprint
import itertools
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import string


def create_fact_check_list(data):
    claim_dict = {}
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
        # print(website_list)
        website_tuple = tuple(website_list)
        if website_tuple not in claim_dict.keys():
            fact_check_list = [website_ratings]
            claim_dict[website_tuple] = fact_check_list
        else:
            fact_check_list = claim_dict[website_tuple]
            fact_check_list.append(website_ratings)
    return claim_dict


# Analysing consistency
def create_consistency_dict(claim_dict: dict):
    consistency_dict = {}
    for key in claim_dict.keys():
        for claim in claim_dict[key]:
            # in the case of only two websites fact checking a claim, check if they're consistant. Store as 1 or 0
            if len(claim) == 2:
                # if they're consistent set value to 1 for this item in the list of the tuple
                if claim[0][1] == claim[1][1]:
                    # print("The two claims are consistent", end=" - ")
                    # print(claim)
                    if key not in consistency_dict:
                        consistency_dict[key] = [1]
                    else:
                        consistency_dict[key].append(1)
                # if inconsistent set value to 0
                else:
                    # print("The two claims are inconsistent", end=" - ")
                    # print(claim)
                    if key not in consistency_dict:
                        consistency_dict[key] = [0]
                    else:
                        consistency_dict[key].append(0)
            elif len(claim) == 3:
                if claim[0][1] == claim[1][1] == claim[2][1]:
                    # print("The three claims are consistent", end=" - ")
                    # print(claim)
                    if key not in consistency_dict:
                        consistency_dict[key] = [111]
                    else:
                        consistency_dict[key].append(111)
                elif claim[0][1] == claim[1][1] != claim[2][1]:
                    # print("The first two claims are consistent", end=" - ")
                    # print(claim)
                    new_key = (claim[0][1], claim[1][1])
                    if key not in consistency_dict:
                        consistency_dict[key] = [110]
                    else:
                        consistency_dict[key].append(110)

                elif claim[0][1] != claim[1][1] == claim[2][1]:
                    # print("The last two claims are consistent", end=" - ")
                    # print(claim)
                    if key not in consistency_dict:
                        consistency_dict[key] = [11]
                    else:
                        consistency_dict[key].append(11)
                elif claim[0][1] == claim[2][1] != claim[1][1]:
                    # print("The first and last claims are consistent", end=" - ")
                    # print(claim)
                    if key not in consistency_dict:
                        consistency_dict[key] = [101]
                    else:
                        consistency_dict[key].append(101)
                else:
                    # print("All three claims are inconsistent", end=" - ")
                    # print(claim)
                    if key not in consistency_dict:
                        consistency_dict[key] = [0]
                    else:
                        consistency_dict[key].append(0)
            # if length of items in the claim is 1, then it is a case where the same website fact checked info more than once, which in the current state of the script we're not taking into account
            """elif len(claim) == 1:
                print("Invalid" + str(len(claim)))
            else:
                print("Unknown Error")"""

    return consistency_dict


def count_consistency_dict(consistency_dict: dict):
    counter = 0
    for key in consistency_dict.keys():
        # print(key, consistency_dict[key])
        # print(len(consistency_dict[key]))
        counter = counter + len(consistency_dict[key])

    # print(counter)


def create_percentages_dict(consistency_dict):
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

    return percentages_dict


def calculate_reliability(consistency_dict: dict):
    # reverse code my original coding into a structure where labeller 1 and 2 are separate
    # so ('The New York Times', 'The Washington Post') [0, 0] becomes labeller 1 [0,0] labeller 2 [1,1]
    # cohens capper isn't just a 1 or 0 thing though, works on a scale as well for continuous variables.
    # migth be worthwhile to reconsider my idea of creating a standardised scale of 0 5o for example across various fact checkers.
    # e.g. false is 0, four pinnochios also 0, true is 5, correct is 5, accurate is 5 etc. that way we actually get descrepancy measured as well.

    for websites, consistencies in consistency_dict.items():
        print(websites)
        if len(websites) == 2:
            rater1 = []
            rater2 = []
            for isConsistent in consistencies:
                if isConsistent:
                    rater1.append(1)
                    rater2.append(1)
                else:
                    rater1.append(0)
                    rater2.append(1)
            print(rater1)
            print(rater2)
            print("----")

            # raters = [rater1, rater2]
            # print(cohen_kappa_score(rater2, rater1))

            labeler1 = [1, 1]
            labeler2 = [1, 1]
            print(cohen_kappa_score(labeler1, labeler2))
            """data = np.zeros((len(raters), len(raters)))
            # Calculate cohen_kappa_score for every combination of raters
            # Combinations are only calculated j -> k, but not k -> j, which are equal
            # So not all places in the matrix are filled.
            for j, k in list(itertools.combinations(range(len(raters)), r=2)):
                data[j, k] = cohen_kappa_score(raters[j], raters[k])

            sns.heatmap(
                data,
                mask=np.tri(len(raters)),
                annot=True, linewidths=5,
                vmin=0, vmax=1,
                xticklabels=[f"Rater {k + 1}" for k in range(len(raters))],
                yticklabels=[f"Rater {k + 1}" for k in range(len(raters))],
            )
            plt.show()"""


# !does not standardise ratings! simply processes them if they are long or contain other text
# e.g. rating "mostly false. Trump said this in a different context" is converted to "mostly false"
def process_ratings(rating: str):
    ratings = re.split("\W+|_", rating)
    if ratings[0] in ['false']:
        return "false"
    if ratings[0] in ['wrong']:
        return "wrong"
    if ratings[0] == "partly":
        return "half true"
    elif ratings[0] in ["mostly"]:
        if ratings[1] == "false":
            return "mostly false"
        elif ratings[1] == "true":
            return "mostly true"
    elif ratings[0] in ["somewhat"]:
        if ratings[1] == "false":
            return "somewhat false"
        elif ratings[1] == "true":
            return "somewhat true"
    elif ratings[0] == "true":
        return "true"
    # elif ' '.join(ratings[0:2]) == "half right":
    #     return "half true"
    elif ratings[0] in ['exagerated', 'exaggerates'] or ' '.join(ratings[0:3]) == "this is exaggerated":
        return "exaggerated"
    elif ' '.join(ratings[0:3]) in ["no evidence provided", "this lacks evidence"]:
        return "no evidence"
    elif ' '.join(ratings[0:2]) in ["lacks context", "needs context"] or ' '.join(ratings[0:3]) == "needs more context":
        return "out of context"
    elif ' '.join(ratings[0:3]) in ["this is misleading"]:
        return "misleading"
    else:
        return rating


# converts to csv file, if process = True, then punctuation will be removed and process_ratings() will be called
def convert_to_csv(data: dict, process: bool):
    csv_columns = ["PolitiFact", "FactCheck.org", "The Washington Post", "The New York Times", "BBC"]
    if process:
        csv_file = "processed_interrater.csv"
    else:
        csv_file = "unprocessed_interrater.csv"
    final_list = []
    try:
        with open(csv_file, 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_columns)
            for claim in data:
                # do not add claim if its being fact checked only by one website
                if claim['claimReview'][0]["publisher"] == claim['claimReview'][1]["publisher"]:
                    continue
                # use this bool to track if website other than 5 above is found, so that claim is ignored
                valid_website = True
                websites = []
                for review in claim['claimReview']:
                    if review['publisher']['name'] not in csv_columns:
                        valid_website = False
                        break
                    websites.append([review['publisher']['name'], review['textualRating'].lower()])

                if not valid_website:
                    continue

                row = ["", "", "", "", ""]
                for website in websites:
                    # remove punctuation from rating if process param is True
                    if process:
                        website[1] = website[1].translate(str.maketrans('', '', string.punctuation))
                        website[1] = process_ratings(website[1])
                    if website[0] == "PolitiFact":
                        row[0] = website[1]
                    if website[0] == "FactCheck.org":
                        row[1] = website[1]
                    if website[0] == "The Washington Post":
                        row[2] = website[1]
                    if website[0] == "The New York Times":
                        row[3] = website[1]
                    if website[0] == "BBC":
                        row[4] = website[1]
                print(row)
                writer.writerow(row)
                final_list.append(row)
    except IOError:
        print("IO Error")

    return final_list


def standardise_ratings(final_list):
    false = ["pants on fire", "Four pinocchios", "Lie of the year", "No evidence", "Very wrong", "Pants on fire",
             "wrong", "Not what X said", "unsupported"]
    mostly_false = ["mostly false", "Three pinocchios", "Misrepresents the record",
                    "inflated", "misleading", "Distorts the facts", "Experts disagree", "Somewhat true", "Partly true",
                    "numbers in dispute"]
    half_true = ["two pinocchios", "Greatly oversold", "Out of context", "Hard to verify", "Not the whole story",
                 "exaggerated", "True, but cherry picked", "Cherry picked", "half true", "half right", "half-right",
                 "half-true", "Hard to verify", "Not the whole story",
                 "Spins the facts", "Way early to say", "cherry picks", "Half right"]
    mostly_true = ["mostly true", "One pinocchio", "Largely correct", "Partly false", "Somewhat false"]
    true = ["true", "Gepetto checkmark", "accurate"]
    for i, claim in enumerate(final_list):
        for j, website_rating in enumerate(claim):
            if website_rating in (standardised.lower() for standardised in false):
                final_list[i][j] = "false"
            if website_rating in (standardised.lower() for standardised in mostly_false):
                final_list[i][j] = "mostly false"
            if website_rating in (standardised.lower() for standardised in half_true):
                final_list[i][j] = "half true"
            if website_rating in (standardised.lower() for standardised in mostly_true):
                final_list[i][j] = "mostly true"
            if website_rating in (standardised.lower() for standardised in true):
                final_list[i][j] = "true"

    return final_list


def write_standardised_to_csv(standardised_list: list, csv_file="standardised_interrater.csv"):
    csv_columns = ["PolitiFact", "FactCheck.org", "The Washington Post", "The New York Times", "BBC"]
    try:
        with open(csv_file, 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_columns)
            for claim in standardised_list:
                writer.writerow(claim)

    except IOError:
        print("IO Error")


def split_fact_checkers_into_two(standardised_list: list, directory="data/consistency_csv", files_suffix="Consistency"):
    csv_columns = ["PolitiFact", "FactCheck.org", "The Washington Post", "The New York Times", "BBC"]
    checked = []
    for i, firstChecker in enumerate(csv_columns):
        for j, secondChecker in enumerate(csv_columns):
            if i == j:
                continue
            # check checked backwards with secondChecker first since if they appear it'll be in a different order
            if [secondChecker, firstChecker] in checked:
                continue
            # append websites to checked so that we don't repeat them
            checked.append([firstChecker, secondChecker])
            with open(f'{directory}/{firstChecker}{secondChecker} {files_suffix}.csv', 'w', newline='',
                      encoding='utf-8') as csvfile:
                websites = [firstChecker, secondChecker]
                writer = csv.writer(csvfile)
                writer.writerow(websites)
                for k, claim in enumerate(standardised_list):
                    if claim[i] != "" and claim[j] != "":
                        row = [claim[i], claim[j]]
                        writer.writerow(row)


def read_ratings_csv(file: string):
    with open(file, 'r') as file:
        csvreader = csv.reader(file)
        final_list = []
        for i, row in enumerate(csvreader):
            if i == 0:
                continue
            else:
                final_list.append(row)

        return final_list


# some ratings even after processing still are not fully standardised. e.g. "hasnt said why"
def process_standardised_list(standardised_list):
    half_true = ["chant is routine", "cherry picks", "hasnt said why", "in dispute", "small impact for most",
                 "they are not eligible"]
    mostly_true = ["depends on whos counting", "the majority are suicides"]
    mostly_false = ["doj killed not murdered", "ignores coronavirus job losses", "migrants not driving surge",
                    "misuse of irs data"]
    false = ["experts not a bailout", "no early timeline", "not historic or final", "not what gm says",
             "not what cbo said", "not what zelensky said"]

    for i, claim in enumerate(standardised_list):
        for j, rating in enumerate(claim):
            if rating in half_true:
                standardised_list[i][j] = "half true"
            elif rating in mostly_true:
                standardised_list[i][j] = "mostly true"
            elif rating in mostly_false:
                standardised_list[i][j] = "mostly false"
            elif rating in false:
                standardised_list[i][j] = "false"

    return standardised_list


def convert_to_numerical(processed_s_list):
    csv_columns = ["PolitiFact", "FactCheck.org", "The Washington Post", "The New York Times", "BBC"]

    # convert ps list to numerical
    for i, claim in enumerate(processed_s_list):
        for j, rating in enumerate(claim):
            if rating == "false":
                processed_s_list[i][j] = 1
            elif rating == "mostly false":
                processed_s_list[i][j] = 2
            if rating == "half true":
                processed_s_list[i][j] = 3
            elif rating == "mostly true":
                processed_s_list[i][j] = 4
            elif rating == "true":
                processed_s_list[i][j] = 5

    return processed_s_list


def calculate_percentages_pairs():
    directory = "data/consistency_csv/numerical"
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        # checking if it is a file and excluding initial file
        if os.path.isfile(file):
            with open(file, 'r') as file:
                csvreader = csv.reader(file)
                agree_counter = 0
                disagree_counter = 0
                close_counter = 0
                close_and_agree_counter = 0
                for i, row in enumerate(csvreader):
                    if i == 0:
                        print(row)
                    elif row[0] == row[1]:
                        agree_counter += 1
                        close_and_agree_counter += 1
                    else:
                        if abs(int(row[0]) - int(row[1])) <= 1:
                            close_counter += 1
                            close_and_agree_counter += 1
                        disagree_counter += 1
                total = agree_counter + disagree_counter
                print(f'Agree: {agree_counter}, Disagree: {disagree_counter}: total: {total}')
                print(f'Agreement: {agree_counter / total}')
                print(f'Close Amount: {close_counter} Close Agreement: {close_counter/total}')
                print(f'Close+Agree Amount: {close_and_agree_counter} Close+Agree Agreement: {close_and_agree_counter / total}')
                print("---")

#I was thinking of calculating the percentage that all fact checkers agreed in total.
# could look at the times all 3 agree, and when percentage at least 2 agree, and percentage none agree
# then could look at pairs and see total agree vs disagree
def calculate_percentages_general(file='numerical_ratings.csv'):
    with open(file, 'r') as file:
        csvreader = csv.reader(file)
        agree_counter = 0
        disagree_counter = 0
        close_counter = 0
        close_and_agree_counter = 0
        for i, row in enumerate(csvreader):
            if i == 0:
                print(row)
            rating_list = []
            for rating in row:
                if rating != '':
                    rating_list.append(rating)
            if len(rating_list) == 2:
                if rating[0] == rating[1]:
                    agree_counter += 1
                    close_and_agree_counter += 1
                else:
                    if abs(int(row[0]) - int(row[1])) <= 1:
                        close_counter += 1
                        close_and_agree_counter += 1
                    disagree_counter += 1
        total = agree_counter + disagree_counter
        print(f'Agree: {agree_counter}, Disagree: {disagree_counter}: total: {total}')
        print(f'Agreement: {agree_counter / total}')
        print(f'Close Amount: {close_counter} Close Agreement: {close_counter/total}')
        print(f'Close+Agree Amount: {close_and_agree_counter} Close+Agree Agreement: {close_and_agree_counter / total}')
        print("---")


def split_general_into_individual_categories(numerical_list):
    rating_dict = {1: "False", 2: "Mostly False", 3: "Half True", 4:"Mostly True", 5: "True"}
    for i in range(1, 6):
        category_list = []
        for j, row in enumerate(numerical_list):
            #may need to remove empty values, but I think krippendorf account for that. if i do need to remove, could create new_row list and append ratings to it, then if rating contains i append that to final list.
            # new_row = []
            # for rating in row:
            #     if rating != '':
            #         new_row.append(rating)
            for rating in row:
                if rating == '':
                    continue
                if int(rating) == i:
                    category_list.append(row)
                    break
        csv_columns = ["PolitiFact", "FactCheck.org", "The Washington Post", "The New York Times", "BBC"]
        csv_file = f'data/consistency_csv/individual_categories_general/{rating_dict[i]}.csv'
        with open(csv_file, 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_columns)
            for claim in category_list:
                writer.writerow(claim)



def main():
    args = sys.argv[1:]
    # parsing json - need to add this to own class
    # parse initial file so that future data could be appended
    # f = open('multiple.json', encoding='utf-8')
    # data = json.load(f)
    #
    # # claim_dict = create_fact_check_list(data)
    #
    # # getting final list after converting to csv
    # final_list = convert_to_csv(data, process=True)
    #
    # # getting final list by reading from interrater.csv
    # final_list = read_ratings_csv("processed_interrater.csv")
    #
    # standardised_list = standardise_ratings(final_list)
    #
    # write_standardised_to_csv(standardised_list)

    # standardised_list = read_ratings_csv("standardised_interrater.csv")

    # split_fact_checkers_into_two(standardised_list)

    # do additional processing to remove some stragglers
    # processed_s_list = process_standardised_list(standardised_list)
    # write_standardised_to_csv(processed_s_list, csv_file="sp_interrater.csv" )
    # split_fact_checkers_into_two(processed_s_list, directory="data/consistency_csv/sp", files_suffix="Consistency SP")

    # convert to numerical and write to csv
    # processed_s_list = read_ratings_csv("sp_interrater.csv")
    # numerical_list = convert_to_numerical(processed_s_list)
    # write_standardised_to_csv(numerical_list, csv_file="numerical_ratings.csv")
    # split_fact_checkers_into_two(numerical_list, directory="data/consistency_csv/numerical", files_suffix="Numerical")

    # calculate_percentages_pairs()

    # split general consistency ratings to simulate fleiss agreeemnt on individual categories for krippendorf
    numerical_list = read_ratings_csv("numerical_ratings_f.csv")
    split_general_into_individual_categories(numerical_list)

    # # number of website combinations
    # print(claim_dict.__len__())
    # # list of website combinations
    # print(claim_dict.keys())
    # # pretty print dictionary
    # pprint(claim_dict)
    # print("--------------")
    # consistency_dict = create_consistency_dict(claim_dict)
    # #
    # count_consistency_dict(consistency_dict)
    # #
    # # percentages_dict = create_percentages_dict(consistency_dict)

    """for key in percentages_dict.keys():
        print(key, percentages_dict[key])"""

    # calculate_reliability(consistency_dict)


if __name__ == "__main__":
    main()
