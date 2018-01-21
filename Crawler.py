import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from Database import DBUrls

from scrapy.linkextractor import LinkExtractor
from scrapy.selector import Selector

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.http import Request


data=[]
domains=[]

class MySpider(CrawlSpider):

    name = 'spider'

    crawled_ids = set()

    def start_requests(self):

        yield scrapy.Request(self.start_urls[0], self.parse)

    def parse(self, response):
        body = Selector(text=response.body)
        pdfs = body.css('a[href$=".pdf"]::attr(href)').extract()
        link_extractor = LinkExtractor(allow=self.allowed_domains)
        next_links = [link.url for link in link_extractor.extract_links(response) if not self.is_extracted(link.url)]

        # Crawl the filtered links
        for link in next_links:
            yield scrapy.Request(link, self.parse)

        if pdfs:
            for link in pdfs:
                data.append(link)

    def is_extracted(self, url):
        if id not in self.crawled_ids:
            self.crawled_ids.add(url)
            return False
        return True

def start_spider(symbol, base_url):
    domain=base_url.replace("http:\/\/www","").replace("https:\/\/www.","").replace("\/","")
    process = CrawlerProcess(get_project_settings())
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    })

    process.crawl(MySpider, start_urls=[base_url], allowed_domains=[base_url])
    process.start()
    print("done crawling")
    for i in data:
        print(i)

start_spider("BIT","http://www.biotron.com.au")