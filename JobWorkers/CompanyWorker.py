from JobWorkers.FileLinkCrawler import FileLinkCrawler

class CompanyWorker:

    @staticmethod
    def file_crawl(q, symbol, base_url):
        print("crawling" + symbol + " " + base_url)
        crawler = FileLinkCrawler()
        results = crawler.start_spider(symbol, base_url)
        q.put({"symbol": symbol, "results": results})
        return
