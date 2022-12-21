from krita import *
from .widget import Widget
from functools import partial


class Slider(Widget):
    """
    Creates a spin box QWidget for use in an interface.
    :param label: The label of the spin box
    :param config_name: The name of the config value to be set
    :param min: The minimum value of the spin box
    :param max: The maximum value of the spin box
    :param step: The step value of the spin box
    :param double: Whether the spin box should be a double spin box
    """
    double = None

    def __init__(self, *args, **kwargs):
        self.parent = kwargs.pop("parent", None)
        self.callback = kwargs.pop("callback", None)
        self.double = kwargs.pop("double", False)
        super().__init__(*args, **kwargs)

    def on_change(self, val):
        # self.config.setValue(self.config_name, val)
        # self.config.sync()
        if self.callback:
            self.callback(val)

    def create_widget(self):
        element = QSlider(
            Qt.Horizontal,
            self.parent.widget,
        )
        element.setMinimum(self.min)
        element.setMaximum(self.max)
        element.valueChanged.connect(lambda v: self.on_change(v))
        self.widget = self.initialize_widget(element)
