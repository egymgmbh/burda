/**
 * This file is part of the source code and related artifacts for eGym Application.
 *
 * Copyright © 2017 eGym GmbH
 */
package de.egym;

import org.zeromq.ZContext;
import org.zeromq.ZMQ;

public final class Application {

	private static final String HOST = "tcp://35.189.246.57:5556";

	private Application() {

	}

	private void subscribeAndAwait() {
		try (final ZContext context = new ZContext()) {
			final ZMQ.Socket socket = context.createSocket(ZMQ.SUB);

			if (socket.connect(HOST) && socket.subscribe("")) {
				processEvents(socket);
			}
		}
	}

	private void processEvents(final ZMQ.Socket socket) {
		while (true) {
			final String data = socket.recvStr();

                        // TODO: Use a JSON parser to get the message_type and the body.

			System.out.println(data);
		}
	}

	public static void main(String[] args) {
		final Application application = new Application();
		application.subscribeAndAwait();
	}
}
