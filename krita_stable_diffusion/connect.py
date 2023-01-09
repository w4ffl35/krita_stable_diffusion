import base64
import json
import os
import queue
import socket
import threading
import time
import logging
from krita_stable_diffusion.settings import DEFAULT_HOST, DEFAULT_PORT, CHUNK_SIZE
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
SDPATH = os.path.join("stablediffusion")


class Connection:
    """
    Connects to Stable Diffusion service
    """
    threads = []

    def start_thread(self, target, daemon=False, name=None):
        """
        Start a thread.
        :param target: target
        :param daemon: daemon
        :param name: name
        return: thread
        """
        thread = threading.Thread(target=target, daemon=daemon)
        if name:
            thread.setName(name)
        thread.start()
        self.threads.append(thread)
        return thread

    def connect(self):
        """
        Override this method to set up a connection to something.

        Do not call connect directly, it should be used in a thread.

        Use the start() method which starts this method in a new thread.
        :return: None
        """

    def disconnect(self):
        """
        Override this method to disconnect from something.
        :return: None
        """

    def reconnect(self):
        """
        Disconnects then reconnects to service. Does not stop the thread.
        :return: None
        """
        self.disconnect()
        self.connect()

    def start(self):
        """
        Starts a new thread with a connection to service.
        :return: None
        """
        self.start_thread(
            target=self.connect,
            name="Connection thread"
        )

    def stop(self):
        """
        Disconnects from service and stops the thread
        :return: None
        """
        self.disconnect()
        logger.info("Stopping connection thread...")
        for index in range(len(self.threads)):
            thread = self.threads[index]
            total = len(self.threads)
            name = thread.getName()
            logger.info(f"{index+1} of {total} Stopping thread {name}")
            try:
                thread.join()
            except RuntimeError:
                logger.info(f"Thread {thread.getName()} not running")
            logger.info(f"Stopped thread {thread.getName()}...")
        logger.info("All threads stopped")

    def restart(self):
        """
        Stops the thread and starts a new one which in turn stops and starts
        connection to service.
        :return: None
        """
        self.stop()
        self.start()

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self.start()


class SocketConnection(Connection):
    """
    Opens a socket on a server and port.

    parameters:
    :host: Hostname or IP address of the service
    :port: Port of the service
    """
    port = DEFAULT_PORT
    host = DEFAULT_HOST
    soc = None
    soc_connection = None
    soc_addr = None

    def open_socket(self):
        """
        Open a socket conenction
        :return:
        """

    def handle_open_socket(self):
        """
        Override this method to handle open socket
        :return:
        """

    def connect(self):
        """
        Open a socket and handle connection
        :return: None
        """
        self.open_socket()
        self.handle_open_socket()

    def disconnect(self):
        """
        Disconnect from socket
        :return: None
        """
        if self.soc_connection:
            self.soc_connection.close()
        self.soc.close()
        self.soc_connection = None

    def initialize_socket(self):
        """
        Initialize a socket. Use timeout to prevent constant blocking.
        :return: None
        """
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.settimeout(3)

    def __init__(self, *args, **kwargs):
        """
        Initialize the socket connection, call initialize socket prior
        to calling super because super will start a thread calling connect,
        and connect opens a socket.

        Failing to call initialize socket prior to super will result in an error
        """
        self.initialize_socket()
        super().__init__(*args, **kwargs)
        self.queue = queue.Queue()


class SocketClient(SocketConnection):
    has_connection = False
    connecting = False

    def callback(self, msg):
        """
        Override this method or pass it in as a parameter to handle messages
        :param msg:
        :return:
        """

    def worker(self):
        """
        Worker is started in a thread and waits for messages that are appended
        to the queue. When a message is received, it is passed to the callback
        method. The callback method should be overridden to handle the message.
        :return:
        """

    def reset_connection(self):
        """
        Reset connection to service
        :return: None
        """
        self.disconnect()
        self.initialize_socket()
        self.has_connection = False

    def handle_response(self, response):
        """
        Handle the response from the server
        :param response:
        :return:
        """
        self.queue.put(response)

    def connect(self):
        """
        Connect to the server
        :return:
        """
        sleep_time = 1
        if self.connecting:
            return
        self.connecting = True
        logger.info("CLIENT: connecting")
        while True:
            # check self.soc for connection
            if not self.has_connection:
                self.reset_connection()
                try:
                    self.soc.connect((self.host, self.port))
                    self.has_connection = True
                    setattr(self.Application, "connected_to_sd", True)

                    connection_label = self.Application.__getattribute__("connection_label")
                    if connection_label:
                        self.Application.connection_label.setText(
                            f"Connected to {self.host}:{self.port}"
                        )
                    self.soc.settimeout(None)
                    logger.info("CLIENT: connected")
                except ConnectionRefusedError as exc:
                    logger.info("CLIENT: failed to connect - connection refused", exc)
                    self.has_connection = False

            if self.quit_event.is_set():
                logger.info("CLIENT: quitting")
                break

            if self.has_connection:
                try:
                    # recieve message in CHUNK_SIZE byte chunks
                    response = b""
                    total_bytes_recieved = 0
                    n = 0
                    while self.has_connection:
                        chunk = self.soc.recv(CHUNK_SIZE)

                        if not chunk:
                            self.has_connection = False

                        # check if chunk is CHUNK_SIZE 00 bytes
                        if chunk == b'\x00' * CHUNK_SIZE:
                            break
                        response += chunk
                        total_bytes_recieved += len(chunk)
                        n+=1
                except socket.timeout:
                    self.has_connection = False
                    logger.warning("CLIENT: connection timed out")
                except Exception as exc:
                    self.has_connection = False
                    logger.error("CLIENT: Connection lost", exc)
                if self.quit_event.is_set():
                    break

                if self.has_connection:
                    sleep_time = 0
                else:
                    sleep_time = 1

                if self.quit_event.is_set():
                    break

                if not self.has_connection and connection_label:
                    self.Application.connection_label.setText(
                        f"Not connected to {self.host}:{self.port}"
                    )
                self.handle_response(response)
            if self.quit_event.is_set():
                break
            time.sleep(sleep_time)

    def close(self):
        """
        Close the socket
        :return:
        """
        logger.info("Do Close")
        self.res_queue.put("quit")
        self.soc.shutdown(socket.SHUT_RDWR)
        self.has_connection = False
        self.quit_event.set()
        self.stop()

    def __init__(self, *args, **kwargs):
        self.Application = kwargs.get("Application")
        self.res_queue = queue.Queue()
        self.quit_event = threading.Event()
        self.quit_event.clear()
        super().__init__(*args, **kwargs)
        self.start_thread(
            target=self.worker,
            name="socket client worker"
        )
        self.start_thread(
            target=self.connect,
            name="socket client connect"
        )


class SimpleEnqueueSocketClient(SocketClient):
    """
    Creates a Queue and waits for messages to append to it.
    """

    @property
    def message(self):
        """
        Does nothing. Only used for the setter.
        """
        return ""

    @message.setter
    def message(self, msg):
        """
        Set the message property
        """
        logger.info("Putting message in queue")
        self.queue.put(msg)

    @property
    def response(self):
        """
        Get the response from the server
        :return: response string
        """
        return ""

    @response.setter
    def response(self, msg):
        """
        Set the response
        :param msg:
        :return: None
        """
        self.res_queue.put(msg)

    @staticmethod
    def handle_response_default(_msg):
        """
        Handle the response from the server
        :param _msg:
        :return: None
        """
        logger.info("CLIENT: Pass handle_response to kwargs to override this method")

    def handle_response(self, response):
        """
        Handle the response from the server
        :param response:
        :return: None
        """
        res = json.loads(response.decode("utf-8"))
        if "response" in res:
            self.response = response
        else:
            self.message = response

    def retry_messages(self):
        """
        TODO: implement this function
        :return:
        """
        failed_messages = self._failed_messages
        for message in failed_messages:
            try:
                # remove message from failed messages
                self._failed_messages.remove(message)
                self.callback(message)
            except Exception as err:
                logger.info(f"CLIENT: error in retry_message: {err}")
                pass

    def pad_chunk(self, chunk):
        """
        Pad the chunk to expected size in bytes
        :param chunk:
        :return:
        """
        return chunk.ljust(CHUNK_SIZE, b"\x00")

    def send_end_signal(self):
        """
        send a byte string consisting of CHUNK_SIZE null bytes
        this tells the server we are done sending messages
        :return:
        """
        self.soc.sendall(b"\x00" * CHUNK_SIZE)

    def send_message(self, message):
        """
        Ease of use function to send a message to the server
        """
        self.callback(message)

    def callback(self, message):
        """
        Callback function to handle messages
        send a request to server
        :param message:
        :return: None
        """
        logger.info("CLIENT: callback")
        try:
            # encode the message
            message = json.dumps(message).encode("utf-8")

            # ensure message is at least CHUNK_SIZE bytes
            if len(message) < CHUNK_SIZE:
                message += b"\x00" * (CHUNK_SIZE - len(message))

            # send message in chunks
            n = 0
            while len(message) > 0:
                chunk = message[:CHUNK_SIZE]
                chunk = self.pad_chunk(chunk)
                self.soc.send(chunk)
                message = message[CHUNK_SIZE:]
                n+=1
            self.send_end_signal()
        except BrokenPipeError:
            logger.error("BrokenPipeError")
            # keep track of failed messages and resend them
            # when we regain a connection
            self._failed_messages.append(message)
            self.has_connection = False
            self.disconnect()
            self.initialize_socket()
            logger.info("CLIENT: lost connection to server")
        except Exception as err:
            logger.error(f"CLIENT: error in callback: {err}")

    def quit(self):
        """
        Quit the client
        :return: None
        """
        self.quit_event.set()
        self.res_queue.put("quit")
        self.queue.put("quit")

    def worker(self):
        """
        Worker thread to handle responses from the server
        :return: None
        """
        while True:
            if self.quit_event.is_set():
                break
            # check if we are connected to server
            if self.has_connection and not self.queue.empty():
                msg = self.queue.get()
                if msg == "quit":
                    self.quit_event.set()
                    break
                self.callback(msg)
            time.sleep(1)

    def response_worker(self):
        """
        Wait for responses from the server
        :return: None
        """
        while True:
            msg = self.res_queue.get()
            if msg == "quit":
                break
            try:
                msg = msg.decode("utf-8")
            except Exception as err:
                logger.error("Failed to decode message", err)
                pass
            try:
                self.callback(msg)
                continue
            except Exception as err:
                logger.error("Something went wrong ", err)
                pass
            if msg != "" and msg is not None:
                self.handle_response(msg)
            if self.quit_event.is_set(): break

    def __init__(self, *args, **kwargs):
        """
        Initialize the client
        """
        self._failed_messages = []
        self.handle_response = kwargs.get(
            "handle_response",
            self.handle_response_default
        )
        super().__init__(*args, **kwargs)
        self.start_thread(
            self.response_worker,
            name="response worker"
        )