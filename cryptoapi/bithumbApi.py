import logging
import os
import pathlib
import sys
import time
from pprint import pprint

import pybithumb
from config.configuration import Configuration


class BithumbApi:
    def __init__(self, bithumb_id):
        logging.basicConfig(level=logging.INFO,
                            format='[%(asctime)s][%(levelname)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            stream=sys.stdout)
        self.bithumb_config = Configuration("config_%s.json" % bithumb_id)

        try:
            self.__api = pybithumb.Bithumb(self.bithumb_config.get_connect_key(), self.bithumb_config.get_secret_key())
        except Exception as e:
            logging.error("[Bithumb] Error in Bithumb connect / %s" % str(e))

    def get_api(self):
        return self.__api

    def get_ticker_k(self):
        return self.bithumb_config.get_ticker_k()

    def get_current_price(self, ticker):
        return pybithumb.get_current_price(ticker)

    def get_balance(self, ticker):
        balance = self.__api.get_balance(ticker)
        return format(balance[0], 'f')

    def get_balance_krw(self):
        balance = self.__api.get_balance('BTC')
        return int(balance[2])

    def get_moving_average(self, ticker, statistics_days):
        df = pybithumb.get_ohlcv(ticker)
        madays = df['close'].rolling(window=statistics_days).mean()
        last_madays = madays[-2]

        return last_madays

    def get_is_bull_market(self, ticker, moving_average):
        price = pybithumb.get_current_price(ticker)

        if price > moving_average:
            return True
        else:
            return False

    def get_target_price(self, ticker, k):
        df = pybithumb.get_ohlcv(ticker)
        yesterday = df.iloc[-2]

        today_open = yesterday['close']
        yesterday_high = yesterday['high']
        yesterday_low = yesterday['low']
        target = today_open + (yesterday_high - yesterday_low) * k

        return target

    def buy_crypto_currency(self, ticker, ratio):
        krw = int(self.__api.get_balance(ticker)[2] * ratio)
        orderbook = pybithumb.get_orderbook(ticker)
        sell_price = orderbook['asks'][0]['price']
        unit = krw / float(sell_price)
        return self.__api.buy_market_order(ticker, unit)

    def sell_crypto_currency(self, ticker):
        unit = self.__api.get_balance(ticker)[0]
        return self.__api.sell_market_order(ticker, unit)




if __name__ == '__main__':
    os.chdir(str(pathlib.Path(__file__).parent.parent.absolute()))
    print(os.getcwd())
    bithumb = BithumbApi(bithumb_id="bithumb_id")
    print(bithumb.get_target_price('LUNA', 0.03))


