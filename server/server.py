#!/usr/bin/python3
import zmq
from time import sleep
from google.cloud import pubsub_v1
import json

context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5556")
print("zeroMQ server started")

def createMessage(message):
    decoded_message = message.data.decode("utf-8")
    payload = "null" if decoded_message == "null" else json.loads("{" + decoded_message + "}")
    return '{} {}'.format(message.attributes['message_type'], json.dumps(
        {'machine_id': message.attributes['machine_id'],
         'machine_type': message.attributes['machine_type'],
         'timestamp': message.attributes['timestamp'],
         'rfid': message.attributes['rfid'],
         'payload': payload}))

def listen(project, subscription_name):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription_name)

    def callback(message):
        try:
            publisher.send_string(createMessage(message))
            message.ack()
        except json.decoder.JSONDecodeError as e:
            pass

    subscriber.subscribe(subscription_path, callback=callback)

    while True:
        sleep(0.05)
listen("test-mg-1006", "machine_message_subscription")

