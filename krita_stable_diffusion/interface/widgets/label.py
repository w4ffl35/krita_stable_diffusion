from krita import *
from .widget import Widget


class Label(Widget):
    """
    Creates a label QWidget for use in an interface.
    :param label: The text of the label
    :return: None
    """
    def create_widget(self):
        element = QLabel(self.label)
        self.widget = self.initialize_widget(element)
