from krita import *
from krita_stable_diffusion.interface.interfaces.layout_base import LayoutBase
from krita_stable_diffusion.interface.widgets.plain_text import PlainText
from krita_stable_diffusion.interface.widgets.label import Label


class PlainTextInterface(LayoutBase):
    def __init__(self, **kwargs):
        label = Label(label=kwargs.get("label", "Label"))
        txt = PlainText(
            placeholder=kwargs.get("placeholder", ""),
            config_name=kwargs.get("config_name", None),
        )
        super().__init__(
            widgets=[label, txt],
            interfaces=[],
            orientation=kwargs.get("orientation", "vertical"),
        )
