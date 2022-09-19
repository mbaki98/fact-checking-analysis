import csv

def return_category(claim: str, politicians: set, full):
    claim = claim.lower()
    social_media = ['social media', 'facebook', 'twitter', 'instagram', 'tweet', 'fb', 'tweet', 'social', 'tiktok.com',
                    'tiktok', 'i.imgur.com']
    multiple_source = ['mutliple sources', 'multiple resources', 'multiples sources', 'various sources',
                       'sources multiples', 'multiple people', 'multiple source', 'multiple', 'several', 'مصادر عدّة',
                       'عدة مصادر', 'مصادر عدة', 'أطراف عدّة']
    youtube = ['youtube', 'youtu']
    whatsapp = ['whatsapp']
    trump = ['donald trump', 'donald j trump', 'donald j. trump', 'trump white house', 'trump campaign',
             'donaldjtrump.com', 'team trump', 'the trump campaign', 'newsdonaldtrumps.com', 'president trumps lawyers',
             'truetrumpers.com']
    biden = ['joe biden', 'biden']
    news_sites = ['cbsnews.us', 'realrawnews.com', 'duffelblog.com', 'southendnewsnetwork.net', 'your news wire', 'yournewswire.com',
                  'huzlers.com', 'the times', 'boom', 'Dailyexpose.Uk', 'the expose', 'thegatewaypundit.com',
                  'rumble.com', 'daily express', 'bitchute.com', 'real raw news', 'the telegraph', 'the guardian',
                  'beforeitsnews.com', 'redvoicemedia.com', 'daily mail', 'the sun', 'the gateway pundit', 'tvc news',
                  'the daily expose', 'daily expose', 'bestnewshere.com', 'sky news', 'the africa report',
                  'thetruereporter.com', 'the independent', 'daily telegraph', 'daily mail', 'infowars', 'infowars.com',
                  'dailyexpose.co.uk', 'bbc news', 'trend news', 'africanews', 'worldnewsdailyreport.com',
                  'worldgreynews.com', 'worldnewsdailyreport', 'world grey news', 'westernjournal.com', 'the mirror',
                  'the herald', 'the daily telegraph', 'skyline news', 'sky news kenya', 'naturalnews.com', 'daily mirror', 'theexpose.uk', 'natural news', 'mail online']

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
    if [element for element in news_sites if (element in claim)]:
        return 'news site'
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
