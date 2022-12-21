from krita import *
from krita_stable_diffusion.interface.tabs.generatetab import GenerateTab


class Img2ImgTab(GenerateTab):
    """
    Img2ImgTab interface for text to image generation.
    """
    name = "Img2ImgTab"
    display_name = "img2img"
    config_name = "img2img"
