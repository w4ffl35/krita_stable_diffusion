from krita import *
from krita_stable_diffusion.interface.tabs.generatetab import GenerateTab


class InpaintTab(GenerateTab):
    """
    InpaintTab interface for text to image generation.
    """
    name = "InpaintTab"
    display_name = "inpaint"
    config_name = "inpaint"
