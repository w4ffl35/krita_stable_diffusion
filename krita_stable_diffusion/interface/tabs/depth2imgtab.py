from krita import *
from krita_stable_diffusion.interface.tabs.generatetab import GenerateTab


class Depth2ImgTab(GenerateTab):
    """
    Depth2ImgTab interface for depth to image generation.
    """
    name = "Depth2ImgTab"
    display_name = "depth2img"
    config_name = "depth2img"
