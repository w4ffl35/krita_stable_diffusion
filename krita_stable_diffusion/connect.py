import sys
import os
import queue
import json
import socket
import threading
import logger as log

# add krita_stable_diffusion.stablediffusion to import path
sys.path.append("/home/joe/Projects/ai/stablediffusion/stablediffusion")

from stablediffusion.classes.txt2img import Txt2Img
from stablediffusion.classes.img2img import Img2Img

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


class StablediffusionresponsedConnection(Connection):
    """
    Connects to stablediffusion_responsed service over a socket.

    parameters:
    :host: Hostname or IP address of the service
    :port: Port of the service
    """
    conn = None

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((
            self.kwargs.get("host", "localhost"),
            self.kwargs.get("port", 50007),
        ))
        print("Starting stablediffusion_responsed listener")
        # open a connection to localhost:50007
        check_stream = True
        while check_stream:
            response = None
            try:
                response = json.loads(self.conn.recv(1024))
            except Exception as e:
                print(e)
                check_stream = False
            if response:
                self.callback(response)

    def disconnect(self):
        self.conn.close()

    def __init__(self, *args, **kwargs):
        self.callback = kwargs.get("callback", None)
        super().__init__(*args, **kwargs)


class SimpleEnqueue(Connection):
    """
    Creates a SimpleQueue and waits for messages to append to it.
    """
    message = None
    do_receive = False

    def connect(self):
        """
        Recieves messages and adds them to the Queue
        :return:
        """
        self.do_receive = True
        while self.do_receive:
            self.enqueue()

    def enqueue(self):
        if self.message:
            self.queue.put(self.message)
            self.message = None

    def disconnect(self):
        self.do_receive = False

    def __init__(self, *args, **kwargs):
        # create a new SimpleQueue or use the one passed via kwargs
        self.queue = kwargs.get("queue", queue.SimpleQueue())
        super().__init__(*args, **kwargs)


class SimpleDequeue(SimpleEnqueue):
    def connect(self):
        """
        Gets messages from the Queue
        :return:
        """
        self.do_receive = True
        while self.do_receive:
            self.message = self.queue.get()
            self.message_handler(self.message)

    def message_handler(self, message):
        """
        Override this method to handle messages
        :param message: The message to handle
        :return: None
        """
        pass


class StableDiffusionRunner(Connection):
    stablediffusion = None
    model = None
    device = None

    def connect(self):
        """
        Start Stable Diffusion
        :return: None
        """
        # start a txt2img loader instance
        self._txt2img_loader = Txt2Img(
            options=self.txt2img_options,
            model=self.model,
            device=self.device
        )

        # store model and device for re-use
        self.model = self._txt2img_loader.model
        self.device = self._txt2img_loader.device

        # initialize img2img loader and pass it the same model and device
        self._img2img_loader = Img2Img(
            options=self.img2img_options,
            model=self._txt2img_loader.model,
            device=self._txt2img_loader.device
        )

    def process_options(self, options, data):
        # get all keys from data
        keys = data.keys()

        for index, opt in enumerate(options):
            if opt[0] in keys:
                options[index] = (
                    opt[0],
                    data[opt[0]]
                )
        return options

    def txt2img_sample(self, data):
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
        super(StableDiffusionRunner, self).__init__(*args, **kwargs)


class StableDiffusionRequestQueueWorker(SimpleDequeue):
    def message_handler(self, data):
        """
        Handle a stable diffusion request message
        :return: None
        """
        response = None
        try:
            response = self.stablediffusion.__getattribute__(
                f'{data["method"]}_sample')(data["options"]
            )
        except AttributeError as e:
            log.error(f"Method {data['method']} not found")
            log.error(e)
        if response is not None:
            self.response_queue.put(response)

    def __init__(self, *args, **kwargs):
        self.stablediffusion = kwargs.get("stablediffusion", None)
        self.response_queue = kwargs.get("response_queue", None)
        if not self.stablediffusion:
            raise ValueError("stablediffusion is required")
        if not self.response_queue:
            raise ValueError("response_queue is required")
        super().__init__(*args, **kwargs)


class StableDiffusionResponseQueueWorker(SimpleDequeue):
    def message_handler(self, message):
        """
        Handle a stable diffusion response message
        :return: None
        """
        self.callback(message)

    def __init__(self, *args, **kwargs):
        self.callback = kwargs.get("callback", None)
        super().__init__(*args, **kwargs)


class StableDiffusionConnectionManager:
    def stop_stable_diffusion(self):
        # stop the stablediffusion runner
        pass

    def start_request_connection(self):
        self.request_connection.start()

    def stop_request_connection(self):
        self.request_connection.stop()

    def restart_request_connection(self):
        self.request_connection.restart()

    def start_response_connection(self):
        self.request_connection.start()

    def stop_response_connection(self):
        self.request_connection.stop()

    def restart_response_connection(self):
        self.request_connection.restart()

    def start_request_worker(self):
        self.request_worker.start()

    def stop_request_worker(self):
        self.request_worker.stop()

    def restart_request_worker(self):
        self.request_worker.restart()

    def start_response_worker(self):
        self.response_worker.start()

    def stop_response_worker(self):
        self.response_worker.stop()

    def restart_response_worker(self):
        self.response_worker.restart()

    def start(self):
        """
        Start all connections and workers
        :return: None
        """
        self.start_request_connection()
        self.start_response_connection()
        self.start_request_worker()
        self.start_response_worker()

    def stop(self):
        """
        Stop all connections and workers
        :return: None
        """
        self.stop_request_connection()
        self.stop_response_connection()
        self.stop_request_worker()
        self.stop_response_worker()

    def restart(self):
        """
        Restart all connections and workers
        :return: None
        """
        self.restart_request_connection()
        self.restart_response_connection()
        self.restart_request_worker()
        self.restart_response_worker()

    def __init__(self, callback=None):
        """
        Initialize all connections and workers
        """

        # Callback used for respone queue worker
        if not callback:
            raise ValueError("callback is required")

        # create queues
        self.request_queue = queue.SimpleQueue()
        self.response_queue = queue.SimpleQueue()

        # create a stable diffusion runner service
        log.info("Starting Stable Diffusion Runner...")
        self.stablediffusion = StableDiffusionRunner(
            txt2img_options=SCRIPTS["txt2img"],
            img2img_options=SCRIPTS["img2img"]
        )

        # create request connection thread
        log.info("creating request connection...")
        self.request_connection = SimpleEnqueue(queue=self.request_queue)

        # create response connection thread
        log.info("creating response connection...")
        self.response_connection = SimpleEnqueue(queue=self.response_queue)

        # create worker thread which
        # 1. waits for messages on the request_queue
        # 2. sends the request to stable diffusion
        # 3. adds the response to the response_queue
        log.info("creating request worker...")
        self.request_worker = StableDiffusionRequestQueueWorker(
            queue=self.request_queue,
            response_queue=self.response_queue,
            stablediffusion=self.stablediffusion,
        )

        # create worker thread which
        # 1. waits for messages on the response_queue
        # 2. sends the response to the client
        log.info("creating response worker...")
        self.response_worker = StableDiffusionResponseQueueWorker(
            queue=self.response_queue,
            callback=callback
        )
