import concurrent.futures
from Database import DBUrls
from JobWorkers.FileLinkCrawler import FileLinkCrawler
import asyncio


class CompanyWorker:

    async def crawl(self, symbol, base_url, loop):
        print("crawling" + symbol + " " + base_url)
        crawler = FileLinkCrawler()
        results = await loop.run_in_executor(None, crawler.start_spider, symbol, base_url)
        print(results)


class CompanySupervisor:

    def run_batch(self):
        db = DBUrls()
        data = db.get_stock_list(limit=1)

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            loop = asyncio.get_event_loop()
            tasks = [
            ]
            for line in data:
                worker = CompanyWorker()
                tasks.append(
                    asyncio.ensure_future(worker.crawl(line[0], line[1], loop))
                )
            loop.run_until_complete(asyncio.wait(tasks))
            loop.close()


c = CompanySupervisor()
c.run_batch()
