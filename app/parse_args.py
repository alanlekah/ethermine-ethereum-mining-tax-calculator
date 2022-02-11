import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="A program to give you ETH prices "
                                                 "at a given time when exporting a CSV "
                                                 "from Ethermine (for tax purposes).")

    parser.add_argument('--input', dest='inputfile', default='payout.csv', type=str,
                        help="The Ethermine CSV export (that you get from the site)")

    parser.add_argument('--output', dest='outputfile', type=str, default='payout_updated.csv',
                        help='When specified, this will output a csv of '
                             'updated rows with their given ETH prices.'
                             'If the dbfile is specified as well, '
                             'this will only give you transactions not previously'
                             'inserted in the table')

    parser.add_argument('--db', dest='dbfile', type=str,
                        help="When specified, this will create/update "
                             "the database specified with the filename")

    args = parser.parse_args()
    return args
