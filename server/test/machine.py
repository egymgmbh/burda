#!/usr/bin/env python
import zmq

context = zmq.Context()
producer = context.socket(zmq.PUSH)
producer.connect("tcp://35.187.37.87:5557")
print("after connect")
[producer.send("hello {}".format(x)) for x in range(1, 100)]