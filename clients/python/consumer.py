import zmq
import json


def subscribe(host):
    return subscribe_with_filter(host, "")


def subscribe_with_filter(host, topic_filter):
    subscriber = zmq.Context().socket(zmq.SUB)
    subscriber.setsockopt(zmq.SUBSCRIBE, topic_filter)
    subscriber.connect(host)
    return subscriber

def await_and_consume(subscriber):
    while True:
        msg = subscriber.recv()
        obj = json.loads(msg)
        print(obj)

await_and_consume(subscribe("tcp://35.189.246.57:5556"))
