import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        max_page = 6
        #We send a post request to https://www.thegioididong.com/aj/CategoryV5/Product
        #Category:42
        # Manufacture:0
        # PriceRange:0
        # Feature:0
        # Property:0
        # OrderBy:0
        # PageSize:30
        # PageIndex:x
        # Where page size change from 1 to 5
        # After that we got a list of links that we move to another crawler
        urls = ['https://www.thegioididong.com/dtdd/oppo-f5-6gb']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        count = 0
        path = '/home/dangpham/Dann/source_code/scrapy/crawl_tgdd/html-pages/'
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(path+filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

