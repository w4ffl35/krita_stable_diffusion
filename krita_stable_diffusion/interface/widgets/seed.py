from krita import *
from .line_edit import LineEdit


class SeedLineEdit(LineEdit):
    """
    Creates a line edit QWidget for use in an interface.
    :param label: The label of the line edit
    :param placeholder: The placeholder text of the line edit
    :param config_name: The name of the config to be set when the line edit is changed
    """
    def update_value(self, name, val):
        if int(val) > self.max:
            val = self.max
        super().update_value(name, int(val))
