import json
import csv

with open('data/testFile.json', 'r', encoding="utf8") as f:  # load json file
    claims = json.load(f)

# get ratings of all textualRatings for entire file
all_ratings = {}
for claim in claims:
    for rating in claim['claimReview']:
        if 'textualRating' in rating.keys():
            if rating['textualRating'] in all_ratings.keys():
                all_ratings[rating['textualRating']] += 1
            else:
                all_ratings[rating['textualRating']] = 1
# with open('MultipleEntireFile.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['Textual Rating', 'Percentage'])
#     for rating in all_ratings.keys():
#         row = []
#         row.append(rating)
#         total_rating_sum = sum(list(all_ratings.values()))
#         perc = (all_ratings[rating]/total_rating_sum)*100
#         perc = round(perc, 2)
#         row.append(str(perc))
#         writer.writerow(row)

cleaned_claims = []

# cleaning data
for claim in claims:
    if 'claimant' in claim.keys():
        cleaned_claims.append(claim)

# get all the unique claimants
claimants = []
for claim in cleaned_claims:
    if claim['claimant'] not in claimants:
        claimants.append(claim['claimant'])


# getting all the unique textual ratings for claimants and calculating their frequency
ratings_with_frq = {}


for claimant in claimants:
    ratings_with_frq[claimant] = {}
    for claim in cleaned_claims:
        if claim['claimant'] == claimant:
            for rating in claim['claimReview']:
                if 'textualRating' in rating.keys():
                    if rating['textualRating'] in ratings_with_frq[claimant].keys():
                        ratings_with_frq[claimant][rating['textualRating']] += 1
                    else:
                        ratings_with_frq[claimant][rating['textualRating']] = 1

print(ratings_with_frq)
# saving data to a csv file
# with open('noMultiple.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Claimant', 'Total no. of entries' 'Rating 1', 'Rating 2', 'Rating 3', 'Rating 4', 'Rating 5', 'Rating 6',
#                     'Rating 7', 'Rating 8', 'Rating 9', 'Rating 10'])
#     for claimant in ratings_with_frq.keys():
#         row = []
#         row.append(claimant)
#         total_rating_sum = sum(list(ratings_with_frq[claimant].values()))
#         row.append(str(total_rating_sum))
#         for rating in ratings_with_frq[claimant].keys():
#             perc = ((ratings_with_frq[claimant]
#                     [rating])/(total_rating_sum))*100
#             perc = round(perc, 2)
#             row.append(rating+"( "+str(perc)+"% )")
#         writer.writerow(row)
#     print('Data saved to file')
