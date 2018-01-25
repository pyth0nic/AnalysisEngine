import csv
import Data.Database


def get_csv_data(filename):
    data=[]
    with open(filename, "r+") as file:
        reader = csv.reader(file, delimiter=",")

        for v in reader:
            data.append(v)
    return data


stock_data = get_csv_data("../Small_Caps2.csv")
stock_urls = get_csv_data("../Small_Caps_urls.csv")

db = Data.Database.DBUrls()

for row in stock_data:
    db.create_stock_entry(description=row[0].rstrip(), symbol=row[1], url="")

for row in stock_urls:
    print(row)
    db.update_stock_base_url(symbol=row[0],url=row[1])

