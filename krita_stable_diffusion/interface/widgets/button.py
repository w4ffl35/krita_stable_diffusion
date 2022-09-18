from krita import *
from .widget import Widget


class Button(Widget):
    """
    Creates a button QWidget for use in an interface.
    :param label: The label of the button
    :param release_callback: The callback to be called when the button is released
    """
    release_callback = None

    def create_widget(self):
        """
        Creates a button QWidget for use in an interface.
        :param label: The text of the button
        :param release_callback: The function to be called when the button is released
        :return: None
        """
        element = QPushButton(self.label)
        element.released.connect(lambda: self.release_callback(element))
        self.widget = self.initialize_widget(element)

    def handle_button_release(self, element):
        pass