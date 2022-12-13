import random
import http.client
import json
import socket
import threading


class API:
    _message = None

    def __init__(self, response_callback):
        self.response_callback = response_callback

    def quit(self):
        pass

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value
        self.send_request()

    def send_request(self):
        url = 'http://localhost:5000/'
        # random seed
        seed = random.randint(0, 1000000)
        conn = http.client.HTTPConnection("localhost", 5000)
        conn.request(
            "POST",
            "/",
            json.dumps(self.message),
            {
                'Content-Type': "application/json",
                'Cache-Control': "no-cache",
            }
        )
        res = conn.getresponse()
        data = res.read()
        self.response_callback(data)

    def close(self):
        pass


class SocketAPI(API):
    def __init__(self, response_callback):
        super().__init__(response_callback)
        self.conn = None
        self.connect()

        # listen in a separate thread
        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.start()

    def connect(self):
        # create a socket connection to server
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(('localhost', 5000))

    def close(self):
        self.conn.close()
        self.listen_thread.join()

    def send_request(self):
        self.conn.sendall(self.message)

    def listen(self):
        data = b''
        while True:
            chunk = self.conn.recv(1024)
            if not chunk:
                self.response_callback(data)
                data = b''
            data += chunk
