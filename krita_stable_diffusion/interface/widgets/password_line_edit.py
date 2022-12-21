from krita import *
from .widget import Widget


class PasswordLineEdit(Widget):
    """
    Creates a line edit QWidget for use in an interface.
    :param label: The label of the line edit
    :param placeholder: The placeholder text of the line edit
    :param config_name: The name of the config to be set when the line edit is changed
    """
    config_name = None
    password = ""

    def create_widget(self):
        element = QLineEdit()
        element.setPlaceholderText(self.placeholder)
        self.widget = self.initialize_widget(element)
        element.setEchoMode(QLineEdit.Password)
