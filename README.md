# ethermine-ethereum-mining-tax-calculator
A tool to help you calculate (for US tax purposes) your Ethereum (ETH) received and the price at the given time.

For example, your payouts csv might look like:
```commandline
"Paid_On","From_Block","To_Block","Amount_ETH","Transaction_Hash","Network"
"164452541","14172","141804","0.005017910201146812","0xa25ec3214749a2985e22f85ace1017751", "Polygon"
"164442015","14164","14172","0.005000136875480635","0x192c0e1e11b38d10f2e708aa5d21d4b7b4f", "Polygon"
"164430593","14155","14164","0.005019688846002083","0x10ca3ef21d60dbeaf2b0e7c2d1d066d4eae", "Polygon"
```

This app will append two columns: `Price_ETH` and `Value_ETH` which will pull from Coin Gecko API and get you the value of the tokens at that time for tax income purposes.

# Arguments
Input - The file you get from Ethermine (typically named `payouts.csv`)
- `--input <filepath>`
- Optional
- Defaults to `payouts.csv`
- Specify your input filepath here
- See below for help on getting the file

Output - The output file with the updated columns (as described above)
- `--output <filepath>`
- Optional
- Defaults to `payout_updated.csv`
- This is where your transactions with the updated prices will be

Database (SQLite3 DB to hold previously run transactions)
- `--db <path to db file already existing or to be created>`
- Optional
- If specified, this will store your transaction hashes so the next time you run this app, the output CSV will not contain the same hashes
- This will automatically create the tables if you specify this arg. Otherwise the entire CSV from the input will be run

# How to Run
Setup your venv:
- `pip3 install -U pip`
- `pip3 install -r requirements.txt`
- `python3 -m app`

# How to get you Ethermine payout CSV (input)
- Go to your miners dashboard on ethermine.org (where you see workers, hashrate, etc)
- Click on payouts
- Scroll down until you see the list of payouts
- You should see a download icon that lets you download the last 100 transactions