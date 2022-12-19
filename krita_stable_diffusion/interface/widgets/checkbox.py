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

    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop("callback", False)
        self.checked = kwargs.pop("checked", False)
        super().__init__(*args, **kwargs)

    def set_value(self):
        partial(self.config.setValue, self.config_name)
        self.callback(is_checked=self.widget.isChecked())

    def create_widget(self):
        element = QCheckBox(self.label)
        # on click
        element.stateChanged.connect(lambda: self.set_value())
        element.setChecked(self.config.value(self.config_name, type=bool))
        self.widget = self.initialize_widget(element)
        self.widget.setChecked(self.checked)
