from krita import *

from krita_stable_diffusion.interface.interfaces.dropdown_interface import DropdownInterface
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.settings import SCHEDULERS, MODEL_VERSIONS, MODELS


class ModelInterface(HorizontalInterface):
    @property
    def model_names(self):
        return [m["name"] for m in self.model_options]

    def version_callback(self, _version):
        self.model_dropdown_interface.dropdown.update_options(self.model_names)

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

        # Set the model dropdown interface. This is referenced when changing
        # model versions by the version dropdown callback function.
        self.model_dropdown_interface = DropdownInterface(
            label="Model",
            options=self.model_names,
            config_name=f"{self.section}_model"
        )

        # handle optional scheduler dropdown
        show_scheduler = kwargs.get("show_scheduler", True)
        scheduler_dropdown_interface = None
        if show_scheduler:
            scheduler_dropdown_interface = DropdownInterface(
                label="Scheduler",
                options=SCHEDULERS,
                config_name=f"{self.section}_scheduler",
            )

        # handle optional data type dropdown
        show_data_type = kwargs.get("show_data_type", False)
        data_type_dropdown_interface = None
        if show_data_type:
            data_type_dropdown_interface = DropdownInterface(
                label="Data type",
                options=["float32", "float16"],
                config_name=f"{self.section}_data_type",
            )

        # handle optional model output type dropdown
        show_model_output_type = kwargs.get("show_model_output_type", False)
        model_output_type_dropdown_interface = None
        if show_model_output_type:
            model_output_type_dropdown_interface = DropdownInterface(
                label="Model output type",
                options=["ckpt", "safetensors", "diffusers"],
                config_name=f"{self.section}_model_output_type",
            )

        super().__init__(
            widgets=[],
            interfaces=[
                scheduler_dropdown_interface,
                DropdownInterface(
                    label="Version",
                    options=MODEL_VERSIONS,
                    config_name=f"{self.section}_model_version",
                    max_width=100,
                    callback=self.version_callback,
                ),
                self.model_dropdown_interface,
                data_type_dropdown_interface,
                model_output_type_dropdown_interface,
            ]
        )