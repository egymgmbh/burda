#!/usr/bin/env python

import zmq
import json
import sys

if sys.version_info < (3, 0):
    print("This script requires Python 3.")
    sys.exit(1)

def subscribe(host):
    return subscribe_with_filter(host, "")


def subscribe_with_filter(host, topic_filter):
    subscriber = zmq.Context().socket(zmq.SUB)
    subscriber.setsockopt_string(zmq.SUBSCRIBE, topic_filter)
    subscriber.connect(host)
    return subscriber

def await_and_consume(subscriber, handlers):
    while True:
        msg = subscriber.recv_string()
        try:
            obj = json.loads(msg)
            # print(obj)

            message_type = obj['message_type']
            handler = handlers.get(message_type, None)
            if handler:
                handler(obj['body'])
            else:
                print('No handler for message type: ' + message_type)

        except ValueError:
            print('Failed to parse JSON: ' + msg)

def login_topic_handler(data):
        print("Login with data: {}".format(data))


await_and_consume(subscribe("tcp://35.189.246.57:5556"), {'login': login_topic_handler})
