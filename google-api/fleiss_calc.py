import json
from pprint import pprint
import os
import csv

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


def main():
    directory = 'fleiss_pair_files'

    f = open('multiple.json', encoding='utf-8')
    data = json.load(f)
    counter = 0
    for claim in data:
        counter += 1
        if 'claimReview' in claim:
            claimReview = claim['claimReview']
            publisherOne = claimReview[0]['publisher']['name']
            publisherTwo = claimReview[1]['publisher']['name']
            textualRatingOne = claimReview[0]['textualRating']
            textualRatingTwo = claimReview[1]['textualRating']

            for filename in os.listdir(directory): # loop through files in the folder
                file = os.path.join(directory, filename)
                if os.path.isfile(file):
                    if publisherOne and publisherTwo in filename:
                        with open(file, 'a') as f:
                            writer = csv.writer(f)
                            writer.writerow([textualRatingOne, textualRatingTwo])
                    else:
                        newFilename = publisherOne+publisherTwo
                        print(newFilename)
                        with open(directory + '/' + newFilename, 'w') as f:
                            writer = csv.writer(f)
                            writer.writerow([publisherOne, publisherTwo])
                            writer.writerow([textualRatingOne, textualRatingTwo])


            # print(publisherOne)
            # print(publisherTwo)
            # print(claimReview[0]['publisher']['name'])
            # print(claimReview[0]['textualRating'])
        #     quit()
        # pprint(claim)
    print(counter)

if __name__ == "__main__":
    main()
