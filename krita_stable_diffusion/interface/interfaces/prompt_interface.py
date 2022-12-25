from krita import *

from krita_stable_diffusion.interface.interfaces.dropdown_interface import DropdownInterface
from krita_stable_diffusion.interface.interfaces.plain_text_interface import PlainTextInterface
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.settings import SCHEDULERS, MODEL_VERSIONS


class PromptInterface(VerticalInterface):
    def __init__(self, **kwargs):
        section = kwargs.get("section", "txt2img")
        super().__init__(
            widgets=[],
            interfaces=[
                PlainTextInterface(
                    label="Prompt",
                    placeholder="prompt",
                    config_name=f"{section}_prompt",
                ),
                PlainTextInterface(
                    label="Negative Prompt",
                    placeholder="negative_prompt",
                    config_name=f"{section}_negative_prompt",
                ),
            ]
        )