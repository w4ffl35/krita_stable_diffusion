import base64
import os
import logging
import random
from krita import *
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.settings import APPLICATION_ID


class Base:
    """
    Extend this class to create a new tab for use in an interface.
    :param name: The name of the tab
    :param settings_key: The key of the settings to be used
    :param widget: The widget to add to the layout
    :param layout: The layout to add the widget to
    :param default_setting_values: The default values of the settings object
    """
    inserting_image = False
    krita_instance = None
    display_name = ""
    name = ""
    settings_key = ""
    widget = None
    layout = None
    default_setting_values = {}
    log_widget = None
    available_models = [
        "runwayml/stable-diffusion-v1-5",
        "w4ffl35/kqz",
    ]

    @property
    def color_mode(self):
        return self.config.value("color_mode", "RGBA")

    @property
    def resolution(self):
        return float(self.config.value("resolution", 300.0))

    @property
    def width(self):
        return int(self.config.value("width", 512))

    @property
    def height(self):
        return int(self.config.value("height", 512))

    @property
    def active_document(self):
        return self.krita.activeDocument()

    @property
    def active_node(self):
        return self.active_document.activeNode()

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
    def krita(self):
        if not self.krita_instance:
            self.krita_instance = Krita.instance()
        return self.krita_instance

    def string_to_binary(self, st):
        return ''.join(format(ord(i), '08b') for i in str(st))

    def build_prompt(self, data, image_type=None, style=None):
        if image_type and style:
            data["prompt"] = " ".join([
                f"{style} {image_type}",
                data["prompt"]
            ])
        return data

    def get_active_layer_binary(self):
        """
        Saves image to path
        :param path:
        :param is_mask:
        :return:
        """
        logging.info(f"saving layer...")
        item = self.active_document.activeNode()
        pixels = item.pixelData(self.x, self.y, self.width, self.height)
        image_data = QImage(
            pixels,
            self.width,
            self.height,
            QImage.Format_RGB32
        ).rgbSwapped()
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        image_data.save(buffer, "PNG", -1)
        return bytes(byte_array)

    def get_mask(self):
        """
        Get the mask from the top mask layer
        :return: mask as bytes
        """
        mask = None
        node = self.active_document.activeNode()
        childNodes = node.childNodes()
        for childNode in childNodes:
            if childNode.type() == "transparencymask":
                mask = childNode
                break
        if mask is None:
            return None
        pixels = mask.pixelData(0, 0, self.width, self.height)
        image_data = QImage(
            pixels,
            self.width,
            self.height,
            QImage.Format_Indexed8
        )

        image_data.invertPixels()

        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        image_data.save(buffer, "PNG", -1)
        return bytes(byte_array)

    def handle_button_press(self, request_type, **kwargs):
        """
        Callback for the txt2img button.
        :param _element: passed by the button but not used
        :return: None, sends request to stable diffusion
        """
        # prepare request data
        data = {}
        for k, v in self.default_setting_values.items():
            if k == "seed":
                v = self.seed()
            else:
                v = self.config.value(k, v)
            data[k] = v

        # add config options to request data
        data = self.prep_config_options(data)

        # build the prompt based on request data
        data = self.build_prompt(
            data,
            kwargs.get("image_type", None),
            kwargs.get("style", None)
        )

        # send request
        print("HANDLE BUTTON PRESS")

        if request_type in ["img2img", "inpaint"]:
            pixels = base64.b64encode(
                self.get_active_layer_binary()
            ).decode("utf-8")
            data["pixels"] = pixels

            if request_type == "inpaint":
                # get mask from top mask layer
                mask = self.get_mask()
                if mask:
                    print("FOUND MASK")
                    data["mask"] = base64.b64encode(mask).decode("utf-8")
                else:
                    print("NO MASK")
                    data["mask"] = mask

        # if there is no self.active_document, create one
        if not self.active_document:
            document = self.krita.createDocument(
                self.width,
                self.height,
                "StableDiffusion",
                self.color_mode,
                "U8",
                "",
                self.resolution
            )
            self.krita.activeWindow().addView(document)
            # activate the document
            self.krita.activeDocument().setActiveNode(
                self.krita.activeDocument().rootNode()
            )
        self.send(data, request_type)

    def update_progressbar(self):
        if Application.step != Application.progress_bar.value:
            Application.progress_bar.setvalue(
                Application.step,
                Application.total_steps
            )

    def update_image_insert(self):
        if len(Application.image_queue) > 0 and not self.inserting_image:
            self.inserting_image = True
            image = Application.image_queue.pop(0)
            self.insert_image(image)

    def progressbar_timed_update(self):
        self.progressbar_update_timer = QTimer()
        self.progressbar_update_timer.timeout.connect(self.update_progressbar)
        self.progressbar_update_timer.start(100)

    def image_insert_timed_update(self):
        self.image_insert_timer = QTimer()
        self.image_insert_timer.timeout.connect(self.update_image_insert)
        self.image_insert_timer.start(100)

    def byte_array(self, image):
        """
        Convert QImage to QByteArray
        :param image:
        :return: QByteArray
        """
        print(f"converting image to byte array")
        print(type(image))
        bits = image.bits()
        bits.setsize(image.byteCount())
        return QByteArray(bits.asstring())

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

    @property
    def root_node(self):
        doc = self.krita.activeDocument()
        if not doc:
            raise Exception("NO ACTIVE DOCUMENT")
        try:
            root = doc.rootNode()
        except RuntimeError:
            print("runtime error")
            # check if doc has been deleted
            if not doc:
                print("NO ACTIVE DOCUMENT")
            # rootNode has been deleted, fix it
            doc.setRootNode(doc.createNode("root", "paintLayer"))
            root = doc.rootNode()
        return root

    def insert_image(self, image):
        """
        Insert an image into the document
        :param image: The image to insert
        :return: None
        """
        total_layers = len(self.root_node.childNodes()) + 1
        self.add_image_from_bytes(f"Layer {total_layers}", image)

        self.inserting_image = False

    def send(self, options, request_type):
        """
        Send request to stable diffusion
        :param options: The options to send
        :param request_type: The type of request to send
        :return: None
        """
        self.log_message(f"Requesting {options['prompt']} {os.getpid()}...")
        Application.stablediffusion.client.message = {
            "action": request_type,
            "options": options,
        }

    message_log = []

    def log_message(self, message, level="info"):
        """
        Log a message to the log widget
        :param message: The message to log
        :param level: The level of the message
        :return: None
        """
        self.message_log.append(f"{level.upper()} {message}")
        if self.log_widget:
            self.log_widget.widget.setPlaceholderText(
                "\n".join(self.message_log)
            )

    def tab(self):
        return self.widget, self.display_name

    def prep_config_options(self, data):
        # add config options
        do_nsfw_filter = self.config.value("do_nsfw_filter", True)
        do_watermark = self.config.value("do_watermark", True)
        data["do_nsfw_filter"] = False if do_nsfw_filter == 0 else True
        data["do_watermark"] = False if do_watermark == 0 else True
        data["model"] = self.available_models[int(self.config.value("model", 0))]
        data["model_path"] = self.config.value("model_path", "")
        self.config.setValue("log", Application.stablediffusion.log)
        return data

    def initialize_settings(self):
        """
        Create tab specific settings
        :return:
        """
        self.settings_key = f"ksd_{self.name}_settings"
        Application.__setattr__(self.settings_key, QSettings(
            QSettings.IniFormat,
            QSettings.UserScope,
            "krita",
            APPLICATION_ID
        ))
        self.config = Application.__getattribute__(self.settings_key)

    def reset_default_values(self):
        # set default values
        for k, v in self.default_setting_values.items():
            self.config.setValue(k, v)

    def initialize_interfaces(self, interfaces):
        interfaces[0].addStretch()
        self.layout = VerticalInterface(interfaces=interfaces)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)

    def seed(self):
        seed = self.config.value("seed")
        if seed == "" or seed is None:
            seed = random.randint(0, 1000000)
        return seed

    def __init__(self, interfaces):
        Application.__setattr__("connected_to_sd", False)
        Application.__setattr__("log_message", self.send)
        Application.__setattr__("app", self)
        # get steps from config
        self.initialize_settings()
        #self.reset_default_values()
        self.config.sync()
        Application.__setattr__("step", 0)
        Application.__setattr__("total_steps", int(self.config.value("ddim_steps", 50)))
        Application.__setattr__("image_queue", [])
        self.initialize_interfaces(interfaces)
        self.log_message(f"Initialized with PID {os.getpid()}")
        self.progressbar_timed_update()
        self.image_insert_timed_update()
