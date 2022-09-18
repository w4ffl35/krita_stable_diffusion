import os
import sys
from krita import *
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.interface.tabs.base import Base
from krita_stable_diffusion.interface.widgets.checkbox import CheckBox
from krita_stable_diffusion.interface.widgets.button import Button


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
        Restarts the Stable Diffusion plugin.
        """
        Application.restart_stablediffusiond()
        # os.system("sudo systemctl restart stablediffusiond.service")
        # os.system("sudo systemctl restart stablediffusion_responsed.service")

    def __init__(self):
        super().__init__([
            VerticalInterface(widgets=[
                CheckBox(label="NSFW Filter", config_name="do_nsfw_filter", default_value=self.default_setting_values["do_nsfw_filter"]),
                CheckBox(label="Add Watermark", config_name="do_watermark", default_value=self.default_setting_values["do_watermark"]),
                CheckBox(label="Auto delete temp files", config_name="purge_temp_files", default_value=self.default_setting_values["purge_temp_files"]),
                CheckBox(label="Try to fix aspect ratio for selections", config_name="aspect_ratio_correction", default_value=self.default_setting_values["aspect_ratio_correction"]),
                CheckBox(label="Allow tiling only with no selection (on full image)", config_name="restrict_tiling", default_value=self.default_setting_values["restrict_tiling"]),
                Button(label="Restart Stable Diffusion", release_callback=self.restart_stable_diffusion),
            ])
        ])
