import json
from pprint import pprint
from util.nofils_claimant_categoriser import return_category, get_politician_list


def main():
    with open('data/usatoday.json', 'r', encoding="utf8") as f:  # load json file
        data = json.load(f)

    claims = data['claims']  # get all the claims
    cleaned_claims = []

    # cleaning data
    for claim in claims:
        if 'claimant' in claim.keys():
            cleaned_claims.append(claim)

    # get ratings of all textualRatings for entire file
    all_ratings = {}
    for claim in claims:
        if 'textualRating' in claim['claimReview'][0].keys():
            if claim['claimReview'][0]['textualRating'] in all_ratings.keys():
                all_ratings[claim['claimReview'][0]['textualRating']] += 1
            else:
                all_ratings[claim['claimReview'][0]['textualRating']] = 1
    # with open('noMultipleEntireFile.csv', 'w', newline='') as f:
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
                if 'textualRating' in claim['claimReview'][0].keys():
                    if claim['claimReview'][0]['textualRating'] in ratings_with_frq[claimant].keys():
                        ratings_with_frq[claimant][claim['claimReview']
                        [0]['textualRating']] += 1
                    else: 
                        ratings_with_frq[claimant][claim['claimReview']
                        [0]['textualRating']] = 1

    pprint(ratings_with_frq)
    # saving data to a csv file
    # with open('multipleData.csv', 'w', newline='') as file:
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


if __name__ == "__main__":
    main()
