from krita import *
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface


class LayoutBase:
    def __init__(self, **kwargs):
        interface_kwargs = {
            "widgets": kwargs.get("widgets", []),
            "interfaces": kwargs.get("interfaces", []),
        }
        if kwargs.get("orientation", "vertical") == "vertical":
            self.layout = VerticalInterface(**interface_kwargs)
        else:
            self.layout = HorizontalInterface(**interface_kwargs)
