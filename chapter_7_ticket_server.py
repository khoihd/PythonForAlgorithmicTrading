import zmq
import math
import time
import random
from InstrumentPrice import InstrumentPrice


if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind('tcp://0.0.0.0:5555')

    ip = InstrumentPrice()
    while True:
        msg = '{} {:.2f}'.format(ip.symbol, ip.simulate_value())
        print(msg)
        socket.send_string(msg)
        time.sleep(random.random() * 2)
