The server can be deployed to a kubernetes project.

For instance, to use our test kubernetes project:
```
$ gcloud config set project test-mg-1006
```

You can then deploy, or re-deploy the server like so:

```
$ cd server
$ kubectl create namespace burda-hackday
$ export PROJECT_ID="$(gcloud config get-value project -q)"
$ docker build -t gcr.io/${PROJECT_ID}/burda:murrayc-zeromq .
$ gcloud docker -- push gcr.io/${PROJECT_ID}/burda:murrayc-zeromq
$ kubectl apply -f deploy/burda.yaml
```

You can then discover the server's IP address like so:
```
$ kubectl get services --namespace=burda-hackday
```

You can test the server by running the test machine.py and consumer.py scripts in separate terminals.
The machine.py script will send messages to the server, which the consumer.py script should receive:
```
$ python test/consumer.py
...
$ python test/machine.py
```

