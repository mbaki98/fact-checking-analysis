import scrapy


class PolitifactSpider(scrapy.Spider):
    name = 'politifact'
    allowed_domains = ['politifact.com']
    start_urls = ['https://www.politifact.com/factchecks/list/?page=1&']

    def parse(self, response):
        print("in parse")
        for item in response.css('li.o-listicle__item'):
            yield {
                "statement_name": item.css('a.m-statement__name::text').get().strip(),
                "statement_desc": item.css('div.m-statement__desc::text').get().strip(),
                "statement_quote": item.css('div.m-statement__quote a::text').get().strip(),
                "date_posted": item.css('footer.m-statement__footer::text').get().strip(),
                "rating": item.css('div.c-image img::attr(alt)').get().strip()
            }
        for button in response.css('a.c-button.c-button--hollow'):
            text = button.css('::text').get().strip()
            if text == 'Next':
                href = button.css('::attr(href)').get()
                link = "https://www.politifact.com/factchecks/list/" + href
                yield response.follow(link, callback=self.parse)



