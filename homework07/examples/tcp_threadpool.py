import socket
import threading
import time
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s'
)


def worker_thread(serversocket: socket.socket, shutdown_event: threading.Event) -> None:
    while not shutdown_event.isSet():
        try:
            clientsock, (client_address, client_port) = serversocket.accept()
            logging.debug(f"New client: {client_address}:{client_port}")
        except (OSError, ConnectionAbortedError):
            continue

        while True:
            try:
                message = clientsock.recv(1024)
                logging.debug(f"Recv: {message} from {client_address}:{client_port}")
            except OSError:
                break

            if len(message) == 0:
                break

            sent_message = message
            while True:
                sent_len = clientsock.send(sent_message)
                if sent_len == len(sent_message):
                    break
                sent_message = sent_message[sent_len:]
            logging.debug(f"Send: {message} to {client_address}:{client_port}")

        clientsock.close()
        logging.debug(f"Bye-bye: {client_address}:{client_port}")
    logging.debug("Shutting down thread")


def main(host: str = 'localhost', port: int = 9090) -> None:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    serversocket.bind((host, port))
    serversocket.listen(128)

    print(f"Starting TCP Echo Server at {host}:{port}")

    NUMBER_OF_THREADS = 10
    threads = []
    shutdown_event = threading.Event()
    for _ in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=worker_thread,
                                  args=(serversocket, shutdown_event))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        serversocket.close()
        shutdown_event.set()
        time.sleep(1)


if __name__ == "__main__":
    main()
