import zmq

if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect('tcp://0.0.0.0:5555')
    socket.setsockopt_string(zmq.SUBSCRIBE, 'SYMBOL')

    while True:
        data = socket.recv_string()
        print(data)