"""
Krita stable diffusion Controller class.
"""
import json
import sys
import threading
import time
import os
from krita_stable_diffusion.connect import SimpleEnqueueSocketClient
from krita import *
from krita_stable_diffusion.interface.widgets.label import Label
from krita_stable_diffusion.interface.interfaces.panel import KritaDockWidget
from krita_stable_diffusion.interface.menus.stable_diffusion_menu import StableDiffusionMenu

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
    def workaround_timeout(self):
        self.config.value('workaround_timeout', bool)

    @workaround_timeout.setter
    def workaround_timeout(self, value):
        self.config.setValue('workaround_timeout', value)

    def insert_images(self, msg):
        Application.image_queue.append(msg)

    def create_layer(self, name, visible=True, type="paintLayer"):
        """
        Creates a new layer in the active document
        :param name:
        :param type:
        :return: a reference to the new layer
        """
        document = self.active_document.createNode(name, type)
        self.root_node.addChildNode(document, None)
        return document

    def byte_array(self, image):
        """
        Convert QImage to QByteArray
        :param image:
        :return: QByteArray
        """
        bits = image.bits()
        bits.setsize(image.byteCount())
        return QByteArray(bits.asstring())

    def add_image_from_bytes(self, name, image_bytes):
        """
        Adds image from bytes
        :param name:
        :param image_bytes:
        :return:
        """
        print(f"adding image from bytes")

        # conver image_bytes byte string to byte array and set layer
        image = QImage()
        image.loadFromData(image_bytes)
        layer = self.create_layer(name)
        layer.setPixelData(self.byte_array(image), 0, 0, self.width(), self.height())

        # the layer is not visible until we refresh the projection
        self.active_document.refreshProjection()

        return layer

    def add_image(self, layer_name, path, visible=True):
        """
        Loads image from path and adds it to the active document
        :param layer_name:
        :param path:
        :param visible:
        :return:
        """
        print(f"adding image: {path}")
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
        if len(msg) > 1:
            # strip zero bytes from end of msg
            msg = msg.rstrip(b'\x00')

            # decode msg from binary string to json
            og_message = msg
            try:
                msg = msg.decode("utf-8", "ignore")
            except UnicodeDecodeError:
                print("UnicodeDecodeError")
                return

            # convert msg string to dict
            try:
                msg = json.loads(msg)
                if "image" in msg:
                    self.insert_images(msg)
                elif "action" in msg:
                    if msg["action"] == 4:  # progress
                        # get a reference to the main thread
                        Application.__setattr__("cur_reqtype", msg["reqtype"])
                        Application.__setattr__("step_total", msg["total"])
                        Application.__setattr__("cur_step", msg["step"])
                        return
            except json.decoder.JSONDecodeError:
                print("JSONDecodeError")
                # JSON decode error means that we have received
                # a potential image
                pass

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
        print("Handle stable diffusion response")
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

    def window_created(self):
        StableDiffusionMenu()

    def initialize_client(self):
        Application.__setattr__("status_label", Label(
            label=f"",
            alignment="left",
            padding=10
        ))
        Application.__setattr__("connection_label", Label(
            label=f"Not connected to localhost:5000",
            alignment="right",
            padding=10
        ))
        self.popup("Starting client")
        Krita.instance().eventFilter = self.eventFilter
        self.popup("Loading client")
        self.client = SimpleEnqueueSocketClient(
            port=50006,
            handle_response=self.stablediffusion_response_callback,
            status_change_callback=self.handle_status_change,
            Application=Application
        )
        Application.__setattr__("client", self.client)
        KRITA_INSTANCE = Krita.instance()
        if not KRITA_INSTANCE:
            print("No Krita instance!")
            sys.exit()
        self.start_thread(
            target=self.watch_connection,
            name="watch_connection"
        )

    def __init__(self, *args, **kwargs):
        self.client = None
        Application.__setattr__("connected_to_sd", False)
        super().__init__(*args, **kwargs)
        self.init_settings(**kwargs)
        self.create_stable_diffusion_panel()
        # self.popup(f"Plugin loaded {self}")
        Application.__setattr__("stablediffusion", self)
        self.initialize_client()
        Application.addDockWidgetFactory(
            DockWidgetFactory(
                "krita_stable_diffusion",
                DockWidgetFactoryBase.DockRight,
                KritaDockWidget
            )
        )
        # krita notifier for windowCreated
        Application.notifier().windowCreated.connect(self.window_created)


controller = Controller()
