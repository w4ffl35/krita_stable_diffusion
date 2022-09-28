"""
Krita stable diffusion Controller class.
"""
import json
import queue
import socket
import threading
import time
import os
import krita_stable_diffusion.logger as log
from krita import *


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


class StableDiffusionConnectionManager:
    def __init__(self, *args, **kwargs):
        """
        Initialize all connections and workers
        """
        # create queues
        self.request_queue = kwargs.get("request_queue", queue.SimpleQueue())
        self.response_queue = kwargs.get("response_queue", queue.SimpleQueue())

        # create request client
        print("creating request worker...")
        self.request_worker = StableDiffusionRequestQueueWorker(
            port=50006,
            pid=kwargs.get("pid"),
        )

from krita_stable_diffusion.interface.interfaces.panel import KritaDockWidget

HOME = os.path.expanduser("~")


class Controller(QObject):
    krita_instance = None
    config = None
    stop_socket_connection = None
    log = []
    threads = []
    first_run = True
    name = "Controller"

    def popup(self, message):
        # QMessageBox.information(
        #     QWidget(),
        #     "Stable Diffusion",
        #     message
        # )
        pass


    def start_thread(self, target, daemon=False, name=None):
        t = threading.Thread(target=target, daemon=daemon)
        if name:
            t.setName(name)
        t.start()
        self.threads.append(t)
        return t

    def stop(self):
        print("Stopping client")
        self.client.quit()
        for n in range(len(self.threads)):
            thread = self.threads[n]
            print(f"{n+1} of {len(self.threads)} Stopping thread {thread.getName()} from {self.name}...")
            try:
                thread.join()
            except:
                print("Failed to join thread")
            print(f"Stopped thread {thread.getName()}...")
        print(f"All threads in {self.name} stopped")

    @property
    def krita(self):
        if not self.krita_instance:
            self.krita_instance = Krita.instance()
        return self.krita_instance

    @property
    def selection(self):
        return self.active_document.selection()

    def x(self):
        return 0 if self.selection is None else self.selection.x()

    def y(self):
        return 0 if self.selection is None else self.selection.y()

    @property
    def active_document(self):
        return self.krita.activeDocument()

    @property
    def root_node(self):
        return self.active_document.rootNode()

    def width(self):
        return self.active_document.width() if self.selection is None else self.selection.width()

    def height(self):
        return self.active_document.height() if self.selection is None else self.selection.height()

    @property
    def img2img_base_size(self ):
        return self.config.value('img2img_base_size', int)

    @img2img_base_size.setter
    def img2img_base_size(self, value):
        self.config.setValue('img2img_base_size', value)

    @property
    def img2img_max_size(self):
        return self.config.value('img2img_max_size', int)

    @img2img_max_size.setter
    def img2img_max_size(self, value):
        self.config.setValue('img2img_max_size', value)

    @property
    def txt2img_seed(self):
        return self.config.value('txt2img_seed', int)

    @txt2img_seed.setter
    def txt2img_seed(self, value):
        self.config.setValue('txt2img_seed', value)

    @property
    def workaround_timeout(self):
        self.config.value('workaround_timeout', bool)

    @workaround_timeout.setter
    def workaround_timeout(self, value):
        self.config.setValue('workaround_timeout', value)

    @property
    def img2img_seed(self):
        self.config.value('img2img_seed', bool)

    @img2img_seed.setter
    def img2img_seed(self, value):
        self.config.setValue('img2img_seed', value)

    def stablediffusion_responsed_callback(self, response):
        """
        Handles response from Stable Diffusion service
        :param response:
        :return:
        """
        self.insert_images(response)
        self.active_document.refreshProjection()
        self.delete_generated_images(response)

    def insert_images(self, image_paths):
        """
        Inserts images into the active document
        :param image_paths:
        :return:
        """
        layer_name_prefix = "SD_txt2img:"
        print("Inserting images")
        for image_data in image_paths:
            print("IMAGE DATA", image_data)
            seed = image_data.__contains__("seed") or ""
            image_path = image_data["file_name"]
            self.add_image(f"{layer_name_prefix}:{seed}:{image_path}", image_path)

    def create_layer(self, name, visible=True, type="paintLayer"):
        """
        Creates a new layer in the active document
        :param name:
        :param type:
        :return: a reference to the new layer
        """
        log.info(f"creating layer")
        document = self.active_document.createNode(name, type)
        self.root_node.addChildNode(document, None)
        document.setVisible(visible)
        return document

    def byte_array(self, image):
        """
        Convert QImage to QByteArray
        :param image:
        :return: QByteArray
        """
        log.info(f"converting image to byte array")
        bits = image.bits()
        bits.setsize(image.byteCount())
        return QByteArray(bits.asstring())

    def add_image(self, layer_name, path, visible=True):
        """
        Loads image from path and adds it to the active document
        :param layer_name:
        :param path:
        :param visible:
        :return:
        """
        log.info(f"adding image: {path}")
        image = QImage()
        image.load(path, "PNG")
        print("Getting layer ", layer_name)
        layer = self.create_layer(layer_name, visible=visible)
        layer.setPixelData(self.byte_array(image), self.x(), self.y(), self.width(), self.height())

    def delete_generated_images(self, files):
        for file in files:
            os.remove(file)

    def init_settings(self, **kwargs):
        # create settings objects for various tabs and also main settings
        Application.__setattr__("krita_stable_diffusion_config", QSettings(
            QSettings.IniFormat,
            QSettings.UserScope,
            "krita",
            "krita_stable_diffusion"
        ))
        self.config = Application.krita_stable_diffusion_config
        self.config.setValue("server_connected", False)

        # initialize default settings
        for k, v in kwargs.get("defaults", {}).items():
            if not self.config.contains(k):
                self.config.setValue(k, v)

    def create_stable_diffusion_panel(self):
        Application.addDockWidgetFactory(
            DockWidgetFactory(
                "krita_stable_diffusion",
                DockWidgetFactoryBase.DockRight,
                KritaDockWidget
            )
        )

    def stablediffusion_response_callback(self, msg):
        print("STABLE DIFFUSION RESPONSE CALLBACK", msg)
        msg = json.loads(msg.decode("utf-8"))
        print(msg)
        print(type(msg))
        print(msg["response"])
        self.insert_images(msg["response"])

    def kritastablediffusion_service_start(self):
        """
        Launches kritastablediffusion service
        :return:
        """
        pass

    def request_prompt(self, message):
        """
        Sends prompt request to stable diffusion
        :param message:
        :return:
        """
        self.client.message = json.dumps(message).encode("ascii")

    def handle_sd_response(self, response):
        log.info("Handle stable diffusion response")
        # TODO handle image insertion here

    def try_quit(self):
        try:
            if Application.connected_to_sd and Application.activeWindow() is None:
                return True
        except Exception as e:
            print("application dead", e)
            pass
        return False

    def watch_connection(self):
        while True:
            if self.try_quit():
                print("CLIENT: QUITTING")
                self.client.close()
                break
            time.sleep(1)


    def handle_status_change(self, status):
        if status == "CONNECTED":
            self.config.setValue("sever_connected", True)
        else:
            self.config.setValue("sever_connected", False)

    def __init__(self, *args, **kwargs):
        Application.__setattr__("connected_to_sd", False)
        self.client = None
        super().__init__(*args, **kwargs)
        self.init_settings(**kwargs)
        self.create_stable_diffusion_panel()
        self.popup(f"Plugin loaded {self}")
        Application.__setattr__("stablediffusion", self)
        # on Application quit, close the server
        self.popup("Starting client")
        Krita.instance().eventFilter = self.eventFilter
        self.popup("Loading client")
        self.client = SimpleEnqueueSocketClient(
            port=50006,
            handle_response=self.stablediffusion_response_callback,
            status_change_callback=self.handle_status_change,
            Application=Application
        )
        # self.start_thread(
        #     target=self.kritastablediffusion_service_start,
        #     name="kritastablediffusion"
        # )
        self.start_thread(
            target=self.watch_connection,
            name="watch_connection"
        )


controller = Controller()
