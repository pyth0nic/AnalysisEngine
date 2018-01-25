from JobWorkers.FileLinkCrawler import FileLinkCrawler

class CompanyWorker:

    def file_crawl(self, q, symbol, base_url):
        print("STARTING" + symbol)
        print("crawling" + symbol + " " + base_url)
        crawler = FileLinkCrawler()
        results = crawler.start_spider(symbol, base_url)
        q.put({"symbol": symbol, "results": results})
        return
