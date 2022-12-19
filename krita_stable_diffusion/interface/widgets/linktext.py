from krita import *
from .widget import Widget


class LinkText(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.link = kwargs.get("link", "")

    def create_widget(self):
        element = QLabel(self.label)
        element.setText(f"<a href='{self.link}'>{self.label}</a>")
        element.setOpenExternalLinks(True)
        self.widget = self.initialize_widget(element)
