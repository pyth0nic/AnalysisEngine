import requests
import asyncio
from bs4 import BeautifulSoup
import concurrent.futures
from Data.Database import DBUrls
import json
urls=[]

async def fetch_url(symbol, executor, loop):
    print("task started" + symbol)

    def parse_response(response, symbol):
        soup = BeautifulSoup(response.text, 'html.parser')
        profile = soup.find(class_="asset-profile-container")
        links = profile.find_all("a")
        for link in links:
            print(link)
            if "http:" in link["href"] or "https:" in link["href"]:
                urls.append({symbol: link["href"]})

    try:
        url = "https://au.finance.yahoo.com/quote/%s.AX/profile?p=%s.AX" % (symbol, symbol)
        response = await loop.run_in_executor(None, requests.get, url)
        parse_response(response, symbol)
    except Exception as e:
        print(symbol + "\tFailed")
        print(str(e))

async def fetch_url_asx(symbol, executor, loop):
    print("task started asx" + symbol)

    def parse_response(_response):
        payload = json.loads(_response.text)
        print(payload)
        urls.append({symbol:payload["web_address"]})

    try:
        url = "https://www.asx.com.au/asx/1/company/%s" % symbol
        response = await loop.run_in_executor(None, requests.get, url)
        parse_response(response)
    except Exception as e:
        print(symbol + "\tFailed")
        print(str(e))


def runner(db):
    data = db.get_stock_list()
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
        ]
        for line in data:
            tasks.append(
                asyncio.ensure_future(fetch_url_asx(line[0], executor, loop))
            )
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()


def to_db(db):
    print("starting insertion")
    print(urls)
    for i in urls:
        symbol=[k for k in i.keys()][0]
        url=[k for k in i.values()][0]
        db.update_stock_base_url(symbol, url)

def update_urls():
    db=DBUrls()
    runner(db)
    to_db(db)