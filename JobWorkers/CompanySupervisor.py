from Data.Database import DBUrls
from JobWorkers.CompanyWorker import CompanyWorker
from multiprocessing import Manager
import multiprocessing as mp


class CompanySupervisor:

    def run_batch(self):
        db = DBUrls()
        data = db.get_stock_list_today(limit=10)
        if not data:
            return

        q = Manager().Queue()
        urls = []
        plist = []
        print(data)
        for line in data:
            worker = CompanyWorker()
            p = mp.Process(target=worker.file_crawl, args=(q, line[0], line[1]))
            plist.append(p)
            p.start()

        for p in plist:
            p.join()

        urls.append(q.get())

        for url in urls:
            db.insert_stock_urls(url["symbol"], url["results"])

        return self.run_batch()
