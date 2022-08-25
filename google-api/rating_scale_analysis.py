import json
import os
from pprint import pprint
from matplotlib import pyplot as plt
import numpy as np
import csv

directory = 'data'

# iterate over files in that directory
for filename in os.listdir(directory):
    file = os.path.join(directory, filename)
    # checking if it is a file and excluding initial file
    if os.path.isfile(file):
        f = open(file, encoding='utf-8')
    else:
        continue

    data = json.load(f)

    year_dict = {}

    # some fact checks don't have review date for some reason. For these I could potentially look for the claim date and use that


    counter = 0
    review_counter = 0

    #convert ratings to lowercase and add each rating grouped into respective years
    for claim in data['claims']:
        year = ''
        for review in claim['claimReview']:
            counter = counter + 1
            # check if this claim actually has a reviewDate
            if 'reviewDate' in review.keys():
                review_counter = review_counter + 1
                year = review['reviewDate'][0:4]
                rating = review['textualRating']
                #convert rating to lowercase
                rating = rating.lower()
                if year not in year_dict.keys():
                    ratings_list = [rating]
                    year_dict[year] = ratings_list
                else:
                    year_list = year_dict[year]
                    year_list.append(rating)

    print(counter)
    print(review_counter)

    pprint(year_dict)

    frequency_dict = {}

    for year, ratings in year_dict.items():
        frequency = {}
        for rating in ratings:
            if rating in frequency:
                frequency[rating] += 1
            else:
                frequency[rating] = 1
        frequency_dict[year] = frequency

    # For any rating that has less than 5 frequency, remove it and add to 'other' rating
    for year, frequencies in frequency_dict.items():
        print(year)
        print(frequencies)
        ratings_to_delete = []
        other = 0
        for rating, frequency in frequencies.items():
            if frequency < 5:
                other += frequency
                ratings_to_delete.append(rating)
        frequencies['other'] = other
        for rating in ratings_to_delete:
            del frequencies[rating]

    pprint(frequency_dict)

    """for year, rating_frequencies in frequency_dict.items():
    
        plt.bar(rating_frequencies.keys(), rating_frequencies.values())
        plt.title('Frequency of ratings')
        plt.xlabel('Frequency')
        plt.ylabel('Rating')
        plt.xticks(rotation=90)
        plt.show()"""


    csv_columns = ['Year', 'Rating', 'Frequency']

    csv_file = f"frequency-csv/{filename}_frequency.csv"
    try:
        with open(csv_file, 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for year, ratings in frequency_dict.items():
                for rating, frequency in ratings.items():
                    writer.writerow({'Year': year, 'Rating': rating, 'Frequency': frequency})
    except IOError:
        print("I/O error")

