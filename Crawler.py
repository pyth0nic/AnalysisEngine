import scrapy
from scrapy.spiders import CrawlSpider, Rule

from scrapy.linkextractor import LinkExtractor
from scrapy.selector import Selector

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


data=[]


class MySpider(CrawlSpider):
    name = 'spider'

    crawled_ids = set()

    def start_requests(self):

        yield scrapy.Request(self.start_urls[0], self.parse)

    def parse(self, response):
        body = Selector(text=response.body)

        pdfs = body.css('a[href$=".pdf"]::attr(href)').extract()
        csvs = body.css('a[href$=".csv"]::attr(href)').extract()
        xl1 = body.css('a[href$=".xls"]::attr(href)').extract()
        xl2 = body.css('a[href$=".xlsx"]::attr(href)').extract()
        doc1 = body.css('a[href$=".doc"]::attr(href)').extract()
        doc2 = body.css('a[href$=".docx"]::attr(href)').extract()
        link_objs = [pdfs, csvs, xl1, xl2, doc1, doc2]

        link_extractor = LinkExtractor(allow=self.allowed_domains)
        next_links = [link.url for link in link_extractor.extract_links(response) if not self.is_extracted(link.url)]

        # Crawl the filtered links
        for link in next_links:
            yield scrapy.Request(link, self.parse)

        def get_links(obj):
            print(obj)
            if obj:
                for link in obj:
                    data.append(link)
            return

        [get_links(obj) for obj in link_objs]

    def is_extracted(self, url):
        if id not in self.crawled_ids:
            self.crawled_ids.add(url)
            return False
        return True


###
### usage example: start_spider("BIT","http://www.biotron.com.au")
### returns list of pdf files
###
def start_spider(symbol, base_url):
    domain = base_url.replace("http://", "").replace("https://", "").replace("www.", "").replace("/", "")
    try:
        process = CrawlerProcess(get_project_settings())
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        })

        process.crawl(MySpider, start_urls=[base_url], allowed_domains=[domain], ROBOTSTXT_OBEY=false,
                      DOWNLOAD_DELAY=0.25)
        process.start()
        print("done crawling")
    except Exception as e:
        print("Crawling ERROR " + symbol)
        print(str(e))
    return data
