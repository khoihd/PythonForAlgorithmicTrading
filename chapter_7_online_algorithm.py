import datetime
import pandas as pd
import zmq
import numpy as np


if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect('tcp://0.0.0.0:5555')
    socket.setsockopt_string(zmq.SUBSCRIBE, 'SYMBOL')

    mom = 3
    min_len = mom + 1
    time_sym_price = []

    while True:
        data = socket.recv_string()
        t = datetime.datetime.now()
        time_sym_price.append([t] + data.split())
        df = pd.DataFrame(time_sym_price, columns=["time", "symbol", "price"])
        df['price'] = df['price'].astype(float)
        df = df.set_index('time')

        if df.shape[0] <= min_len:
            continue

        dr = df.resample('5s', label='right').last()
        dr['returns'] = np.log(dr['price'] / dr['price'].shift(1))
        if len(dr) > min_len:
            min_len += 1
            dr['momentum'] = np.sign(dr['returns'].rolling(mom).mean())
            print('\n' + '=' * 51)
            print('NEW SIGNAL | {}'.format(datetime.datetime.now()))
            print('=' * 51)
            print(dr.iloc[:-1].tail())
            if dr['momentum'].iloc[-2] == 1.0:
                print('\nLong market position.')
            # take some action (e.g., place buy order)
            elif dr['momentum'].iloc[-2] == -1.0:
                print('\nShort market position.')
        # # take some action (e.g., place sell order)

