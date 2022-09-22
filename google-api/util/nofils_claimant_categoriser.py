import csv


def return_category(claim: str):
    claim = claim.lower()
    social_media = ['social media', 'facebook', 'twitter', 'instagram', 'tweet', 'fb', 'tweet', 'social', 'tiktok.com',
                    'tiktok', 'i.imgur.com', 'social media users', 'Social media users', 'social media user', 'Social media user', 'post', 'public', 'video', 'image', '8shit.net']
    multiple_source = ['mutliple sources', 'multiple resources', 'multiples sources', 'various sources',
                       'sources multiples', 'multiple people', 'multiple source', 'multiple', 'several', 'مصادر عدّة',
                       'عدة مصادر', 'مصادر عدة', 'أطراف عدّة']
    youtube = ['youtube', 'youtu']
    whatsapp = ['whatsapp']
    trump = ['donald trump', 'donald j trump', 'donald j. trump', 'trump white house', 'trump campaign',
             'donaldjtrump.com', 'team trump', 'the trump campaign', 'newsdonaldtrumps.com', 'president trumps lawyers',
             'truetrumpers.com']
    biden = ['joe biden', 'biden']
    news_sites = ['cbsnews.us', 'world news daily report','babylonbee.com','thereisnews.com','al jazeera','realrawnews.com', 'duffelblog.com', 'southendnewsnetwork.net', 'your news wire', 'yournewswire.com',
                  'huzlers.com', 'the times', 'boom', 'dailyexpose.Uk', 'the expose', 'thegatewaypundit.com',
                  'rumble.com', 'daily express', 'bitchute.com', 'real raw news', 'the telegraph', 'the guardian',
                  'beforeitsnews.com', 'redvoicemedia.com', 'daily mail', 'the sun', 'the gateway pundit', 'tvc news',
                  'the daily expose', 'daily expose', 'bestnewshere.com', 'sky news', 'the africa report',
                  'thetruereporter.com', 'the independent', 'daily telegraph', 'daily mail', 'infowars', 'infowars.com',
                  'dailyexpose.co.uk', 'bbc news', 'trend news', 'africanews', 'worldnewsdailyreport.com',
                  'worldgreynews.com', 'worldnewsdailyreport', 'world grey news', 'westernjournal.com', 'the mirror',
                  'the herald', 'the daily telegraph', 'skyline news', 'sky news kenya', 'naturalnews.com', 'daily mirror', 'theexpose.uk', 'natural news', 'mail online', 'gb news', 'zee news', 'bbc', 'a nigerian newspaper', 'cape talk']
    viral_post = ['viral image', 'viral video', 'viral post', 'viral rumor', 'viral quote', 'viral photo', 'viral footage', 'viral images', 'viral story', 'viral meme']
    pol_info = get_politician_list()
    # returns true if claim contains any elements from list social media
    if [element for element in social_media if (element in claim)]:
        return 'social media'
    if [element for element in multiple_source if (element in claim)]:
        return 'multiple sources'
    if [element for element in youtube if (element in claim)]:
        return 'youtube'
    if [element for element in whatsapp if (element in claim)]:
        return 'whatsapp'
    # if [element for element in trump if (element in claim)]:
    #     return 'donald trump'
    # if [element for element in biden if (element in claim)]:
    #     return 'joe biden'
    if [element for element in pol_info.keys() if (element in claim)] or 'labour' or 'labor' or 'Labour' or 'Conservative' or 'conservative' or 'Democratic' or 'democratic' in claim:
        for key, value in pol_info.items():
            if key in claim:
                # print('key: '+key)
                # print('claim: '+claim)
                if "republican" in value.lower():
                    return 'Republicans'
                else:
                    return 'Democrats'
        # return 'US politicians - '
    if [element for element in news_sites if (element in claim)]:
        return 'news sites'

    # for key, value in pol_info.items():
    #     if key in claim:
    #         # print('key: '+key)
    #         # print('claim: '+claim)
    #         if "republican" in value.lower():
    #             return 'Republicans'
    #         else:
    #             return 'Democrats'

    return claim


def get_politician_list():
    with open('data/extra/politicians.csv', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)

    name_list = {}
    for politician in data:
        name_list[politician[0].lower()] = politician[9].lower()
        # name_list.append(tuple([politician[0].lower(), politician[9].lower()]))

    # print(name_list)
    # for key, value in name_list.items():
    #     print(key)
    #     if (value == 'democratic party'):
    #         print('dem dog')
    #     else:
    #         print('repub pig')
    return name_list
