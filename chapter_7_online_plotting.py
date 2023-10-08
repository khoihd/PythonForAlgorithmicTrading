import zmq
from datetime import datetime
import plotly.graph_objects as go


if __name__ == "__main__":
    symbol = 'SYMBOL'
    fig = go.FigureWidget()
    fig.add_scatter()

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect('tcp://0.0.0.0:5555')
    socket.setsockopt_string(zmq.SUBSCRIBE, 'SYMBOL')

    times, prices = [], []
    for _ in range(50):
        msg = socket.recv_string()
        t = datetime.now()
        times.append(t)
        _, price = msg.split()
        prices.append(float(price))
        fig.data[0].x = times
        fig.data[0].y = prices
