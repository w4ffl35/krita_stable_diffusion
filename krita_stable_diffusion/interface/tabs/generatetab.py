import os
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.interface.tabs.base import Base
from krita_stable_diffusion.interface.widgets.plain_text import PlainText
from krita_stable_diffusion.settings import DEFAULT_MODEL, DEFAULT_SCHEDULER

class GenerateTab(Base):
    """
    GenerateTab interface for the Krita Stable Diffusion plugin.
    :param name: The name of the tab
    :param interfaces: The interfaces to be added to the tab
    """
    HOME = os.path.expanduser("~")
    SDDIR = os.path.join(HOME, "stablediffusion")
    name = "GenerateTab"
    submit_button = None
    display_name = "Generate images"
    default_setting_values = {
        "txt2img_prompt": "",
        "txt2img_negative_prompt": "",
        "txt2img_steps": 20,
        "txt2img_ddim_eta": 0.0,  # only applies to ddim scheduler
        "txt2img_n_iter": 1,
        "txt2img_height": 512,
        "txt2img_width": 512,
        "txt2img_n_samples": 1,
        "txt2img_scale": 7.5,
        "txt2img_seed": 42,
        "txt2img_model": DEFAULT_MODEL,
        "txt2img_scheduler": DEFAULT_SCHEDULER,
        "txt2img_model_path": "",

        "img2img_prompt": "",
        "img2img_negative_prompt": "",
        "img2img_steps": 20,
        "img2img_ddim_eta": 0.0,  # only applies to ddim scheduler
        "img2img_n_iter": 1,
        "img2img_height": 512,
        "img2img_width": 512,
        "img2img_n_samples": 1,
        "img2img_strength": 0.8,
        "img2img_scale": 7.5,
        "img2img_seed": 42,
        "img2img_model": DEFAULT_MODEL,
        "img2img_scheduler": DEFAULT_SCHEDULER,
        "img2img_model_path": "",

        "inpaint_prompt": "",
        "inpaint_negative_prompt": "",
        "inpaint_steps": 20,
        "inpaint_ddim_eta": 0.0,
        "inpaint_n_iter": 1,
        "inpaint_height": 512,
        "inpaint_width": 512,
        "inpaint_n_samples": 1,
        "inpaint_scale": 7.5,
        "inpaint_from-file": False,
        "inpaint_seed": 42,
        "inpaint_model": DEFAULT_MODEL,
        "inpaint_scheduler": DEFAULT_SCHEDULER,
        "inpaint_model_path": "",

        "outpaint_prompt": "",
        "outpaint_negative_prompt": "",
        "outpaint_steps": 20,
        "outpaint_ddim_eta": 0.0,
        "outpaint_n_iter": 1,
        "outpaint_height": 512,
        "outpaint_width": 512,
        "outpaint_n_samples": 1,
        "outpaint_scale": 7.5,
        "outpaint_from-file": False,
        "outpaint_seed": 42,
        "outpaint_model": DEFAULT_MODEL,
        "outpaint_scheduler": DEFAULT_SCHEDULER,
        "outpaint_model_path": "",
    }

    def txt2img_button_release_callback(self, _element):
        """
        Callback for the txt2img button.
        :param _element: passed by the button but not used
        :return: None, sends request to stable diffusion
        """
        self.handle_button_press("txt2img")

    def img2img_release_callback(self, _element):
        """
        Callback for the img2img button.
        :param _element: passed by the button but not used
        :return: None, sends request to stable diffusion
        """
        self.handle_button_press("img2img")

    def inpaint_release_callback(self, _element):
        self.handle_button_press("inpaint")

    def outpaint_release_callback(self, _element):
        self.handle_button_press("outpaint")

    def __init__(self, interfaces = None):
        self.log_widget = PlainText(
            placeholder="log",
            config_name="log",
            max_height=50,
            disabled=True
        )
        submit_button = [HorizontalInterface(
            widgets=[self.submit_button]
        )] if self.submit_button else []
        super().__init__([] if not interfaces else interfaces)
