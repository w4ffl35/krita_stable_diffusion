from krita import *
from krita_stable_diffusion.interface.interfaces.layout_base import LayoutBase
from krita_stable_diffusion.interface.widgets.dropdown import DropDown
from krita_stable_diffusion.interface.widgets.label import Label


class DropdownInterface(LayoutBase):
    def __init__(self, **kwargs):
        label = Label(label=kwargs.get("label", "Label"))
        dropdown = kwargs.get("dropdown", None)
        if not dropdown:
            dropdown = DropDown(
                options=kwargs.get("options", []),
                config_name=kwargs.get("config_name", None),
                max_width=kwargs.get("max_width", None),
            )
        super().__init__(
            widgets=[label, dropdown],
            interfaces=[],
            orientation=kwargs.get("orientation", "vertical"),
        )
