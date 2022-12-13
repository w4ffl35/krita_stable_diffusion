import os
import sys
from krita import *
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.interface.tabs.base import Base
from krita_stable_diffusion.interface.widgets.checkbox import CheckBox
from krita_stable_diffusion.interface.widgets.button import Button
from krita_stable_diffusion.interface.widgets.dropdown import DropDown
from krita_stable_diffusion.interface.widgets.line_edit import LineEdit
from krita_stable_diffusion.interface.widgets.label import Label


class ConfigTab(Base):
    """
    ConfigTab interface for the Krita Stable Diffusion plugin.
    :param name: The name of the tab
    :param interfaces: The interfaces to be added to the tab
    """
    name = "ConfigTab"
    display_name = "Config"
    default_setting_values = {
        "do_nsfw_filter": False,
        "do_watermark": False,
        "purge_temp_files": True,
        "aspect_ratio_correction": True,
        "restrict_tiling": True,
    }

    def restart_stable_diffusion(self, _element):
        """
        Restarts the Stable Diffusion Response connection
        """
        Application.sdresponse_connection.restart()
        # os.system("sudo systemctl restart stablediffusiond.service")
        # os.system("sudo systemctl restart stablediffusion_responsed.service")

    def __init__(self):
        super().__init__([
            VerticalInterface(widgets=[
                # drop down for selecting the model
                Label(label="Extra models path"),
                LineEdit(
                    placeholder="Extra models path",
                    config_name="model_path"
                ),
                CheckBox(label="NSFW Filter", config_name="do_nsfw_filter",
                         default_value=self.default_setting_values["do_nsfw_filter"]),
                CheckBox(label="Add Watermark", config_name="do_watermark",
                         default_value=self.default_setting_values["do_watermark"]),
                Button(label="Restart Stable Diffusion", release_callback=self.restart_stable_diffusion),
            ])
        ])
