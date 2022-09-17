from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.interface.tabs.base import Base
from krita_stable_diffusion.interface.widgets.button import Button
from krita_stable_diffusion.interface.widgets.checkbox import CheckBox
from krita_stable_diffusion.interface.widgets.dropdown import DropDown
from krita_stable_diffusion.interface.widgets.label import Label
from krita_stable_diffusion.settings import UPSCALERS


class UpscaleTab(Base):
    """
    UpscaleTab interface for the Krita Stable Diffusion plugin.
    :param name: The name of the tab
    :param interfaces: The interfaces to be added to the tab
    """

    name = "UpscaleTab"
    display_name = "Upscale"
    default_setting_values = {
        "upscaler": "",
        "downscale": False
    }

    def update_list_release_callback(self):
        pass

    def upscale_release_callback(self):
        pass

    def __init__(self):
        super().__init__([
            VerticalInterface(widgets=[
                Label(label="Upscalers"),
                DropDown(options=UPSCALERS, config_name="upscale_upscaler_name"),
                Button(label="Update list", release_callback=self.update_list_release_callback),
                Label(label="Downscale image x0.5 before upscaling"),
                CheckBox(label="Enable", config_name="downscale", default_value=self.default_setting_values["downscale"]),
                Button(label="Apply upscaler", callback=self.upscale_release_callback),
            ]),
        ])