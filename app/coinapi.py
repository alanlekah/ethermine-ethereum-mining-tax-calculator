import time
import requests
from pycoingecko import CoinGeckoAPI


class CoinAPI:

    def __init__(self):
        self.cg = CoinGeckoAPI()
        self.cg.ping()

    def get_price_at_time(self, epoch: int):
        while True:
            try:
                ret = self.cg.get_coin_market_chart_range_by_id(id='ethereum',
                                                                vs_currency='usd',
                                                                from_timestamp=epoch,
                                                                to_timestamp=(epoch+5600))
                return ret
            except requests.exceptions.HTTPError:
                print("Sleeping..")
                time.sleep(3)
