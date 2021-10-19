import logging
import os
import pathlib
import sys
import time

import pybithumb
from config.configuration import Configuration


class BithumbApi:
    def __init__(self, bithumb_id):
        logging.basicConfig(level=logging.INFO,
                            format='[%(asctime)s][%(levelname)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            stream=sys.stdout)
        bithumb_config = Configuration("config_%s.json" % bithumb_id)

        try:
            self.__api = pybithumb.Bithumb(bithumb_config.get_connect_key(), bithumb_config.get_secret_key())
        except Exception as e:
            logging.error("[Bithumb] Error in Bithumb connect / %s" % str(e))

    def get_api(self):
        return self.__api

    def get_balance(self, ticker):
        balance = self.__api.get_balance(ticker)
        return format(balance[0], 'f')

    def get_is_bull_market(self, ticker, statistics_days):
        df = pybithumb.get_ohlcv(ticker)
        madays = df['close'].rolling(window=statistics_days).mean()
        last_madays = madays[-2]

        price = pybithumb.get_current_price(ticker)

        if price > last_madays:
            return True
        else:
            return False

    def get_target_price(self, ticker):
        df = pybithumb.get_ohlcv(ticker)
        yesterday = df.iloc[-2]

        today_open = yesterday['close']
        yesterday_high = yesterday['high']
        yesterday_low = yesterday['low']
        target = today_open + (yesterday_high - yesterday_low) * 0.5
        return target

    def buy_crypto_currency(self, ticker):
        krw = self.__api.get_balance(ticker)[2]
        orderbook = pybithumb.get_orderbook(ticker)
        sell_price = orderbook['asks'][0]['price']
        unit = krw / float(sell_price)
        self.__api.buy_market_order(ticker, unit)

    def sell_crypto_currency(self, ticker):
        unit = self.__api.get_balance(ticker)[0]
        self.__api.sell_market_order(ticker, unit)


if __name__ == '__main__':
    os.chdir(str(pathlib.Path(__file__).parent.parent.absolute()))
    print(os.getcwd())
    bithumb = BithumbApi(bithumb_id="hhpp1231")

    print(bithumb.get_target_price("BTC"))

