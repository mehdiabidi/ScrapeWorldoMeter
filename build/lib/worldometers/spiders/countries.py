import scrapy


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath('//td/a')
        for country in countries:
            country_name = country.xpath('.//text()').get()
            country_link = country.xpath('.//@href').get()

            # yield scrapy.Request(url=absolute_url)
            # yield scrapy.Request(url=absolute_url)
            yield response.follow( url = country_link, callback = self.parse_countries, meta = { 'country_name' : country_name})
            # yield {
            #     'absolute_url':absolute_url
            # }
        # pass
    def parse_countries(self, response):
        country_name = response.request.meta['country_name']
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        print(len(rows))
        if len(rows)<2:
            exit(0)
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yield {
                'country_name' : country_name,
                'year' : year,
                'population' : population
            }
