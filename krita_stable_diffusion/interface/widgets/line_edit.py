from krita import *
from .widget import Widget


class LineEdit(Widget):
    """
    Creates a line edit QWidget for use in an interface.
    :param label: The label of the line edit
    :param placeholder: The placeholder text of the line edit
    :param config_name: The name of the config to be set when the line edit is changed
    """

    def create_widget(self):
        element = QLineEdit()
        element.setPlaceholderText(self.placeholder)
        element.textChanged.connect(
            lambda: self.config.setValue(self.config_name, element.text())
        )
        element.setText(self.config.value(self.config_name))
        self.widget = self.initialize_widget(element)
