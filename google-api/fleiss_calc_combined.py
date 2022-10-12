import json
from pprint import pprint
import os
import csv
from util.politics_claimant_categoriser import return_category, get_politician_list
from consistency import process_ratings

'''
This file goes through the multiple.json file containing all claims with multiple fact checkers for one claim

Loop through multiple.json

    open claim

        store publisher one
        store publisher two
        if in 'fleiss_pair_files' folder, a file already exists containing both publisher one and two
            store the textual rating for publisher one
            store the textual rating for publisher two
        else
            create a new csv file with columns for publisher one and two
            write the textual rating for publisher one and two accordingly

Notes: claimReview is an array of 2 objects
[] is an array
{} is an object
'''


def standardise_rating(rating):
    false = ["pants on fire", "four pinocchios", "lie of the year", "no evidence", "very wrong", "pants on fire",
             "wrong", "not what X said", "unsupported","hasn't said why", "this lacks evidence.", "no evidence provided",
             "not what gm says", "no early timeline", "wasn't a fixer-upper economy", "this is unknown.", "gov't data shows otherwise", "not historic or final", "misuse of irs data"
             ,"obama did well too", "doj: killed, not murdered"]
    mostly_false = ["mostly false", "three pinocchios", "misrepresents the record",
                     "inflated", "misleading", "experts disagree",
                      "numbers in dispute", "needs more context", "in dispute",
                    "experts: not a bailout", "not the whole story", "chant is routine",
                    "this is misleading.", "exagerated",
                    "they are not eligible", "we explain the research", "exaggerates",
                    "can't for domestic group", "distorts the facts", "pricew reflect too high supply", "somewhat true",
                    "partly true", "not what zelensky said", "mental health experts say no", "small impact for most"]
    half_true = ["half true", "half right", "half-right", "half-true", "hard to verify",
                 "true, but cherry picked", "cherry picked", "half right",
                  "way early to say","greatly oversold", "two pinocchios","this is exaggerated."
                 "partly right, needs context", "needs context", "ignores coronavirus job losses",
                 "migrants not driving surge", "cherry picks", "true, but cherry-picked.", "not in every state",
                  "missing context", "out of context", "exaggerated", "spins the facts"]
    mostly_true = ["mostly true", "one pinocchio", "largely correct", "largely correct","partly false", "the majority are suicides.", "somewhat false", "depends on who's counting"]
    true = ["true", "gepetto checkmark", "accurate"]
    if rating in false:
        return 'false'
    elif rating in mostly_false:
        return 'mostly false'
    elif rating in half_true:
        return 'half true'
    elif rating in mostly_true:
        return 'mostly true'
    elif rating in true:
        return 'true'
    else:
        return rating


def check_file(directory, claimant):
    for filename in os.listdir(directory):
        if claimant in filename:
            return filename

    return 0


def main():
    directory = 'fleiss_files_combined_final'

    f = open('multiple.json', encoding='utf-8')
    data = json.load(f)
    for claim in data:
        if 'claimant' not in claim:
            continue
        claimant = claim['claimant'].lower()
        claimant = return_category(claimant)
        if 'claimReview' in claim:
            claimReview = claim['claimReview']
            publisherOne = claimReview[0]['publisher']['name']
            publisherTwo = claimReview[1]['publisher']['name']
            textualRatingOne = standardise_rating(process_ratings(claimReview[0]['textualRating'].lower()))
            textualRatingTwo = standardise_rating(process_ratings(claimReview[1]['textualRating'].lower()))

            if publisherOne == publisherTwo:
                continue

            print('number of publishers: ' + str(len(claimReview)))
            # get the number of publishers
            nPublishers = len(claimReview)

            # if 3 then go thru pairs of files
            if nPublishers == 3:
                textualRatingThree = standardise_rating(process_ratings(claimReview[2]['textualRating'].lower()))
                fileFound = check_file(directory, claimant)
                if fileFound == 0: # doesnt exist
                    filename = claimant
                    with open(directory + '/' + filename, 'w', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([textualRatingOne, textualRatingTwo, textualRatingThree])
                else: # exists
                    with open(directory + '/' + fileFound, 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([textualRatingOne, textualRatingTwo, textualRatingThree])

            else:
                fileFound = check_file(directory, claimant)
                if fileFound == 0: # doesnt exist
                    filename = claimant
                    with open(directory + '/' + filename, 'w', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([textualRatingOne, textualRatingTwo])
                else: # exists
                    with open(directory + '/' + fileFound, 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([textualRatingOne, textualRatingTwo])



if __name__ == "__main__":
    main()
