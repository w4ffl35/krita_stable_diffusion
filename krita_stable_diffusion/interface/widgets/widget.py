from krita import *


class Widget(QWidget):
    """
    Base widget class. This class should be inherited by all widgets.
    """
    attributes = []

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.widget = None

        # set the config object so that variables are accessible to all widgets
        self.config = Application.krita_stable_diffusion_config

        # set attributes
        self.initialize_args(kwargs)

        # generate the widget
        self.create_widget()

    def initialize_args(self, kwargs):
        """
        This method sets the attributes on the widget based on the kwargs passed to the widget
        :param kwargs:
        :return:
        """
        for k,v in kwargs.items():
            setattr(self, k, v)

    def create_widget(self):
        """
        This method should be overwritten by the widget class
        :return:
        """
        pass