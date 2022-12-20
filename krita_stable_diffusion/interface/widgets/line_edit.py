from krita import *
from .widget import Widget


class LineEdit(Widget):
    """
    Creates a line edit QWidget for use in an interface.
    :param label: The label of the line edit
    :param placeholder: The placeholder text of the line edit
    :param config_name: The name of the config to be set when the line edit is changed
    """
    def __init__(self, *args, **kwargs):
        self.max = kwargs.pop("max", None)
        super().__init__(*args, **kwargs)

    def update_value(self, config_name, value):
        if self.max and value and value != "" and int(value) > self.max:
            value = self.max
            self.widget.setText(str(value))
        super().update_value(config_name, value)

    def create_widget(self):
        element = QLineEdit()
        element.setPlaceholderText(self.placeholder)
        if self.config_name:
            element.textChanged.connect(
                lambda: self.update_value(self.config_name, element.text())
            )
            element.setText(str(self.config.value(self.config_name)))
        self.widget = self.initialize_widget(element)
