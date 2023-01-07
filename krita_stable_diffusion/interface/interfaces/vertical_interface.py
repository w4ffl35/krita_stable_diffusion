from krita import *


class VerticalInterface(QVBoxLayout):
    """
    A collection of widgets and interfaces in a vertical layout container (QVBoxLayout)
    :param widgets: A list of widgets to add to the interface
    :param interfaces: A list of interfaces to add to the interface
    """

    def __init__(self, widgets=[], interfaces=[]):
        super().__init__()
        self.add_widgets(widgets)
        self.add_interfaces(interfaces)
        self.setAlignment(Qt.AlignTop)

    def add_widgets(self, widgets):
        """
        Add each widget from list of widgets to this interface
        :param widgets:
        :return:
        """
        for widget in widgets:
            self.addWidget(widget.widget)

    def add_interfaces(self, interfaces):
        """
        Add each interface from list of interfaces to this interface
        :param interfaces:
        :return:
        """
        for interface in interfaces:
            if not interface:
                continue
            if isinstance(interface, QBoxLayout):
                self.addLayout(interface)
            else:
                self.addLayout(interface.layout)
