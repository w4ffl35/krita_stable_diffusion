import json
import os

from krita import *
import logging
import random
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

    def send(self, data, request_type):
        data["type"] = request_type
        st = json.dumps(data)
        os.system(f"stablediffusion_client {self.string_to_binary(st)}")

    def tab(self):
        return self.widget, self.display_name

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
            if not self.config.contains(k):
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
        self.initialize_settings()
        self.reset_default_values()
        self.initialize_interfaces(interfaces)
