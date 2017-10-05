# Burda Hackaday
Selected machines to the event will run a special software build that 
will publish certain events during a user workout, making it possible to 
develop applications that will collect such data.

In order to consume such messages, each application will need to 
subscribe to zeroMQ server. 

## Message format

All the published messages always have 5 attributes:
* **machine_id**
the ID of the machine sending the event (e.g. “3756”)
* **machine_type**
the machine type of the machine sending the event (“M1”, “M2”, …, “M18”)
* **timestamp**
Time at which the event was emitted by the machine in milliseconds since 1/1/1970 0:00 UTC 
* **rfid**
rfid of the user logged in at the time of the event (e.g. 000003ed). 
Can be used to match events to users.
* **payload**
The payload of the message. These values vary per message type.

An example message might look like this:
```JSON
“login {
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
}”
```
All messages are of the form *“<message_type> <message_body>”*.

### Payload Definition

#### login
Emitted when an already registered user logs in.

**Payload:** JSON object with the following attributes:
* **gender**
JSON `null` if the user hasn’t selected the gender yet, or one of the JSON strings “male” or “female”
* **goal**
One of the JSON strings “muscle_building”, “weight_loss”, “athletic”, “body_toning”, “general_fitness”, “reha_fit”, “classic”
* **height**
JSON `null` if the user hasn’t set the height yet, or a JSON number describing the height of the user in centimeters.
* **intensity**
One of the JSON strings “low”, “medium” or “high”
* **first_name**
First name of the user.

#### logout
Emitted when a user logs out.

**Payload:** JSON `null`

#### trainer_needed
Emitted when a user has logged in, but doesn’t have settings for that particular machine yet.

**Payload:** JSON `null`

#### start_training
Emitted when a user starts a training.

**Payload:** JSON object with keys
* **training_method**
JSON string, one of “regular”, “negative”, “adaptive”, “isokinetic” and “explonic”
* **training_weight_concentric**
JSON number, training weight in the concentric direction in kilograms
* **training_weight_excentric**
JSON number, training weight in the excentric direction in kilograms
* **number_of_repetitions**
JSON number, recommended number of repetitions for the training

#### end_training
Emitted when a user ends the training.

**Payload:** JSON object with keys
* **moved_weight**
JSON number, the weight moved during the training in kilograms

####start_strength_measurement
Emitted when a user starts a strength measurement.

**Payload:** JSON `null`

#### end_strength_measurement
Emitted when a user accepts a strength measurement.

**Payload:**  JSON object with keys
* **weight**
JSON number, the result of the strength measurement in kilograms

#### training_position_data
Emitted every 100ms during a training session.

**Payload:** JSON object with keys
* **position**
JSON number between 0.0 and 1.0. Describes the position of the training lever 
in percent of the range of motion.

#### training_weight_data
Emitted every 100ms during a training session. Most interesting for isokinetic training where the machine adjusts 
the weight during repetitions, but can also be used to detect changes in weight due to a user clicking on the 
respective button.

**Payload:** JSON object with keys
* **weight** JSON number. The current training weight in kg. 

#### training_direction_data
Emitted every time the training direction changes during training

**Payload:** JSON object with keys
* **direction** JSON string. Either “concentric” or “excentric”. 

#### training_repetition_data
Emitted every time the user completes a repetition during training.

**Payload:** JSON object with keys
* **repetition** JSON number. The number of repetitions completed so far.

