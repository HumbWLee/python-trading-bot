import argparse
import datetime
import logging
import sys
import time

from cryptoapi.bithumbApi import BithumbApi

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s][%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        stream=sys.stdout)

    parser = argparse.ArgumentParser(description='Trading Bot at Bithumb')
    parser.add_argument('--bithumbId'     , default='hhpp1231',
                        help='Must config file name is <config_bithumbId.json>')
    parser.add_argument('--statisticsDays', default=5,
                        help='This value is the statistical period for judging the bull market')
    args = parser.parse_args()

    bithumb = BithumbApi(bithumb_id=args.bithumbId)
    ticker_k_s = bithumb.get_ticker_k()

    now = datetime.datetime.now()
    tomorrow = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1)

    # reset
    moving_average = {}
    target_price = {}
    buy_price = {}
    is_buy = {}
    for ticker in ticker_k_s.keys():
        moving_average[ticker] = bithumb.get_moving_average(ticker, args.statisticsDays)
        target_price[ticker] = bithumb.get_target_price(ticker, ticker_k_s[ticker])
        buy_price[ticker] = 0
        is_buy[ticker] = False

        sell_result = bithumb.sell_crypto_currency(ticker)
        if type(sell_result) != dict:
            current_price = bithumb.get_current_price(ticker)
            logging.info("[Reset Sell] {0} / Sell : {2}"
                         .format(ticker, buy_price[ticker], current_price))

    logging.info("[Trading Start] KRW : {0}".format(bithumb.get_balance_krw()))

    while True:
        try:
            now = datetime.datetime.now()

            # reset at 00:00 AM
            if tomorrow < now:
                time.sleep(120)
                tomorrow = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1)

                for ticker in ticker_k_s.keys():
                    if is_buy[ticker]:
                        sell_result = bithumb.sell_crypto_currency(ticker)

                        if type(sell_result) == dict:
                            logging.error("[Sell] {0} / {1} / {2}"
                                          .format(ticker, bithumb.get_current_price(ticker), sell_result))
                        else:
                            current_price = bithumb.get_current_price(ticker)
                            rate_of_return = (current_price - buy_price[ticker]) / buy_price[ticker] * 100
                            logging.info("[Sell] {0} / Buy : {1} / Sell : {2} / ROR : {3}%"
                                         .format(ticker, buy_price[ticker], current_price, rate_of_return))

                    moving_average[ticker] = bithumb.get_moving_average(ticker, args.statisticsDays)
                    target_price[ticker] = bithumb.get_target_price(ticker, ticker_k_s[ticker])
                    buy_price[ticker] = 0
                    is_buy[ticker] = False

                time.sleep(120)
                logging.info("[Balance] KRW : {0}".format(bithumb.get_balance_krw()))

            # trading
            for ticker in ticker_k_s.keys():
                if is_buy[ticker]:
                    continue

                current_price = bithumb.get_current_price(ticker)

                if (current_price > target_price[ticker]) and (current_price > moving_average[ticker]):
                    buy_result = bithumb.buy_crypto_currency(ticker, 0.5)

                    if type(buy_result) == dict:
                        logging.error("[Buy Fail] {0} / current : {1}, target : {2}, ma : {3} / {4}".format(
                            ticker, current_price, target_price[ticker], moving_average[ticker], buy_result))
                    else:
                        logging.info("[Buy] {0} / current : {1}, target : {2}, ma : {3}".format(
                            ticker, current_price, target_price[ticker], moving_average[ticker]))
                    buy_price[ticker] = current_price
                    is_buy[ticker] = True

        except Exception as e:
            logging.error("[Main] Error in trading / %s" % str(e))
