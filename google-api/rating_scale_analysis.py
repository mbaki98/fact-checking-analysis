import json
import os
from pprint import pprint
from matplotlib import pyplot as plt
import numpy as np
import csv
import pandas as pd
import re


# processes ratings such that "false - not enough evidence" is converted to "false"
def process_rating(rating: str):
    ratings = re.split("\W+|_", rating)
    # print(ratings)
    # Converting AAP to politifact. Somewhat and mostly combined to mostly. Partly true/false combined to half true
    if ratings[0] == 'false':
        return "false"
    elif ratings[0] == "partly":
        return "half true"
    elif ratings[0] == "somewhat" or ratings[0] == "mostly":
        if ratings[1] == "false":
            return "mostly false"
        elif ratings[1] == "true":
            return "mostly true"
    elif ratings[0] == "true":
        return "true"
    else:
        return rating


def rating_scale():
    directory = 'data'

    website_ratings_frequency = {}
    # iterate over files in that directory
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        # checking if it is a file and excluding initial file
        if os.path.isfile(file) and filename:
            f = open(file, encoding='utf-8')
        else:
            continue

        data = json.load(f)
        year_dict = {}
        # some fact checks don't have review date for some reason. For these I could potentially look for the claim date and use that
        counter = 0
        review_counter = 0

        # convert ratings to lowercase and add each rating grouped into respective years
        for claim in data['claims']:
            year = ''
            for review in claim['claimReview']:
                counter = counter + 1
                # check if this claim actually has a reviewDate
                if 'reviewDate' in review.keys():
                    review_counter = review_counter + 1
                    year = review['reviewDate'][0:4]
                    rating = review['textualRating']
                    # convert rating to lowercase
                    rating = rating.lower()
                    rating = process_rating(rating)
                    if year not in year_dict.keys():
                        ratings_list = [rating]
                        year_dict[year] = ratings_list
                    else:
                        year_list = year_dict[year]
                        year_list.append(rating)

        # print(counter)
        # print(review_counter)

        # pprint(year_dict)

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
            # print(year)
            # print(frequencies)
            ratings_to_delete = []
            other = 0
            for rating, frequency in frequencies.items():
                if frequency < 20:
                    other += frequency
                    ratings_to_delete.append(rating)
            frequencies['other'] = other
            for rating in ratings_to_delete:
                del frequencies[rating]

        # pprint(frequency_dict)

        write_to_csv(filename, frequency_dict)
        website_ratings_frequency[filename[:-5]] = frequency_dict

    return website_ratings_frequency


def plot_results(frequency_dict: dict):
    for year, rating_frequencies in frequency_dict.items():
        plt.bar(rating_frequencies.keys(), rating_frequencies.values())
        plt.title('Frequency of ratings')
        plt.xlabel('Frequency')
        plt.ylabel('Rating')
        plt.xticks(rotation=90)
        plt.show()


# write each website and its ratings into separate csv files
def write_to_csv(filename, frequency_dict: dict):
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


# write all the websites and their ratings and their frequencies into one massive csv file
def write_all_ratings_to_csv(website_ratings_frequency: dict):
    csv_columns = ['Website', 'Year', 'Rating', 'Frequency']
    csv_file = f"frequency-csv/rating_scales.csv"
    pprint(website_ratings_frequency)

    try:
        with open(csv_file, 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()

            for website, year_dict in website_ratings_frequency.items():
                for year, freq_dict in year_dict.items():
                    for rating, frequency in freq_dict.items():
                        writer.writerow({'Website': website, 'Year': year, 'Rating': rating, 'Frequency': frequency})
    except IOError:
        print("I/O error")


def convert_website_ratings_frequency_to_csv(website_ratings_frequency: dict):
    print(website_ratings_frequency)
    df = pd.json_normalize(website_ratings_frequency)
    print(df)


def main():
    website_ratings_frequency = rating_scale()
    write_all_ratings_to_csv(website_ratings_frequency)


if __name__ == "__main__":
    main()
