from krita import *


class Widget(QWidget):
    """
    Base widget class. This class should be inherited by all widgets.
    """
    attributes = []
    min_width = None
    max_width = None
    max_height = None
    disabled = False
    config_name = None
    placeholder = ""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.widget = None
        self.config_name = kwargs.get("config_name", None)
        self.label = kwargs.get("label", "")
        self.update_value = kwargs.get("update_value", self.update_value)
        self.min_width = kwargs.get("min_width", None)
        self.max_width = kwargs.get("max_width", None)
        self.max_height = kwargs.get("max_height", None)
        self.disabled = kwargs.get("disabled", False)

        # set the config object so that variables are accessible to all widgets
        self.config = Application.krita_stable_diffusion_config

        # set attributes
        self.initialize_args(kwargs)

        # generate the widget
        self.create_widget()


    def initialize_widget(self, widget):
        if self.min_width:
            widget.setMinimumWidth(self.min_width)
        if self.max_width:
            widget.setMaximumWidth(self.max_width)
        if self.max_height:
            widget.setMaximumHeight(self.max_height)
        widget.setDisabled(self.disabled)
        return widget

    def initialize_args(self, kwargs):
        """
        This method sets the attributes on the widget based on the kwargs passed to the widget
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            v = self.config.value(k, v)
            setattr(self, k, v)

    def create_widget(self):
        """
        This method should be overwritten by the widget class
        :return:
        """
        pass

    def update_value(self, name, val):
        self.config.setValue(name, val)
        # save the config to disk
        self.config.sync()
