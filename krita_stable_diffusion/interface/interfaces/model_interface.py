from krita import *

from krita_stable_diffusion.interface.interfaces.dropdown_interface import DropdownInterface
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.settings import SCHEDULERS, MODEL_VERSIONS


class ModelInterface(HorizontalInterface):
    def __init__(self, **kwargs):
        section = kwargs.get("section", "txt2img")
        super().__init__(
            widgets=[],
            interfaces=[
                DropdownInterface(
                    label="Scheduler",
                    options=SCHEDULERS,
                    config_name=f"{section}_scheduler",
                ),
                DropdownInterface(
                    label="Version",
                    options=MODEL_VERSIONS,
                    config_name=f"{section}_model_version",
                    max_width=100,
                ),
                DropdownInterface(
                    label="Model",
                    dropdown=kwargs.get("dropdown", None),
                ),
            ]
        )