import pandas as pd
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
        df = df.drop("date", 1)
        df = df.drop("timestamp", 1)
    if add_all:
        df = df.astype('float32')
        ta.add_all_ta_features(df=df, open="open", high='hi', low='lo', close='last', volume='vl', fillna=False)
    return df
