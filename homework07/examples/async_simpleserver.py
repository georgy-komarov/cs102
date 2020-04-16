import asyncore
import asynchat
import logging


class AsyncHTTPRequestHandler(asynchat.async_chat):
    """ Обработчик клиентских запросов """

    def __init__(self, sock):
        super().__init__(sock)
        self.set_terminator(b"\r\n\r\n")

    def collect_incoming_data(self, data):
        log.debug(f"Incoming data: {data}")
        self._collect_incoming_data(data)

    def found_terminator(self):
        self.parse_request()

    def parse_request(self):
        pass

    def parse_headers(self):
        pass


class AsyncHTTPServer(asyncore.dispatcher):

    def __init__(self, host="127.0.0.1", port=9000):
        super().__init__()
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        log.debug(f"Incoming connection from {addr}")
        AsyncHTTPRequestHandler(sock)


logging.basicConfig(
    level=getattr(logging, 'DEBUG'),
    format="%(message)s")
log = logging.getLogger(__name__)

server = AsyncHTTPServer()
asyncore.loop()
