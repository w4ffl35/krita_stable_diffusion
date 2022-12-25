from krita import *
from .widget import Widget
from functools import partial


class DropDown(Widget):
    """
    Creates a dropdown menu with given options for use in an interface.
    :param label: The label of the dropdown menu
    :param options: The options to be displayed in the dropdown menu
    :param config_name: The name of the config to be set when the dropdown menu is changed
    :param callback: The callback to be called when the dropdown menu is changed
    """
    callback = None

    def __init__(self, *args, **kwargs):
        self.options = kwargs.pop("options", [])
        self.callback = kwargs.pop("callback", None)
        super().__init__(*args, **kwargs)

    def default_callback(self, val):
        self.config.setValue(self.config_name, val)
        self.config.sync()
        if self.callback:
            self.callback(val)

    def create_widget(self):
        element = QComboBox()
        element.addItems(self.options)
        current_index = 0
        for opt_index in range(len(self.options)):
            if self.options[opt_index] == self.config.value(self.config_name, type=str):
                current_index = opt_index
        element.setCurrentIndex(current_index)
        element.currentIndexChanged.connect(
            lambda: self.default_callback(element.currentText())
        )
        self.widget = self.initialize_widget(element)

    def update_options(self, options):
        self.clear()
        self.setOptions(options)

    def setOptions(self, options):
        self.widget.addItems(options)

    def clear(self):
        self.widget.clear()