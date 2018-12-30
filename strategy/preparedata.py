import pandas as pd
from ta import *
import ta


def add_features(df: pd.DataFrame, add_all=False, drop_times=False, sma="20,50,200", ema="20,50"):
    # df = df.drop("vl_incr", 1)

    df['h'] = pd.to_numeric(df['datetime'].str[-9:-7])
    df['min'] = pd.to_numeric(df['datetime'].str[-6:-4])
    df['year'] = pd.to_numeric(df['datetime'].str[0:4])
    for i in str(sma).split(","):
        df['sma_' + str(i)] = df['last'].rolling(int(i)).mean()
    # if ma:
    #     df['sma_20'] = df['last'].rolling(20).mean()
    #     df['sma_50'] = df['last'].rolling(50).mean()
    #     df['sma_200'] = df['last'].rolling(200).mean()

    for i in str(ema).split(","):
        df['ema_' + str(i)] = df['last'].ewm(span=int(i)).mean()

    if drop_times:
        df = df.drop("datetime", 1)
        # df = df.drop("date", 1)
        # df = df.drop("timestamp", 1)
    if add_all:
        df = df.astype('float32')
        ta.add_all_ta_features(df, open="open", high='hi', low='lo', close='last', volume='vl', fillna=False)
    return df


def add_moving_averages(df: pd.DataFrame, drop_times=False, sma="20,50,200", ema="20,50"):
    df['h'] = pd.to_numeric(df['datetime'].str[-9:-7])
    df['min'] = pd.to_numeric(df['datetime'].str[-6:-4])
    df['year'] = pd.to_numeric(df['datetime'].str[0:4])

    for i in str(sma).split(","):
        df['sma_' + str(i)] = df['last'].rolling(int(i)).mean()
        df['sma_20'] = df['last'].rolling(20).mean()
        df['sma_50'] = df['last'].rolling(50).mean()
        df['sma_200'] = df['last'].rolling(200).mean()

    for i in str(ema).split(","):
        df['ema_' + str(i)] = df['last'].ewm(span=int(i)).mean()

    if drop_times:
        df = df.drop("datetime", 1)
    return df


def add_features_category(df: pd.DataFrame, momentum=False, volatility=False, trend=False, drop_times=True):
    df['h'] = pd.to_numeric(df['datetime'].str[-9:-7])
    df['min'] = pd.to_numeric(df['datetime'].str[-6:-4])
    df['year'] = pd.to_numeric(df['datetime'].str[0:4])

    if drop_times:
        df = df.drop("datetime", 1)

    if momentum:
        df = df.astype('float32')
        ta.add_momentum_ta(df, high='hi', low='lo', close='last', volume='vl', fillna=False)
    if trend:
        df = df.astype('float32')
        ta.add_trend_ta(df, high='hi', low='lo', close='last', fillna=False)
    if volatility:
        df = df.astype('float32')
        ta.add_volatility_ta(df, high='hi', low='lo', close='last', fillna=False)
    return df


# from docs https://technical-analysis-library-in-python.readthedocs.io/en/latest/
def add_bollinger_band(df: pd.DataFrame, n=20, ndev=2, drop_times=True):
    df['h'] = pd.to_numeric(df['datetime'].str[-9:-7])
    df['min'] = pd.to_numeric(df['datetime'].str[-6:-4])
    df['year'] = pd.to_numeric(df['datetime'].str[0:4])

    if drop_times:
        df = df.drop("datetime", 1)

    # Add bollinger band high indicator filling Nans values
    df['bb_high'] = bollinger_hband_indicator(df["last"], n=n, ndev=ndev, fillna=True)
    # Add bollinger band low indicator filling Nans values
    df['bb_low'] = bollinger_lband_indicator(df["last"], n=n, ndev=ndev, fillna=True)
    return df
