/**
 * This file is part of the source code and related artifacts for eGym Application.
 *
 * Copyright © 2017 eGym GmbH
 */
package de.egym;

import org.zeromq.ZContext;
import org.zeromq.ZMQ;

public final class Application {

	private static final String HOST = "tcp://35.195.199.160:5556";

	private Application() {

	}

	private void subscribeAndAwait() {
		try (final ZContext context = new ZContext()) {
			final ZMQ.Socket socket = context.createSocket(ZMQ.PULL);

			if (socket.connect(HOST) && socket.subscribe("")) {
				processEvents(socket);
			}
		}
	}

	private void processEvents(final ZMQ.Socket socket) {
		while (true) {
			final String[] data = socket.recvStr().split(" ", 2);
			final String topic = data[0];
			final String payload = data[1];
			System.out.println(topic + ", " + payload);
		}
	}

	public static void main(String[] args) {
		final Application application = new Application();
		application.subscribeAndAwait();
	}
}
