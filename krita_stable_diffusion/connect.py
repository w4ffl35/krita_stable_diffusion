import json
import os
import queue
import socket
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")
SDPATH = os.path.join(HOME, "stablediffusion")

SCRIPTS = {
    'txt2img': [
        ('prompt', ''),
        ('outdir', os.path.join(SDPATH, "txt2img")),
        ('skip_grid', ''),
        # ('skip_save', ''),
        ('ddim_steps', 50),
        ('plms', ''),
        # ('laion400m', ''),
        ('fixed_code', ''),
        ('ddim_eta', 0.0),
        ('n_iter', 1),
        ('H', 512),
        ('W', 512),
        ('C', 4),
        ('f', 8),
        ('n_samples', 1),
        ('n_rows', 0),
        ('scale', 7.5),
        # ('from-file', ''),
        ('config', os.path.join(SDPATH, 'configs/stable-diffusion/v1-inference.yaml')),
        ('ckpt', os.path.join(SDPATH, 'models/ldm/stable-diffusion-v1/model.ckpt')),
        ('seed', 42),
        ('precision', 'autocast'),
        ('do_nsfw_filter', ''),
    ],
    'img2img': [
        ('prompt', ''),
        ('init_img', ''),
        ('outdir', os.path.join(SDPATH, "img2img")),
        ('skip_grid', True),
        ('skip_save', False),
        ('ddim_steps', 50),
        ('plms', ''),
        ('fixed_code', True),
        ('ddim_eta', 0.0),
        ('n_iter', 1),
        ('H', 512),
        ('W', 512),
        ('C', 4),
        ('f', 8),
        ('n_samples', 2),
        ('n_rows', 0),
        ('scale', 5.0),
        ('strength', 0.75),
        ('from-file', ''),
        ('config', os.path.join(SDPATH, 'configs/stable-diffusion/v1-inference.yaml')),
        ('ckpt', os.path.join(SDPATH, 'models/ldm/stable-diffusion-v1/model.ckpt')),
        ('seed', 42),
        ('precision', 'autocast'),
        ('do_nsfw_filter', ''),
    ],
    'inpaint': [
        ('indir', f'{HOME}/inpaint/input'),
        ('outdir', f'{HOME}/inpaint'),
        ('steps', 50),
    ],
    'knn2img': [
        ('prompt', ''),
        ('outdir', f'{HOME}/knn2img'),
        ('skip_grid', True),
        ('ddim_steps', 50),
        ('n_repeat', 1),
        ('plms', True),
        ('ddim_eta', 0.0),
        ('n_iter', 1),
        ('H', 768),
        ('W', 768),
        ('n_samples', 1),
        ('n_rows', 0),
        ('scale', 5.0),
        ('from-file', ''),
        ('config', os.path.join(SDPATH, 'configs/retrieval-augmented-diffusion/768x768.yaml')),
        ('ckpt', os.path.join(SDPATH, 'models/rdm/rdm768x768/model.ckpt')),
        ('clip_type', 'ViT-L/14'),
        ('database', 'artbench-surrealism'),
        ('use_neighbors', False),
        ('knn', 10),
    ],
    'train_searcher': [
        ('d', 'stablediffusion/data/rdm/retrieval_database/openimages'),
        ('target_path', 'stablediffusion/data/rdm/searchers/openimages'),
        ('knn', 20),
    ],
}

class StableDiffusionRunner:
    """
    Run Stable Diffusion.
    """
    stablediffusion = None
    model = None
    device = None

    def process_data_value(self, key, value):
        """
        Process the data value. Ensure that we use the correct types.
        :param key: key
        :param value: value
        :return: processed value
        """
        if value == "true":
            return True
        if value == "false":
            return False
        if key in [
            "ddim_steps", "n_iter", "H", "W", "C", "f",
            "n_samples", "n_rows", "seed"
        ]:
            return int(value)
        if key in ["ddim_eta", "scale", "strength"]:
            return float(value)
        return value

    def process_options(self, options, data):
        """
        Process the data, compare aginast options.
        :param options: options
        :param data: data
        return: processed options
        """
        # get all keys from data
        keys = data.keys()
        for index, opt in enumerate(options):
            if opt[0] in keys:
                options[index] = (
                    opt[0],
                    self.process_data_value(
                        opt[0],
                        data.get(opt[0], opt[1])
                    )
                )
        return options

    def txt2img_sample(self, data):
        """
        Run txt2img sample.
        :param data: data
        return: result
        """
        print("Sampling txt2img")
        return self._txt2img_loader.sample(
            options=self.process_options(self.txt2img_options, data)
        )

    def img2img_sample(self, data):
        """
        Run img2img sample.
        :param data: data
        return: result
        """
        return self._img2img_loader.sample(
            options=self.process_options(self.img2img_options, data)
        )

    def __init__(self, *args, **kwargs):
        """
        Initialize the runner.
        """
        from stablediffusion.classes.txt2img import Txt2Img
        from stablediffusion.classes.img2img import Img2Img
        self.txt2img_options = kwargs.get("txt2img_options", None)
        self.img2img_options = kwargs.get("img2img_options", None)
        if self.txt2img_options is None:
            raise Exception("txt2img_options is required")
        if self.img2img_options is None:
            raise Exception("img2img_options is required")

        # start a txt2img loader instance
        self._txt2img_loader = Txt2Img(
            options=self.txt2img_options,
            model=self.model,
            device=self.device
        )
        # initialize img2img loader and pass it the same model and device
        self._img2img_loader = Img2Img(
            options=self.img2img_options,
            model=self._txt2img_loader.model,
            device=self._txt2img_loader.device
        )


class Connection:
    """
    Connects to Stable Diffusion service
    """

    threads = []
    pid = None  # keep track of krita process id

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
        print("Stopping connection thread...")
        for index in range(len(self.threads)):
            thread = self.threads[index]
            total = len(self.threads)
            name = thread.getName()
            print(f"{index+1} of {total} Stopping thread {name}")
            try:
                thread.join()
            except RuntimeError:
                print(f"Thread {thread.getName()} not running")
            print(f"Stopped thread {thread.getName()}...")
        print("All threads stopped")

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
    port = 50006
    host = "localhost"
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
        self.queue = queue.SimpleQueue()


class SocketServer(SocketConnection):
    """
    Opens a socket on a server and port.
    """
    max_client_connections = 1
    quit_event = None
    has_connection = False
    response_queue = None

    def reset_connection(self):
        """
        Reset connection to service
        :return: None
        """
        self.disconnect()
        self.initialize_socket()
        self.has_connection = False
        self.open_socket()

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

    def open_socket(self):
        """
        Open a socket conenction
        :return: None
        """
        try:
            self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.soc.settimeout(1)
            self.soc.bind((self.host, self.port))
        except socket.error as err:
            print(f"Failed to open a socket at {self.host}:{self.port}")
            print(str(err))
        except Exception as e:
            print(f"Failed to open a socket at {self.host}:{self.port}")
        print(f"Socket opened {self.soc}")

    def try_quit(self):
        """
        Try to quit the thread
        :return: None
        """
        has_krita_process = False
        import psutil
        for proc in psutil.process_iter():
            if int(proc.pid) == int(self.pid):
                has_krita_process = True
                break
        if not has_krita_process:
            print("krita process not found, quitting")
            self.quit_event.set()
            self.response_queue.put("quit")
            if self.soc_connection:
                self.soc_connection.close()
                self.soc_connection = None
            if self.queue:
                self.queue.put("quit")
        return self.quit_event.is_set()

    def handle_open_socket(self):
        """
        Listen for incoming connections.
        Returns:
        """
        print("Handle open socket")
        self.soc.listen(self.max_client_connections)
        self.soc_connection = None
        self.soc_addr = None
        while True:
            if not self.has_connection:
                try:
                    print("SERVER: awaiting connection")
                    if not self.quit_event.is_set():
                        self.soc_connection, self.soc_addr = self.soc.accept()
                    if self.soc_connection:
                        print(f"SERVER: connection from {self.soc_addr}")
                        self.has_connection = True
                except socket.timeout:
                    print("ERROR: SERVER: socket timeout")
                except Exception as exc:
                    print("ERROR: SERVER: socket error", exc)
                print(f"SERVER: connection established with {self.soc_addr}")

            if self.has_connection:
                msg = None
                try:
                    try:
                        msg = self.soc_connection.recv(1024)
                    except AttributeError:
                        pass
                    if msg is not None and msg != b'':
                        print(f"SERVER: message received")
                        # push directly to queue
                        self.message = msg
                except ConnectionResetError:
                    print("SERVER: connection reset")
                    self.reset_connection()

            if self.quit_event.is_set():
                break

            time.sleep(1)

        print("SERVER: server stopped")

        self.stop()

    def watch_connection(self):
        """
        Watch the connection and shutdown if the server if the connection
        is lost.
        """
        while True:
            if self.try_quit():
                print("SERVER: shutting down")
                break
            time.sleep(1)

    def __init__(self, *args, **kwargs):
        if not self.response_queue:
            self.response_queue = queue.SimpleQueue()
        super().__init__(*args, **kwargs)
        self.quit_event = threading.Event()
        self.quit_event.clear()
        self.max_client_connections = kwargs.get(
            "max_client_connections",
            self.max_client_connections
        )
        self.start_thread(
            target=self.worker,
            name="socket server worker"
        )
        self.start_thread(
            target=self.watch_connection,
            name="watch connection"
        )


class SocketClient(SocketConnection):
    has_connection = False

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
        while True:
            # check self.soc for connection
            if not self.has_connection:
                self.reset_connection()
                try:
                    print("CLIENT: connecting")
                    self.soc.connect((self.host, self.port))
                    self.has_connection = True
                    setattr(self.Application, "connected_to_sd", True)
                    self.soc.settimeout(None)
                    print("CLIENT: connected")
                except Exception as exc:
                    print("CLIENT: failed to connect", exc)
                    self.has_connection = False

            if self.quit_event.is_set():
                print("CLIENT: quitting")
                break

            if self.has_connection:
                try:
                    print("Waiting for response from server")
                    response = self.soc.recv(1024)
                    print("CLIENT: response received", response)
                    if self.quit_event.is_set():
                        break
                    self.handle_response(response)
                except socket.timeout:
                    self.has_connection = False
                    print("CLIENT: connection timed out")
                except Exception as exc:
                    self.has_connection = False
                    print("CLIENT: Connection lost", exc)
                if self.quit_event.is_set():
                    break
            if self.quit_event.is_set():
                break
            time.sleep(1)

    def close(self):
        """
        Close the socket
        :return:
        """
        print("Do Close")
        self.res_queue.put("quit")
        self.soc.shutdown(socket.SHUT_RDWR)
        self.has_connection = False
        self.quit_event.set()
        self.stop()

    def __init__(self, *args, **kwargs):
        self.Application = kwargs.get("Application")
        self.res_queue = queue.SimpleQueue()
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


class SimpleEnqueueSocketServer(SocketServer):
    """
    Simple socket server that enqueues messages to a queue
    """
    _failed_messages = []  # list to hold failed messages

    """
    Creates a SimpleQueue and waits for messages to append to it.
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
        Place incoming messages onto the queue
        """
        self.queue.put(msg)

    def worker(self):
        """
        Start a worker to handle request queue
        """
        print("SERVER WORKER: enqueue worker started")
        while True:
            print("SERVER WORKER: await connection")
            if self.has_connection:  # if a client is connected...
                print("SERVER WORKER: waiting for queue")
                msg = self.queue.get()  # get a message from the queue
                try:  # send to callback
                    self.callback(msg)
                except Exception as err:
                    print(f"SERVER: callback error: {err}")
                    pass
            if self.quit_event.is_set(): break
            time.sleep(1)
        print("SERVER WORKER: worker stopped")

    def __init__(self, *args, **kwargs):
        self.do_run = True
        self.queue = queue.SimpleQueue()
        super().__init__(*args, **kwargs)


class SimpleEnqueueSocketClient(SocketClient):
    """
    Creates a SimpleQueue and waits for messages to append to it.
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
        print("CLIENT: MESSAGE RECEIVED", msg)
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

    def handle_response(self, response):
        """
        Handle the response from the server
        :param response:
        :return: None
        """
        print("CLIENT: handle response")
        res = json.loads(response.decode("utf-8"))
        print(res)
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
                print(f"CLIENT: error in retry_message: {err}")
                pass

    def callback(self, message):
        """
        Callback function to handle messages
        :param message:
        :return: None
        """
        try:
            self.soc.sendall(json.dumps(message).encode("utf-8"))
        except BrokenPipeError:
            # keep track of failed messages and resend them
            # when we regain a connection
            self._failed_messages.append(message)
            self.has_connection = False
            self.disconnect()
            self.initialize_socket()
            print("CLIENT: lost connection to server")
        except Exception as err:
            print(f"CLIENT: error in callback: {err}")

    def handle_response_default(self, msg):
        """
        Handle the response from the server
        :param msg:
        :return: None
        """
        print("CLIENT: Pass handle_response to kwargs to override this method")

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
            if not self.queue.empty():
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
            print("Client waiting for message...")
            msg = self.res_queue.get()
            if msg == "quit":
                break
            print("Message received")
            try:
                msg = msg.decode("utf-8")
            except Exception as err:
                pass
            try:
                keys = msg.keys()
                self.callback(msg)
                continue
            except:
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


class StableDiffusionRequestQueueWorker(SimpleEnqueueSocketServer):
    """
    A socket server that listens for requests and enqueues them to a queue
    """
    def callback(self, data):
        """
        Handle a stable diffusion request message
        :return: None
        """
        response = None
        data = json.loads(data.decode("utf-8"))
        if data["type"] == "txt2img":
            response = self.sdrunner.txt2img_sample(data["options"])
        elif data["type"] == "img2img":
            response = self.sdrunner.img2img_sample(data["options"])
        if response is not None and response != b'':
            self.response_queue.put(response)

    def response_queue_worker(self):
        """
        Wait for responses from the stable diffusion runner and send
        them to the client
        """
        while True:
            print("SERVER: response queue worker")
            response = self.response_queue.get()
            if response == "quit":
                break
            res = json.dumps({"response": response})
            if res is not None and res != b'':
                print("SERVER: sending response")
                try:
                    self.soc_connection.sendall(res.encode("utf-8"))
                except Exception as e:
                    print("SERVER: failed to send response", e)
            if self.quit_event.is_set(): break
            time.sleep(1)

    def init_sd_runner(self):
        """
        Initialize the stable diffusion runner
        return: None
        """
        print("SERVER: starting Stable Diffusion runner")
        self.sdrunner = StableDiffusionRunner(
            txt2img_options=SCRIPTS["txt2img"],
            img2img_options=SCRIPTS["img2img"]
        )

        import torch  # this is a hack to get torch to load on the server
        torch.cuda.empty_cache()

    def __init__(self, *args, **kwargs):
        """
        Initialize the worker
        """
        self.response_queue = queue.SimpleQueue()
        self.pid = kwargs.get("pid")
        # create a stable diffusion runner service
        self.start_thread(
            target=self.response_queue_worker,
            name="response queue worker"
        )
        thread = self.start_thread(
            target=self.init_sd_runner,
            name="init stable diffusion runner"
        )
        thread.join()
        super().__init__(*args, **kwargs)


class StableDiffusionResponseQueueWorker(SimpleEnqueueSocketServer):
    """
    A socket server that listens for responses and enqueues them to a queue
    """
    def callback(self, message):
        """
        Handle a stable diffusion response message
        :return: None
        """
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
