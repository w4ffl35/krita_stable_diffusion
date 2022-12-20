from krita import *
from .widget import Widget

class ProgressBar(Widget):
    """
    QProgressBar for use in an interface.
    :param label: The text displayed above the progress bar
    """
    min = 0
    max = 100
    current_value = 0

    @property
    def value(self):
        return self.widget.value()

    def __init__(self, *args, **kwargs):
        self.min = kwargs.pop("min", self.min)
        self.max = kwargs.pop("max", self.max)
        self.current_value = kwargs.pop("current_value", self.current_value)
        super().__init__(*args, **kwargs)

    def create_widget(self):
        element = QProgressBar()
        element.setRange(self.min, self.max)
        element.text = "Generating"
        self.element = element
        self.widget = self.initialize_widget(element)

    def setRange(self, min, max):
        self.element.setMinimum(min)
        self.element.setMaximum(max)

    def setvalue(self, val, max):
        self.element.setValue(val)
        self.element.setMaximum(max - 1)

    def reset(self):
        self.element.reset()
