# Code downloaded from https://bitbucket.org/vladev/sockjsproxy/src/c89176ba5795?at=default

from __future__ import absolute_import

import logging
import time, signal

import zmq
from zmq.eventloop import zmqstream
from zmq.eventloop import ioloop

ioloop.install()

from tornado import web
from sockjs.tornado import SockJSRouter, SockJSConnection

from tornado.httpserver import HTTPServer

log = logging.getLogger("sockjsproxy")

class BackendConnection(object):
    def __init__(self, io_loop, out_socket):
        self.out_socket = out_socket
        self.io_loop = io_loop
        self.io_loop.add_timeout(50, self.recieve)

    def set_frontend_connection(self, frontend):
        self.frontend = frontend

    def recieve(self):
        try:
            data = self.out_socket.recv_string(zmq.NOBLOCK)
            self.on_recv(data)
        except zmq.ZMQError as e:
            # continue
            pass
        self.io_loop.add_timeout(50, self.recieve)

    def on_recv(self, data):
        log.debug('Got %s :: %s', data)
        self.frontend.send(data)

class FrontendTransport(SockJSConnection):
    """
    The actual sock.js connection. Since the library creates one instance
    of this class for every connection we use the python id() of the instance
    as session_id, and all session_ids should be unicode so we can find
    them easily in dicts.
    """
    frontend = None

    @classmethod
    def initialize(cls, frontend):
        cls.frontend = frontend

    def on_open(self, request):
        self.frontend.add_session(str(id(self)), self)

    def on_message(self, msg):
        self.frontend.message_from_client(str(id(self)), msg)

    def on_close(self):
        self.frontend.remove_session(str(id(self)))


class FrontendConnection(object):
    """
    Connection, responsible for handling messages from SockJS.
    """

    def __init__(self):
        self.sessions = {}


    def add_session(self, session_id, connection):
        self.sessions[session_id] = connection
        log.debug('Session %s established', session_id)

    def remove_session(self, session_id):
        if session_id not in self.sessions:
            log.warn('Session %s missing when removing', session_id)
            return

        del self.sessions[session_id]
        log.debug('Session %s removed', session_id)

    def send(self, message):
        for key in self.sessions:
            self.sessions.get(key).send(message)

    def close(self, session_id):
        connection = self.sessions.get(session_id)
        if not connection:
            log.warn('Could not close session %s: '
                     'Connection not found.', session_id)
            return

        connection.close()

    def close_all(self):
        for c in self.sessions.values():
            c.close()


class SockJSProxy(object):
    def init_logging(self, verbose):
        log.setLevel(logging.DEBUG if verbose else logging.INFO)

    def main(self):
        self.init_logging(True)

        out_address = "tcp://127.0.0.1:5556"

        log.info("Pulling outgoing messages from: %s", out_address)

        ctx = zmq.Context()
        out_socket = ctx.socket(zmq.SUB)
        out_socket.setsockopt_string(zmq.SUBSCRIBE, '')
        out_socket.connect(out_address)

        io_loop = ioloop.IOLoop.instance() # ZMQ loop

        frontend = FrontendConnection()
        backend = BackendConnection(io_loop, out_socket)

        FrontendTransport.initialize(frontend)
        backend.set_frontend_connection(frontend)

        sockjs_router = SockJSRouter(FrontendTransport, io_loop=io_loop)

        routes = sockjs_router.urls

        web_app = web.Application(routes, debug=False)

        web_server = HTTPServer(web_app)
        web_server.listen(5558)

        def term(*_ignore):
            log.info("SockjsProxy shutting down...")
            web_server.stop()
            io_loop.add_timeout(time.time() + 0.3, io_loop.stop)
            io_loop.start() # Let the IO loop finish its work

        signal.signal(signal.SIGTERM, term)

        try:
            log.info('SockjsProxy serving on %s', 5558)
            io_loop.start()
        except KeyboardInterrupt:
            term()

if __name__ == "__main__":
    SockJSProxy().main()