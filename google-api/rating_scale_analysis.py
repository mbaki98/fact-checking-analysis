import json
import os
from pprint import pprint
from matplotlib import pyplot as plt
import numpy as np

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

for year, rating in year_dict.items():
    # Creating histogram
    plt.style.use('ggplot')
    fig, ax = plt.subplots()
    ax.hist(rating)

    # Show plot
    plt.show()

