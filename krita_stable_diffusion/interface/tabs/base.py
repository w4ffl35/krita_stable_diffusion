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
    krita_instance = None
    display_name = ""
    name = ""
    settings_key = ""
    widget = None
    layout = None
    default_setting_values = {}
    log_widget = None

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
    def width(self):
        return self.active_document.width() if self.selection is None else self.selection.width()

    @property
    def height(self):
        return self.active_document.height() if self.selection is None else self.selection.height()

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
        self.send(data, request_type)

    def send(self, options, request_type):
        st = {
            "type": request_type,
            "options": options,
        }
        # os.system(f"stablediffusion_client {self.string_to_binary(st)}")
        Application.stablediffusion.client.message = st
        if self.log_widget:
            self.log_widget.widget.setPlaceholderText(
                f"Requesting {options['prompt']}..."
            )

    def tab(self):
        return self.widget, self.display_name

    def prep_config_options(self, data):
        # add config options
        do_nsfw_filter = self.config.value("do_nsfw_filter", True)
        data["do_nsfw_filter"] = False if do_nsfw_filter == 0 else True
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

    def save_active_node_to_png(self, path, is_mask=False):
        """
        Saves image to path
        :param path:
        :param is_mask:
        :return:
        """
        logging.info(f"saving layer...")
        # get pixels from active node or document
        item = self.active_node if is_mask else self.active_document
        pixels = item.pixelData(self.x, self.y, self.width, self.height)
        image_data = QImage(pixels, self.width, self.height, QImage.Format_RGBA8888).rgbSwapped()
        image_data.save(path, "PNG", -1)

    def seed(self):
        seed = self.config.value("seed")
        if seed == "" or seed is None:
            seed = random.randint(0, 1000000)
        return seed

    def __init__(self, interfaces):
        Application.__setattr__("connected_to_sd", False)
        self.initialize_settings()
        self.reset_default_values()
        self.initialize_interfaces(interfaces)
