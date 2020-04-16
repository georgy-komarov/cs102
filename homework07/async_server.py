import argparse
import asynchat
import asyncore
import logging
import mimetypes
import multiprocessing
import os
import socket
import urllib
from time import strftime, gmtime


def url_normalize(path):
    if path.startswith('.'):
        path = '/' + path
    while '../' in path:
        p1 = path.find('/..')
        p2 = path.rfind('/', 0, p1)
        if p2 != -1:
            path = path[:p2] + path[p1 + 3:]
        else:
            path = path.replace('/..', '', 1)
            path = path.replace('/./', '/')
            path = path.replace('/.', '')
    return path


class FileProducer(object):
    def __init__(self, file, chunk_size=4096):
        self.file = file
        self.chunk_size = chunk_size

    def more(self):
        if self.file:
            data = self.file.read(self.chunk_size)
            if data:
                return data
            self.file.close()
            self.file = None
        return ''


class AsyncServer(asyncore.dispatcher):
    def __init__(self, host='127.0.0.1', port=9000):
        super().__init__()
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        log.debug(f'Incoming connection from {addr}')
        AsyncHTTPRequestHandler(sock)

    def serve_forever(self):
        asyncore.loop()


class AsyncHTTPRequestHandler(asynchat.async_chat):
    def __init__(self, sock):
        super().__init__(sock)
        self.set_terminator(b'\r\n\r\n')

        self.method = ''
        self.urn = ''
        self.protocol = ''
        self.headers = {}
        self.content = ''

    def collect_incoming_data(self, data):
        log.debug(f'Incoming data: {data}')
        self._collect_incoming_data(data)

    def found_terminator(self):
        self.parse_request()

    def parse_request(self):
        if not self.headers:
            try:
                self.parse_headers()
            except:
                pass
            if not self.headers:
                self.send_error(400)
                self.handle_close()
            if self.method == 'POST':
                if (content_length := self.headers.get('content-length')) > 0:
                    self.set_terminator(int(content_length))
                else:
                    self.handle_request()
            else:
                self.handle_request()
        else:
            self.handle_request()

    def parse_headers(self):
        headers = b''.join(self.incoming).decode().split('\r\n')
        log.debug('Got headers, parsing...')

        proto_line, headers_lines = headers[0], headers[1:]
        method, urn, protocol = proto_line.split()
        log.debug(f'{method}, {urn}, {protocol}')
        log.debug(headers_lines)

        self.method, self.urn, self.protocol = method, urn, protocol

        headers_dict = {}
        for header in headers_lines:
            if header:
                name, value = map(lambda h: h.strip(), header.split(':', maxsplit=1))
                name = name.lower()  # According to RFC2616 Section 4.2, field names are case-insensitive
                headers_dict[name] = value
                log.debug(f'{name}: {value}')
        if (header := 'host') in headers_dict:
            headers_dict[header] = headers_dict[header].lower()  # According to RFC2616 Section 3.2.3
        if (header := 'content-length') in headers_dict:
            headers_dict[header] = int(headers_dict[header])

        self.headers = headers_dict
        log.debug('Headers parsing completed successfully!')

    def handle_request(self):
        method_name = 'do_' + self.method
        if not hasattr(self, method_name):
            self.send_error(405)
        else:
            handler = getattr(self, method_name)
            handler()
        self.handle_close()

    def send_header(self, keyword, value):
        self.push(f'{keyword}: {value}\r\n'.encode())

    def send_error(self, code, message=None):
        try:
            short_msg, long_msg = responses[code]
        except KeyError:
            short_msg, long_msg = '???', '???'
        if message is None:
            message = short_msg

        self.send_response(code, message)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Connection', 'close')
        self.end_headers()

    def send_response(self, code=200, message='OK'):
        self.push(f'HTTP/1.1 {code} {message}\r\n'.encode())

    def end_headers(self):
        self.push('\r\n'.encode())

    def date_time_string(self):
        pass

    def send_head(self):
        pass

    def translate_path(self, path):
        pass

    def do_GET(self):
        pass

    def do_HEAD(self):
        pass


responses = {
    200: ('OK', 'Request fulfilled, document follows'),
    400: ('Bad Request',
          'Bad request syntax or unsupported method'),
    403: ('Forbidden',
          'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed',
          'Specified method is invalid for this resource.'),
}


def parse_args():
    parser = argparse.ArgumentParser('Simple asynchronous web-server')
    parser.add_argument('--host', dest='host', default='127.0.0.1')
    parser.add_argument('--port', dest='port', type=int, default=9000)
    parser.add_argument('--log', dest='loglevel', default='info')
    parser.add_argument('--logfile', dest='logfile', default=None)
    parser.add_argument('-w', dest='nworkers', type=int, default=1)
    parser.add_argument('-r', dest='document_root', default='.')

    return parser.parse_args()


def run(args):
    server = AsyncServer(host=args.host, port=args.port)
    server.serve_forever()


logging.basicConfig(
    level='DEBUG',
    format='[%(levelname)s] (%(processName)-10s) (%(threadName)-10s) %(message)s'
)

log = logging.getLogger(__name__)

if __name__ == '__main__':
    args = parse_args()

    DOCUMENT_ROOT = args.document_root
    for _ in range(args.nworkers):
        p = multiprocessing.Process(target=run, args=(args,))
        p.start()
