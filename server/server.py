#!/usr/bin/env python
import zmq

context = zmq.Context()
consumer = context.socket(zmq.PULL)
consumer.bind('tcp://*:5557')

publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5556")

print("zeromq server started")

while True:
    data = consumer.recv()
    print("Publishing message {}".format(data))
    publisher.send(data)
