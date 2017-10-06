# Project: zeromq-server
from python

COPY server.py server.py

RUN pip install pyzmq
RUN pip install google-cloud-pubsub
ENV GOOGLE_APPLICATION_CREDENTIALS /credentials/subscriber_credentials.json

ENTRYPOINT python server.py