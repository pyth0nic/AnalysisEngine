import psycopg2


class db:
    _conn_string = "host='localhost' port='' dbname='postgres' user='postgres' password='postgres'"

    def __init__(self):
        self._conn = psycopg2.connect(self._conn_string)
        self._cur = self._conn.cursor()

    def __del__(self):
        self._cur.close()
        self._conn.close()


class DBUrls(db):

    def create_web_entry(self, symbol, url, data):
        self._cur.execute("INSERT INTO stock_related_urls (symbol, url, data) VALUES ('%s', '%s','')" % (symbol,url))
        self._conn.commit()

    def create_stock_entry(self,symbol, description, url):
        self._cur.execute("INSERT INTO stocks (symbol, description, base_url) \
        VALUES ('%s','%s','%s');" % (symbol,description,url))
        self._conn.commit()

    def update_stock_base_url(self,symbol,url):
        self._cur.execute("UPDATE stocks SET base_url='%s' WHERE symbol='%s';" % (url, symbol))
        self._conn.commit()

    def get_stock_list(self, limit=5):
        self._cur.execute("SELECT * from stocks where base_url<>'' limit %d;" % limit)
        rows = self._cur.fetchall()
        if rows:
            return rows

    def get_stock_list_today(self, limit=5):
        self._cur.execute("select distinct public.stocks.symbol, public.stocks.base_url \
        FROM public.stocks left join public.stock_related_urls on \
        public.stock_related_urls.symbol= public.stocks.symbol \
        where (public.stock_related_urls.last_date::timestamp::date > now()::date - 1 \
        and public.stock_related_urls.last_date::timestamp::date < now()::date - 1) or \
        public.stock_related_urls.last_date is null limit %d;" % limit)
        rows = self._cur.fetchall()
        if rows:
            return rows

    def insert_stock_urls(self, symbol, rows):
        for row in rows:
            self._cur.execute("INSERT INTO stock_related_urls (symbol, url, referer) VALUES (%s,%s,%s)"
                              , (symbol, row["url"], row["referer"]))
        self._conn.commit()

#if __name__=="__main__":
    #print("start")
    #db = DBUrls()
    #db.create_entry("BHP","www.bhp.com.au",None)