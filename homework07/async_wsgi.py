import argparse
import io
import multiprocessing
import sys
import logging as log

import async_server as httpd


class AsyncWSGIServer(httpd.AsyncServer):
    def __init__(self, host='localhost', port=9000):
        super(AsyncWSGIServer, self).__init__(host, port)

    def handle_accepted(self, sock, addr):
        print(f"Incoming connection from {addr}")
        AsyncWSGIRequestHandler(sock, self.addr, self.application)

    def set_app(self, application):
        self.application = application

    def get_app(self):
        return self.application


class AsyncWSGIRequestHandler(httpd.AsyncHTTPRequestHandler):
    def __init__(self, sock, server_addr, app):
        super(AsyncWSGIRequestHandler, self).__init__(sock, server_addr)
        self.application = app
        self.server_name = 'cs102-SimpleAsyncWSGIServer'

    def get_environ(self):
        env = {
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': io.StringIO(b''.join(self.incoming).decode()),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'REQUEST_METHOD': self.method,
            'PATH_INFO': self.urn,
            'SERVER_NAME': self.server_host,
            'SERVER_PORT': str(self.server_port)
        }
        return env

    def start_response(self, status, response_headers, exc_info=None):
        headers = {
            'Server': self.server_name,
            'Date': self.date_time_string(),
        }
        for name, value in response_headers:
            headers[name] = value

        self.response_headers = (status, headers)
        log.debug(self.response_headers)

    def handle_request(self):
        env = self.get_environ()
        app = self.application

        result = app(env, self.start_response)
        log.debug('Got result!')
        log.debug(result)
        self.finish_response(result)

    def finish_response(self, result):
        status, headers = self.response_headers
        code, message = status.split(maxsplit=1)

        self.send_response(int(code), message)

        for name, value in headers.items():
            self.send_header(name, value)
        self.end_headers()

        self.send(b''.join(result))
        self.handle_close()


def run(args):
    log.basicConfig(
        level=args.loglevel.upper(),
        filename=args.logfile,
        format='[%(levelname)s] (%(processName)-10s) (%(threadName)-10s) %(message)s'
    )

    module, app = args.app.split(':', maxsplit=1)
    module = __import__(module)
    application = getattr(module, app)

    server = AsyncWSGIServer(host=args.host, port=args.port)
    server.set_app(application)
    server.serve_forever()


def parse_args():
    parser = argparse.ArgumentParser("Simple asynchronous WSGI-server")
    parser.add_argument("app", metavar='app:module')
    parser.add_argument("--host", dest="host", default="127.0.0.1")
    parser.add_argument("--port", dest="port", type=int, default=9000)
    parser.add_argument('--log', dest='loglevel', default='info')
    parser.add_argument('--logfile', dest='logfile', default=None)
    parser.add_argument("-w", dest="nworkers", type=int, default=1)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    for _ in range(args.nworkers):
        p = multiprocessing.Process(target=run, args=(args,))
        p.start()
