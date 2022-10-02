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
            textualRatingOne = claimReview[0]['textualRating'].lower()
            textualRatingTwo = claimReview[1]['textualRating'].lower()

            if publisherOne == publisherTwo:
                continue

            print('number of publishers: ' + str(len(claimReview)))
            # get the number of publishers
            nPublishers = len(claimReview)

            # if 3 then go thru pairs of files
            if nPublishers == 3:
                publisherThree = claimReview[2]['publisher']['name']
                textualRatingThree = claimReview[2]['textualRating'].lower()
                comboOne = publisherOne + publisherTwo
                comboTwo = publisherOne + publisherThree
                comboThree = publisherTwo + publisherThree

                fileOne = os.path.join(directory, comboOne)
                fileTwo = os.path.join(directory, comboTwo)
                fileThree = os.path.join(directory, comboThree)

                if os.path.isfile(fileOne):
                    with open(fileOne, 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([textualRatingOne, textualRatingTwo])
                else:
                    with open(directory + '/' + comboOne, 'w', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([publisherOne, publisherTwo])
                        writer.writerow([textualRatingOne, textualRatingTwo])

                if os.path.isfile(fileTwo):
                    with open(fileTwo, 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([textualRatingOne, textualRatingThree])
                else:
                    with open(directory + '/' + comboTwo, 'w', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([publisherOne, publisherThree])
                        writer.writerow([textualRatingOne, textualRatingThree])

                if os.path.isfile(fileThree):
                    with open(fileThree, 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([textualRatingTwo, textualRatingThree])
                else:
                    with open(directory + '/' + comboThree, 'w', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([publisherTwo, publisherThree])
                        writer.writerow([textualRatingTwo, textualRatingThree])
            else:
                filename = publisherOne + publisherTwo
                file = os.path.join(directory, filename)
                if os.path.isfile(file):
                    with open(file, 'a', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([textualRatingOne, textualRatingTwo])
                else:
                    with open(directory + '/' + filename, 'w', encoding='UTF8', newline='') as f:
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
