import json
import os
from pprint import pprint
from matplotlib import pyplot as plt
import numpy as np
import csv

f = open('data/politifact.json', encoding='utf-8')
data = json.load(f)

year_dict = {}

# some fact checks don't have review date for some reason. For these I could potentially look for the claim date and use that

counter = 0
review_counter = 0

for claim in data['claims']:
    year = ''
    for review in claim['claimReview']:
        counter = counter + 1
        # check if this claim actually has a reviewDate
        if 'reviewDate' in review.keys():
            review_counter = review_counter + 1
            year = review['reviewDate'][0:4]
            rating = review['textualRating']
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


"""for year, rating_frequencies in frequency_dict.items():

    plt.bar(rating_frequencies.keys(), rating_frequencies.values())
    plt.title('Frequency of ratings')
    plt.xlabel('Frequency')
    plt.ylabel('Rating')
    plt.xticks(rotation=90)
    plt.show()"""


csv_columns = ['Year', 'Rating', 'Frequency']


csv_file = "politifact_frequency.csv"
try:
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for year, ratings in frequency_dict.items():
            for rating, frequency in ratings.items():
                writer.writerow({'Year': year, 'Rating': rating, 'Frequency': frequency})
except IOError:
    print("I/O error")