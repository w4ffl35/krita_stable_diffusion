from krita import *
from krita_stable_diffusion.interface.tabs.generatetab import GenerateTab


class Txt2ImgTab(GenerateTab):
    """
    Txt2ImgTab interface for text to image generation.
    """
    name = "Txt2ImgTab"
    display_name = "txt2img"
    config_name = "txt2img"
