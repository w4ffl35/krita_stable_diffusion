from krita import *
from .widget import Widget


class Label(Widget):
    """
    Creates a label QWidget for use in an interface.
    :param label: The text of the label
    :return: None
    """
    def __init__(self, *args, **kwargs):
        self.alignment = kwargs.pop("alignment", "left")
        self.padding = kwargs.pop("padding", 0)
        super().__init__(*args, **kwargs)

    def align_element(self, element):
        alignment = Qt.AlignLeft
        if self.alignment == "right":
            alignment = Qt.AlignRight
        elif self.alignment == "center":
            alignment = Qt.AlignCenter
        element.setAlignment(alignment)
        return element

    def create_widget(self):
        element = QLabel(self.label)
        element = self.align_element(element)

        # set width
        if self.max_width:
            element.setMaximumWidth(self.max_width)

        # add padding to element
        element.setContentsMargins(self.padding, self.padding, self.padding, self.padding)

        self.widget = self.initialize_widget(element)

    def setText(self, text):
        self.widget.setText(text)
