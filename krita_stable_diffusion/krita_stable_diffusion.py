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
from krita_stable_diffusion.settings import MODELS
from krita_stable_diffusion.settings import DEFAULT_HOST, DEFAULT_PORT
from krita_stable_diffusion.settings import VERSION
from subprocess import Popen
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.interface.widgets.button import Button
CREATE_NEW_CONSOLE = None
try:
    from subprocess import CREATE_NEW_CONSOLE
except:
   pass


class Controller(QObject):
    """
    Krita stable diffusion Controller class.
    """
    krita_instance = None
    config = None
    stop_socket_connection = None
    log = []
    threads = []
    first_run = True
    name = "Controller"
    version_check_timer = None
    version_checked = False
    update_available = False
    window_is_created = False

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

    @property
    def x(self):
        return 0 if self.selection is None else self.selection.x()

    @property
    def y(self):
        return 0 if self.selection is None else self.selection.y()

    @property
    def active_document(self):
        return self.krita.activeDocument()

    @property
    def root_node(self):
        return self.active_document.rootNode()

    @property
    def width(self):
        return self.active_document.width() if self.selection is None else self.selection.width()

    @property
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
        layer.setPixelData(self.byte_array(image), 0, 0, self.width, self.height)

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
        layer.setPixelData(self.byte_array(image), self.x, self.y, self.width, self.height)

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
                elif "versions" in msg:
                    versions = msg["versions"]
                    # set versions here
                    self.versions = versions
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
        self.start_server()
        StableDiffusionMenu()
        # time.sleep(3)
        self.version_check()

    def initialize_client(self):
        Application.__setattr__("status_label", Label(
            label=f"",
            alignment="left",
            padding=10
        ))
        Application.__setattr__("update_button", Button(
            label="Update",
            release_callback=self.update_plugin,
            padding=10,
            disabled=True
        ))
        Application.__setattr__("connection_label", Label(
            label=f"Not connected to {DEFAULT_HOST}:{DEFAULT_PORT}",
            alignment="right",
            padding=10
        ))
        self.popup("Starting client")
        Krita.instance().eventFilter = self.eventFilter
        self.popup("Loading client")
        self.client = SimpleEnqueueSocketClient(
            port=DEFAULT_PORT,
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

    def load_base_models(self, model_list):
        """
        Iterate over each model string in model_list and prefix self.config.value("model_base_path", "")
        :param model_list:
        :return:
        """
        model_base_path = self.config.value("model_base_path", "")
        for model in model_list:
            model["path"] = os.path.join(model_base_path, model["path"])
        return model_list

    def load_extra_models(self, path):
        # find all ckpt files in config.model_path
        # check recursively for ckpt files
        config = Application.krita_stable_diffusion_config
        model_path = config.value(path, None)
        extra_models = []
        if model_path:
            # get a list of directories in model_path
            dirs = [os.path.join(model_path, d) for d in os.listdir(model_path)]
            for dir in dirs:
                is_diffusers = True
                # check if dir has ckpt files in it
                ckpt_files = [f for f in os.listdir(dir) if f.endswith(".ckpt")]
                st_files = [f for f in os.listdir(dir) if f.endswith(".safetensors")]
                # check if dir has all required_files
                required_files = [
                    "scheduler/scheduler_config.json",
                    "text_encoder/config.json",
                    "text_encoder/pytorch_model.bin",
                    "tokenizer/merges.txt",
                    "tokenizer/special_tokens_map.json",
                    "tokenizer/tokenizer_config.json",
                    "tokenizer/vocab.json",
                    "unet/config.json",
                    "unet/diffusion_pytorch_model.bin",
                    "vae/config.json",
                    "vae/diffusion_pytorch_model.bin",
                ]

                for file in required_files:
                    if not os.path.exists(os.path.join(dir, file)):
                        is_diffusers = False
                        print("is not diffusers", os.path.join(dir, file))
                        break

                    display_name = dir if is_diffusers else file

                    # check if name already exists in extra_models
                    add_data = True
                    for m in extra_models:
                        if m["name"] == display_name:
                            add_data = False
                            break

                    # check if file already exists in extra_models
                    if add_data:
                        data = {
                            "name": display_name,
                            "path": os.path.join(model_path, display_name),
                        }
                        extra_models.append(data)

                for file in ckpt_files:
                    # check if name already exists in extra_models
                    add_data = True
                    for m in extra_models:
                        if m["name"] == file:
                            add_data = False
                            break

                    # check if file already exists in extra_models
                    if add_data:
                        data = {
                            "name": file,
                            "path": os.path.join(dir, file),
                        }
                        extra_models.append(data)

        return extra_models

    def update_extra_models(self):
        Application.available_models_v1 = self.load_base_models(MODELS["v1"])
        Application.available_models_v2 = self.load_base_models(MODELS["v2"])
        Application.available_models_custom_v1 = self.load_extra_models("model_path_v1")
        Application.available_models_custom_v2 = self.load_extra_models("model_path_v2")

    def convert_model_to_diffusers(self):
        print("CONVERT MODEL TO DIFFUSERS")

    def update_plugin(self, _element):
        """
        Downloads the latest releases from github in background and stores them.
        :return:
        """
        print("run updates")

        # send message to server requesting an upgrade
        self.client.send_message({
            "action": "update",
            "version": VERSION
        })

    def start_server(self):
        """
        Starts the server
        :return:
        """
        # get krita resources folder
        here = os.path.dirname(os.path.realpath(__file__))
        # get platform
        platform = sys.platform
        if platform == "linux":
            Popen(
                os.path.join(here, "runai", "runai --timeout"),
                shell=True
            )
        else:
            # windows
            Popen(
                f"{here}\\runai\\runai --timeout",
                creationflags=CREATE_NEW_CONSOLE
            )

    def version_check(self):
        """
        Checks if there are any server or client updates available.
        :return:
        """
        versions = self.versions
        current_ksd_version = self.config.value("current_ksd_version", VERSION)
        current_runai_version = versions["current_runai_version"]
        latest_ksd_version = versions["latest_ksd_version"]
        latest_runai_version = versions["latest_runai_version"]

        if current_ksd_version and current_runai_version and latest_ksd_version and latest_runai_version:
            print("VERSION CHECK COMPLETED")
            # all values have been set by the server
            self.version_checked = True
            if current_runai_version != latest_runai_version or current_ksd_version != latest_ksd_version:
                # versions are out of sync, tell the user to update
                self.update_available = True
            else:
                print("NO UPDATE AVAILABLE")

            if self.update_available:
                self.plugin_versions = {
                    "current_ksd_version": current_ksd_version,
                    "current_runai_version": current_runai_version,
                    "latest_ksd_version": latest_ksd_version,
                    "latest_runai_version": latest_runai_version
                }
                Application.update_button.widget.setDisabled(False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = None
        Application.__setattr__("connected_to_sd", False)
        self.init_settings(**kwargs)
        Application.__setattr__("stablediffusion", self)
        self.initialize_client()
        Application.__setattr__("available_models_v1", MODELS["v1"])
        Application.__setattr__("available_models_v2", MODELS["v2"])
        Application.__setattr__("available_models_custom_v1", [])
        Application.__setattr__("available_models_custom_v2", [])
        Application.__setattr__("model_version", 1)
        Application.__setattr__("update_extra_models", self.update_extra_models)
        Application.__setattr__("convert_model_to_diffusers", self.convert_model_to_diffusers)

        print("*" * 800)
        print("version_check")
        # connect to https://raw.githubusercontent.com/w4ffl35/krita_stable_diffusion/master/VERSION
        # and print the contents of the response

        # the following attributes are set by a push request from the server
        # on server start. They are used to determine if the client and server
        # software versions are up-to-date
        Application.__setattr__("current_ksd_version", VERSION)
        Application.__setattr__("current_runai_version", None)
        Application.__setattr__("latest_ksd_version", None)
        Application.__setattr__("latest_runai_version", None)

        # Application.__setattr__(
        #     "txt2img_available_models_dropdown",
        #     DropDown(options=[], config_name="txt2img_model")
        # )
        # Application.__setattr__(
        #     "img2img_available_models_dropdown",
        #     DropDown(options=[], config_name="img2img_model")
        # )
        # Application.__setattr__(
        #     "inpaint_available_models_dropdown",
        #     DropDown(options=[], config_name="inpaint_model")
        # )
        # Application.__setattr__(
        #     "outpaint_available_models_dropdown",
        #     DropDown(options=[], config_name="outpaint_model")
        # )
        # Application.__setattr__(
        #     "outpaint_available_models_dropdown",
        #     DropDown(options=[], config_name="outpaint_model")
        # )
        self.update_extra_models()
        self.create_stable_diffusion_panel()
        Application.notifier().windowCreated.connect(self.window_created)


controller = Controller()
