import csv
import re
import validators

def return_category(claim: str, politicians: set, full):
    claim = claim.lower()
    social_media = ['social media', 'facebook', 'twitter', 'instagram', 'tweet', 'fb', 'tweet', 'social', '']
    multiple_source = ['mutliple sources', 'multiple resources', 'multiples sources', 'various sources',
                       'sources multiples', 'multiple people', 'multiple source', 'multiple', 'several', 'مصادر عدّة', 'عدة مصادر', 'مصادر عدة', 'أطراف عدّة']
    youtube = ['youtube', 'youtu']
    whatsapp = ['whatsapp']
    trump = ['donald trump', 'donald j trump', 'donald j. trump']
    biden = ['joe biden']
    # returns true if claim contains any elements from list social media
    if [element for element in social_media if (element in claim)]:
        return 'social media'
    if [element for element in multiple_source if (element in claim)]:
        return 'multiple sources'
    if [element for element in youtube if (element in claim)]:
        return 'youtube'
    if [element for element in whatsapp if (element in claim)]:
        return 'whatsapp'
    if [element for element in trump if (element in claim)]:
        return 'donald trump'
    if [element for element in biden if (element in claim)]:
        return 'joe biden'
    if [element for element in politicians if (element in claim)]:
        return 'US politicians'
    else:
        return claim


def get_politician_list():
    with open('data/extra/politicians.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)

    name_list = []
    for politician in data:
        name_list.append(politician[0].lower())

    return set(name_list)
