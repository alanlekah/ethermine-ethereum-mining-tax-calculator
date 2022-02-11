import csv
from app import parse_args, coinapi, sqlite


def main():
    args = parse_args.parse_args()

    # initialize the CAPI (coin gecko API wrapper)
    # TODO - update to use inject
    c_api = coinapi.CoinAPI()

    with open(args.inputfile) as f:
        reader = list(csv.DictReader(f))

    if args.dbfile:
        # initialize the sqlite api (sqlite3 wrapper)
        sql_api = sqlite.SQLiteDB(args.dbfile)

        # create the table to store transaction hashes if it doesnt exist
        sql_api.create_table_if_not_exists()

        # if a sqlite file specified, get the completed hashes
        completed_hashes = sql_api.get_completed_hashes_from_db()

    with open(args.outputfile, "w") as f:
        headers = list(reader[0].keys())
        headers.extend(['Price_ETH', 'Value_ETH'])

        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for row in reader:
            # skip rows that are already done
            t_hash = row['Transaction_Hash']
            if args.dbfile and t_hash in completed_hashes:
                print(f"skipped hash {t_hash}")
                continue
            else:
                print(f'processing hash {t_hash}')

            epoch = int(row['Paid_On'])
            row['Price_ETH'] = c_api.get_price_at_time(epoch)['prices'][0][1]
            row['Value_ETH'] = row['Price_ETH'] * float(row['Amount_ETH'])
            writer.writerow(row)

            if args.dbfile:
                sql_api.insert_hash(t_hash)
    
    if args.dbfile:
        sql_api.close()


if __name__ == '__main__':
    main()
