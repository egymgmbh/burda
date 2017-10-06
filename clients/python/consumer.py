import zmq


def subscribe(host):
    return subscribe_with_filter(host, "")


def subscribe_with_filter(host, topic_filter):
    subscriber = zmq.Context().socket(zmq.SUB)
    subscriber.setsockopt(zmq.SUBSCRIBE, topic_filter)
    subscriber.connect(host)
    return subscriber


def await_and_consume(subscriber, handlers):
    while True:
        (type, data) = subscriber.recv_string().split(' ', 1)
        handler = handlers.get(type, None)
        if handler:
            handler(data)


def login_topic_handler(data):
    print("Login with data: {}".format(data))


await_and_consume(subscribe("tcp://35.195.199.160:5556"), {'login': login_topic_handler})
