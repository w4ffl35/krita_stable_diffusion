from krita import *
from .widget import Widget


class PlainText(Widget):
    """
    Creates a plain text QWidget for use in an interface.
    :param placeholder: The placeholder text of the plain text
    :param config_name: The name of the config to be set
    """

    def create_widget(self):
        element = QPlainTextEdit()
        element.setPlaceholderText(self.placeholder)
        element.textChanged.connect(
            lambda: self.config.setValue(self.config_name, element.toPlainText())
        )
        element.setPlainText(self.config.value(self.config_name))
        self.widget = self.initialize_widget(element)
