import requests
import csv
from pycoingecko import CoinGeckoAPI
import time
import argparse

parser = argparse.ArgumentParser(description="Turn off database inserts and lookups")
parser.add_argument('--nodb', dest='use_db', default=True, action='store_false')
args = parser.parse_args()
if args.use_db:
    import sqlite3

cg = CoinGeckoAPI()
# cg.ping()

def get_price_at_time(epoch: int):
    while True:
        try:
            ret = cg.get_coin_market_chart_range_by_id(id='ethereum', vs_currency='usd', from_timestamp=(epoch), to_timestamp=(epoch+3600))
            return ret
        except requests.exceptions.HTTPError:
            print("Sleeping..")
            time.sleep(3)

def main():
    with open("payouts.csv") as f:
        reader = list(csv.DictReader(f))

    if args.use_db:
        db_conn = sqlite3.connect('transactions.sqlite')
        db_cur = db_conn.cursor()

        completed_hashes_cur = db_cur.execute("select hash from hashes")
        completed_hashes = completed_hashes_cur.fetchall()
        completed_hashes = [x[0] for x in completed_hashes]

    with open("payouts_updated.csv", "w") as f:
        headers = list(reader[0].keys())
        headers.extend(['Price_ETH', 'Value_ETH'])

        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for row in reader:
            # skip rows that are already done
            hash = row['Transaction_Hash']
            if args.use_db and hash in completed_hashes:
                print(f"skipped hash {hash}")
                continue
            else:
                print(f'processing hash {hash}')

            epoch = int(row['Paid_On'])
            row['Price_ETH'] = get_price_at_time(epoch)['prices'][0][1]
            row['Value_ETH'] = row['Price_ETH'] * float(row['Amount_ETH'])
            writer.writerow(row)
            if args.use_db:
                db_cur.execute(f"insert into hashes (hash) VALUES (\"{hash}\")")
    
    if args.use_db:
        db_conn.commit()
        db_cur.close()
        db_conn.close()

if __name__ == '__main__':
    main()