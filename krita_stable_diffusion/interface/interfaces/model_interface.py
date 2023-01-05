from krita import *

from krita_stable_diffusion.interface.interfaces.dropdown_interface import DropdownInterface
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.settings import SCHEDULERS, MODEL_VERSIONS, MODELS


class ModelInterface(HorizontalInterface):
    def version_callback(self, _version):
        self.model_dropdown_interface.dropdown.update_options(self.model_options)

    @property
    def model_options(self):
        version = self.config.value(f"{self.section}_model_version", "v1")
        if version == "v1":
            return Application.available_models_v1
        elif version == "v2":
            return Application.available_models_v2
        elif version == "v1 (community)":
            return Application.available_models_custom_v1
        elif version == "v2 (community)":
            return Application.available_models_custom_v2

    def __init__(self, **kwargs):
        self.section = kwargs.get("section", "txt2img")
        self.config = Application.krita_stable_diffusion_config
        self.model_dropdown_interface = DropdownInterface(
            label="Model",
            options=self.model_options,
            config_name=f"{self.section}_model"
        )
        super().__init__(
            widgets=[],
            interfaces=[
                DropdownInterface(
                    label="Scheduler",
                    options=SCHEDULERS,
                    config_name=f"{self.section}_scheduler",
                ),
                DropdownInterface(
                    label="Version",
                    options=MODEL_VERSIONS,
                    config_name=f"{self.section}_model_version",
                    max_width=100,
                    callback=self.version_callback,
                ),
                self.model_dropdown_interface,
            ]
        )