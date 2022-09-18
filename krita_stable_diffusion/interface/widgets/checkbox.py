from krita import *
from .widget import Widget
from functools import partial


class CheckBox(Widget):
    """
    Creates a checkbox QWidget for use in an interface.
    :param label: The label of the checkbox
    :param default_value: The default value of the checkbox
    :param config_name: The name of the config value to be set on checkbox state change
    """
    def create_widget(self):
        element = QCheckBox(self.label)
        element.setChecked(self.config.value(self.config_name, type=bool))
        element.stateChanged.connect(partial(self.config.setValue, self.config_name))
        self.widget = self.initialize_widget(element)