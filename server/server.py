#!/usr/bin/python3
import zmq
from time import sleep
from google.cloud import pubsub_v1

context = zmq.Context()
consumer = context.socket(zmq.PULL)
consumer.bind('tcp://*:5557')

publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5556")
print("zeroMQ server started")


def listen(project, subscription_name):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription_name)

    def callback(message):
        publisher.send_string('{} {}'.format(message.attributes['message_type'], message.data))
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)

    while True:
        sleep(0.05)
listen("test-mg-1006", "machine_message_subscription")

