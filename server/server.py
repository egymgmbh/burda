#!/usr/bin/env python

import zmq

import sys

if sys.version_info < (3, 0):
    print("This script requires Python 3.")
    sys.exit(1)

context = zmq.Context()
consumer = context.socket(zmq.PULL)
consumer.bind('tcp://*:5557')

publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5556")
print("zeroMQ server started")

while True:
    try:
        data = consumer.recv_string()
        print(data)
        publisher.send_string(data)
    except Exception as e:
        print("Exception caught {}".format(e))

