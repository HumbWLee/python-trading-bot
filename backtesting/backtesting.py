from pprint import pprint

import pybithumb
import numpy as np

def get_returns(fee=0.0032, k=0.7, seed=100000):
    df_ohlcv = pybithumb.get_ohlcv("BTC")
    df_ohlcv['range'] = (df_ohlcv['high'] - df_ohlcv['low']) * k
    df_ohlcv['target'] = df_ohlcv['open'] + df_ohlcv['range'].shift(1)

    df_ohlcv['ror'] = np.where(df_ohlcv['high'] > df_ohlcv['target'],
                               df_ohlcv['close'] / df_ohlcv['target'] - fee, 1)
    df_ohlcv['seed'] = df_ohlcv['ror'].cumprod() * seed
    df_ohlcv = df_ohlcv.drop(['open', 'high', 'low', 'close', 'volume', 'range', 'target'], axis=1)

    print(df_ohlcv)

def get_rate_of_returns(fee=0.0032, k=0.5):
    df_ohlcv = pybithumb.get_ohlcv("BTC")
    df_ohlcv['range'] = (df_ohlcv['high'] - df_ohlcv['low']) * k
    df_ohlcv['target'] = df_ohlcv['open'] + df_ohlcv['range'].shift(1)

    df_ohlcv['ror'] = np.where(df_ohlcv['high'] > df_ohlcv['target'],
                               df_ohlcv['close'] / df_ohlcv['target'] - fee, 1)

    rate_of_returns = df_ohlcv['ror'].cumprod()[-2]

    return rate_of_returns

if __name__ == '__main__':
    # for k in np.arange(0.1, 1.0, 0.01):
    #     ror = get_rate_of_returns(k=k)
    #     print("k= {0} / ror= {1}".format(k, ror))

    get_returns(k=0.75)