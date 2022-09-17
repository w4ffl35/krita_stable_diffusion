from krita import *
from .widget import Widget
from functools import partial


class SpinBox(Widget):
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

    def create_widget(self):
        if self.double:
            element = QDoubleSpinBox()
        else:
            element = QSpinBox()

        element.setMinimum(self.min)
        element.setMaximum(self.max)

        if self.step:
            element.setSingleStep(self.step)

        if self.double:
            element.setValue(self.config.value(self.config_name, type=float))
        else:
            element.setValue(self.config.value(self.config_name, type=int))
        element.valueChanged.connect(partial(self.config.setValue, self.config_name))
        self.widget = element
