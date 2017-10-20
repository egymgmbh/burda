# Burda Hackaday

Presentation slides of the eGym challenge: https://docs.google.com/presentation/d/1iMP5wNzl2cyZ4g1deecPTVYjzG9N7sY15OGWY0jCfo0/edit?usp=sharing

Selected machines at the event will run a special software build that
will publish certain events during a user workout or strength measurement, making it possible to
develop interesting applications.

In order to consume such messages, each application will need to
subscribe to a ZeroMQ server. Developers using the provided API are able to
subscribe to a variety of different message topics which are described below.

## Message format

All the published messages always have 5 attributes:
* **machine_id**
the ID of the machine sending the event (e.g. “3756”)
* **machine_type**
the machine type of the machine sending the event (“M1”, “M2”, …, “M18”). Look up which machine is which here: https://www.egym.de/business/fitness-power
* **timestamp**
Time at which the event was emitted by the machine in milliseconds since 1/1/1970 0:00 UTC
* **rfid**
rfid of the user logged in at the time of the event (e.g. 000003ed).
Can be used to match events to users.
* **payload**
The payload of the message. These values vary per message type.

An example message might look like this:
```JSON
“login": {
   "timestamp":1507214081.483756,
   "rfid":"0x1234567",
   "machine_id":4567,
   "payload":{
      "gender":"Male",
      "intensity":"MEDIUM",
      "first_name":"Shawn",
      "goal":"FITNESS",
      "height":182
   },
   "machine_type":"M18"
}
```
All messages are of the form *“<message_type> <message_body>”*.

### Payload Definition

#### login
Emitted when an already registered user logs in.

**Payload:** JSON object with the following attributes:
* **gender**
`null` if the user hasn’t selected the gender yet, or one of the strings “male” or “female”
* **goal**
One of the strings “muscle_building”, “weight_loss”, “athletic”, “body_toning”, “general_fitness”, “reha_fit”, “classic”
* **height**
`null` if the user hasn’t set the height yet, or a number describing the height of the user in centimeters.
* **intensity**
One of the strings “low”, “medium” or “high”
* **first_name**
First name of the user.

#### logout
Emitted when a user logs out.

**Payload:** `null`

    "logout": {
       "timestamp":1507282654.697113,
       "rfid":"0x1234567",
       "machine_id":4567,
       "payload":null,
       "machine_type":"M18"
    }

#### trainer_needed
Emitted when a user has logged in, but doesn’t have settings for that particular machine yet.

**Payload:** `null`

#### start_training
Emitted when a user starts a training.

    "start_training": {
       "timestamp":1507278857.209818,
       "rfid":"0x1234567",
       "machine_id":4567,
       "payload":{
          "training_weight_excentric":70,
          "training_method":"regular",
          "training_weight_concentric":50,
          "number_of_repetitions":8
       },
       "machine_type":"M18"
    }

**Payload:** JSON object with keys
* **training_method**
string, one of “regular”, “negative”, “adaptive”, “isokinetic” and “explonic”
* **training_weight_concentric**
number, training weight in the concentric direction in kilograms
* **training_weight_excentric**
number, training weight in the excentric direction in kilograms
* **number_of_repetitions**
number, recommended number of repetitions for the training

#### end_training
Emitted when a user ends the training.

    "end_training": {
       "timestamp":1507283268.229535,
       "rfid":"0x1234567",
       "machine_id":4567,
       "payload":{
          "moved_weight":480
       },
       "machine_type":"M18"
    }

**Payload:** JSON object with keys
* **moved_weight**
number, the weight moved during the training in kilograms

#### start_strength_measurement
Emitted when a user starts a strength measurement.

    "start_strength_measurement": {
       "timestamp":1507283268.229615,
       "rfid":"0x1234567",
       "machine_id":4567,
       "payload":"null,
       "machine_type":"M18"
    }

**Payload:** `null`

#### end_strength_measurement
Emitted when a user accepts a strength measurement.

    "end_strength_measurement": {
       "timestamp":1507283268.229639,
       "rfid":"0x1234567",
       "machine_id":4567,
       "payload":{
          "weight":275
       },
       "machine_type":"M18"
    }

**Payload:**  JSON object with keys
* **weight**
number, the result of the strength measurement in kilograms

#### training_position_data
Emitted every 100ms during a training session.

    "training_position_data": {
       "timestamp":1507283268.229425,
       "rfid":"0x1234567",
       "machine_id":4567,
       "payload":{
          "position":0.75
       },
       "machine_type":"M18"
    }

**Payload:** JSON object with keys
* **position**
number between 0.0 and 1.0. Describes the position of the training lever
in percent of the range of motion.

#### training_weight_data
Emitted every 100ms during a training session. Most interesting for isokinetic training where the machine adjusts
the weight during repetitions, but can also be used to detect changes in weight due to a user clicking on the
respective button.

    "training_weight_data": {
       "timestamp":1507283268.229454,
       "rfid":"0x1234567",
       "machine_id":4567,
       "payload":{
          "weight":65
       },
       "machine_type":"M18"
    }

**Payload:** JSON object with keys
* **weight** number. The current training weight in kg.

#### training_direction_data
Emitted every time the training direction changes during training

    "training_direction_data": {
       "timestamp":1507283268.22948,
       "rfid":"0x1234567",
       "machine_id":4567,
       "payload":{
          "direction":"concentric"
       },
       "machine_type":"M18"
    }

**Payload:** JSON object with keys
* **direction** string. Either “concentric” or “excentric”.

#### training_repetition_data
Emitted every time the user completes a repetition during training.

    "training_repetition_data": {
       "timestamp":1507283268.229506,
       "rfid":"0x1234567",
       "machine_id":4567,
       "payload":{
          "repetition":3
       },
       "machine_type":"M18"
    }


**Payload:** JSON object with keys
* **repetition** number. The number of repetitions completed so far.

