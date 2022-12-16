from krita import *
from .widget import Widget

class ProgressBar(Widget):
    @property
    def value(self):
        return self.widget.value()

    """
    QProgressBar for use in an interface.
    :param label: The text displayed above the progress bar
    """
    def create_widget(self):
        element = QProgressBar()
        element.setRange(0, 100)
        element.text = "Generating"
        self.widget = self.initialize_widget(element)

    def setvalue(self, val, max):
        self.widget.setValue(val)
        self.widget.setMaximum(max)

    def reset(self):
        self.widget.reset()