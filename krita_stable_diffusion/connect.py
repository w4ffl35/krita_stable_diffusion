import json
import sys
import os
import queue
import socket
import threading
import time

import torch

sys.path.append("/home/joe/Projects/ai/stablediffusion/stablediffusion")

HOME = os.path.expanduser("~")
SDPATH = os.path.join(HOME, "stablediffusion")

SCRIPTS = {
    'txt2img': [
        ('prompt', ''),
        ('outdir', f'{HOME}/.stablediffusion/txt2img'),
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
        ('do_watermark', ''),
    ],
    'img2img': [
        ('prompt', ''),
        ('init_img', ''),
        ('outdir', f'{HOME}/.stablediffusion/img2img'),
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
        ('do_watermark', ''),
    ],
    'inpaint': [
        ('indir', f'{HOME}/.stablediffusion/inpaint/input'),
        ('outdir', f'{HOME}/.stablediffusion/inpaint'),
        ('steps', 50),
    ],
    'knn2img': [
        ('prompt', ''),
        ('outdir', f'{HOME}/.stablediffusion/knn2img'),
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
        ('config', 'stablediffusion/configs/retrieval-augmented-diffusion/768x768.yaml'),
        ('ckpt', '../models/rdm/rdm768x768/model.ckpt'),
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
    stablediffusion = None
    model = None
    device = None

    def connect(self):
        pass

    def start(self):
        pass

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
        # # get all keys from data
        # keys = data.keys()
        #
        # for index, opt in enumerate(options):
        #     if opt[0] in keys:
        #         options[index] = (
        #             opt[0],
        #             data[opt[0]]
        #         )
        # return options
        keys = data.keys()
        for index, opt in enumerate(options):
            if opt[0] in keys:
                options[index] = (opt[0], self.process_data_value(opt[0], data.get(opt[0], opt[1])))

    def txt2img_sample(self, data):
        print(self.process_options(self.txt2img_options, data))
        return self._txt2img_loader.sample(
            self.process_options(self.txt2img_options, data)
        )

    def img2img_sample(self, data):
        return self._img2img_loader.sample(
            self.process_options(self.img2img_options, data)
        )

    def __init__(self, *args, **kwargs):
        self.txt2img_options = kwargs.get("txt2img_options", None)
        self.img2img_options = kwargs.get("img2img_options", None)
        if self.txt2img_options is None:
            raise Exception("txt2img_options is required")
        if self.img2img_options is None:
            raise Exception("img2img_options is required")

        from classes.txt2img import Txt2Img
        from classes.img2img import Img2Img

        # start a txt2img loader instance
        self._txt2img_loader = Txt2Img(
            options=self.txt2img_options,
            model=self.model,
            device=self.device
        )


        # initialize img2img loader and pass it the same model and device
        # self._img2img_loader = Img2Img(
        #     options=self.img2img_options,
        #     model=self._txt2img_loader.model,
        #     device=self._txt2img_loader.device
        # )
        #super(StableDiffusionRunner, self).__init__(*args, **kwargs)


class Connection:
    """
    Connects to Stable Diffusion service
    """

    def connect(self):
        """
        Override this method to set up a connection to something.

        Do not call connect directly, it should be used in a thread.

        Use the start() method which starts this method in a new thread.
        :return: None
        """
        pass

    def disconnect(self):
        """
        Override this method to disconnect from something.
        :return: None
        """
        pass

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
        self.thread = threading.Thread(target=self.connect, daemon=False)
        self.thread.start()

    def stop(self):
        """
        Disconnects from service and stops the thread
        :return: None
        """
        self.disconnect()
        self.thread.join(timeout=0)

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
        self.thread = None
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
        pass

    def connect(self):
        self.open_socket()
        self.handle_open_socket()

    def disconnect(self):
        self.soc_connection.close()

    def __init__(self, *args, **kwargs):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        super().__init__(*args, **kwargs)


class SocketServer(SocketConnection):
    max_client_connections = 1

    @property
    def has_connection(self):
        return self.soc_connection is not None

    def callback(self, msg):
        """
        Override this method or pass it in as a parameter to handle messages
        :param msg:
        :return:
        """
        pass

    def worker(self):
        """
        Worker is started in a thread and waits for messages that are appended
        to the queue. When a message is received, it is passed to the callback
        method. The callback method should be overridden to handle the message.
        :return:
        """
        pass

    def open_socket(self):
        try:
            self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.soc.bind((self.host, self.port))
        except socket.error as err:
            print(f"Failed to open a socket at {self.host}:{self.port}")
            print(str(err))
        print(f"Socket opened {self.soc}")

    def handle_open_socket(self):
        """
        Listen for incoming connections.
        Returns:
        """
        self.soc.listen(self.max_client_connections)
        while True:
            self.soc_connection, self.soc_addr = self.soc.accept()
            print(f"Connection established with {self.soc_addr}")
            while True and self.soc_connection is not None:
                msg = self.soc_connection.recv(1024)
                if msg is not None and msg != b'':
                    print("Message received: ", msg)
                    self.message = msg
                time.sleep(1)
            time.sleep(1)

    def __init__(self, *args, **kwargs):
        self.max_client_connections = kwargs.get(
            "max_client_connections",
            self.max_client_connections
        )
        super().__init__(*args, **kwargs)
        self.worker_thread = threading.Thread(target=self.worker, daemon=False)
        self.worker_thread.start()


class SocketClient(SocketConnection):
    def callback(self, msg):
        """
        Override this method or pass it in as a parameter to handle messages
        :param msg:
        :return:
        """
        pass

    def worker(self):
        """
        Worker is started in a thread and waits for messages that are appended
        to the queue. When a message is received, it is passed to the callback
        method. The callback method should be overridden to handle the message.
        :return:
        """
        pass

    def connect(self):
        while True:
            print("Connecting...")
            self.soc.connect((self.host, self.port))
            print("connected...")
            while True:
                response = None
                try:
                    response = self.soc.recv(1024)
                except Exception as e:
                    print("Repsponse error")
                    print(e)
                if response:
                    print("PUTTING RESPONSE INTO QUEUE")
                    self.queue.put(response)
                time.sleep(1)

    def __init__(self, *args, **kwargs):
        self.queue = kwargs.get("queue", queue.SimpleQueue())
        super().__init__(*args, **kwargs)
        self.worker_thread = threading.Thread(target=self.worker, daemon=False)
        self.worker_thread.start()


class SimpleEnqueueSocketServer(SocketServer):
    """
    Creates a SimpleQueue and waits for messages to append to it.
    """
    @property
    def message(self):
        return ""

    @message.setter
    def message(self, msg):
        self.queue.put(msg)

    def worker(self):
        while True:
            print("simple enqueue worker")
            if self.has_connection:     # if a client is connected...
                msg = self.queue.get()  # get a message from the queue
                try:                    # send to callback
                    self.callback(msg)
                except Exception as err:
                    print(f"Error in callback: {err}")
            time.sleep(1)

    def __init__(self, *args, **kwargs):
        self.queue = kwargs.get("queue", queue.SimpleQueue())
        super().__init__(*args, **kwargs)


class SimpleEnqueueSocketClient(SocketClient):
    """
    Creates a SimpleQueue and waits for messages to append to it.
    """

    @property
    def message(self):
        return ""

    @message.setter
    def message(self, msg):
        self.queue.put(msg)

    def callback(self, message):
        print("SimpleEnqueueSocketClient")
        self.soc.sendall(json.dumps(message).encode("utf-8"))

    def worker(self):
        while True:
            msg = self.queue.get()
            try:
                self.callback(msg)
            except Exception as err:
                print(f"Error in callback: {err}")

    def __init__(self, *args, **kwargs):
        self.queue = kwargs.get("queue", queue.SimpleQueue())
        super().__init__(*args, **kwargs)


class StableDiffusionRequestQueueWorker(SimpleEnqueueSocketServer):

    def callback(self, data):
        """
        Handle a stable diffusion request message
        :return: None
        """
        print("SERVER CALLBACK")
        data = json.loads(data.decode("utf-8"))
        print(data)
        response = None
        if data["type"] == "txt2img":
            print("txt2img")
            response = self.sdrunner.txt2img_sample(data["options"])
        elif data["type"] == "img2txt":
            print("img2txt")
            response = self.sdrunner.img2img_sample(data["options"])
        print(response)
        if response is not None and response is not b'':
            print("RESPONSE FROM STABLE DIFFUSION")
            print(response)
            self.response_queue.put(response)


    def response_queue_worker(self):
        while True:
            print("rquest queue worker")
            response = self.response_queue.get()
            message = json.dumps(response)
            if message is not None and message is not b'':
                print("SENDING RESPONSE")
                self.soc_connection.sendall(message.encode("utf-8"))

    def init_sd_runner(self):
        print("Starting Stable Diffusion Runner...")
        self.sdrunner = StableDiffusionRunner(
            txt2img_options=SCRIPTS["txt2img"],
            img2img_options=SCRIPTS["img2img"]
        )
        torch.cuda.empty_cache()

    def __init__(self, *args, **kwargs):
        # create a stable diffusion runner service
        t = threading.Thread(target=self.init_sd_runner, daemon=False)
        t.start()
        t.join()
        self.response_queue = kwargs.get("response_queue", queue.SimpleQueue())
        if not self.response_queue:
            raise ValueError("response_queue is required")
        super().__init__(*args, **kwargs)


class StableDiffusionResponseQueueWorker(SimpleEnqueueSocketServer):
    def callback(self, message):
        """
        Handle a stable diffusion response message
        :return: None
        """
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

