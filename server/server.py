#!/usr/bin/python3
import zmq

context = zmq.Context()
consumer = context.socket(zmq.PULL)
consumer.bind('tcp://*:5557')

publisher = context.socket(zmq.PUSH)
publisher.bind("tcp://*:5556")
print("zeroMQ server started")

while True:
    try:
        data = consumer.recv_multipart()
        print(data)
        publisher.send_multipart(data)
    except Exception as e:
        print("Exception caught {}".format(e))

