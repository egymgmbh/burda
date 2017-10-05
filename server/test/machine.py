#!/usr/bin/env python
import zmq
import json
import time


def create_producer(host):
    context = zmq.Context()
    producer = context.socket(zmq.PUSH)
    producer.connect(host)
    return producer


def create_message(payload):
    return json.dumps(
        {'machine_id': 4567, 'machine_type': 'M18', 'timestamp': time.time(), 'rfid': '0x1234567', 'payload': payload})


def create_login_payload():
    return json.dumps(
        {'gender': 'Male', 'goal': 'FITNESS', 'height': 182, 'intensity': 'MEDIUM', 'first_name': 'Shawn'})


def create_start_training_payload():
    return json.dumps({'training_method': 'regular', 'training_weight_concentric': 50, 'training_weight_excentric': 70,
                       'number_of_repetitions': 8})


def create_end_training_payload():
    return json.dumps({'moved_weight': 480})


def create_end_strength_measurement_payload():
    return json.dumps({'weight': 275})


def create_training_position_data_payload():
    return json.dumps({'position': 0.75})


def create_training_weight_data_payload():
    return json.dumps({'weight': 65})


def create_training_direction_data_payload():
    return json.dumps({'direction': 'concentric'})


def create_training_repetition_data_payload():
    return json.dumps({'repetition': 3})


def create_empty_payload():
    return json.dumps({})


def create_login_message():
    return 'login {}'.format(create_message(create_login_payload()))


def create_logout_message():
    return 'logout {}'.format(create_empty_payload())


def create_trainer_needed_message():
    return 'trainer_needed {}'.format(create_empty_payload())


def create_start_training_message():
    return 'start_training {}'.format(create_start_training_payload())


def create_end_training_message():
    return 'end_training {}'.format(create_end_training_payload())


def create_start_strength_measurement_message():
    return 'start_strength_measurement {}'.format(create_empty_payload())


def create_end_strength_measurement_message():
    return 'end_strength_measurement {}'.format(create_end_strength_measurement_payload())


def create_training_position_data_message():
    return 'training_position_data {}'.format(create_training_position_data_payload())


def create_training_weight_data_message():
    return 'training_weight_data {}'.format(create_training_weight_data_payload())


def create_training_direction_data_message():
    return 'training_direction_data {}'.format(create_training_direction_data_payload())


def create_training_repetition_data_message():
    return 'training_repetition_data {}'.format(create_training_repetition_data_payload())


def send_fake_machine_training_flow(producer):
    producer.send(create_login_message())
    producer.send(create_start_training_message())

    for _ in range(10):
        producer.send(create_training_position_data_message())
        producer.send(create_training_weight_data_message())
    producer.send(create_training_direction_data_message())
    producer.send(create_training_repetition_data_message())
    producer.send(create_end_training_message())
    producer.send(create_logout_message())


def send_fake_machine_strength_measurment_flow(producer):
    producer.send(create_login_message())
    producer.send(create_start_strength_measurement_message())
    producer.send(create_end_strength_measurement_message())
    producer.send(create_logout_message())


producer = create_producer("tcp://35.187.37.87:5557")
send_fake_machine_training_flow(producer)
send_fake_machine_strength_measurment_flow(producer)
