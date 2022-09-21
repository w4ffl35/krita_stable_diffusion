import os
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.interface.tabs.base import Base
from krita_stable_diffusion.interface.widgets.button import Button
from krita_stable_diffusion.interface.widgets.checkbox import CheckBox
from krita_stable_diffusion.interface.widgets.dropdown import DropDown
from krita_stable_diffusion.interface.widgets.label import Label
from krita_stable_diffusion.interface.widgets.line_edit import LineEdit
from krita_stable_diffusion.interface.widgets.plain_text import PlainText
from krita_stable_diffusion.interface.widgets.spin_box import SpinBox
from krita_stable_diffusion.settings import UPSCALERS, SAMPLERS

class AdvancedTab(Base):
    """
    Txt2ImgTab interface for the Krita Stable Diffusion plugin.
    :param name: The name of the tab
    :param interfaces: The interfaces to be added to the tab
    """
    HOME = os.path.expanduser("~")
    SDDIR = os.path.join(HOME, "stablediffusion")
    name = "Advanced"
    display_name = "Advanced settings"
    default_setting_values = {
        "outdir": os.path.join(SDDIR, "txt2img"),
        "skip_grid": True,
        "skip_save": False,
        "ddim_steps": 50,
        "plms": True,
        "laion400m": False,
        "fixed_code": True,
        "ddim_eta": 0.0,
        "C": 4,
        "f": 8,
        "n_samples": 1,
        "n_rows": 0,
        "scale": 7.5,
        "from-file": False,
        "precision": "autocast",
        "init_img":  os.path.join(SDDIR, "img2img/output.png"),
        "negative_prompt": "",
        "cfg_scale": 7.5,
    }

    def img2img_release_callback(self, _element):
        """
        Callback for the img2img button.
        :param _element: passed by the button but not used
        :return: None, sends request to stable diffusion
        """
        path = self.default_setting_values["init_img"]
        self.config.setValue("init_img", path)
        self.save_active_node_to_png(path, False)
        self.handle_button_press("img2img")

    def txt2img_button_release_callback(self, _element):
        """
        Callback for the txt2img button.
        :param _element: passed by the button but not used
        :return: None, sends request to stable diffusion
        """
        self.handle_button_press("txt2img")


    def __init__(self):
        super().__init__([
            HorizontalInterface(widgets=[Label(label="img2img settings")]),
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[
                    Label(label="Prescaler for SD upscale"),
                ]),
                HorizontalInterface(widgets=[
                    DropDown(options=UPSCALERS, config_name="upscaler")
                ]),
            ]),
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[
                    Label(label="Denoising Strength"),
                ]),
                HorizontalInterface(widgets=[
                    SpinBox(min=0, max=1, config_name="strength", step=0.1, double=True),
                    # CheckBox(label="Enable GFPGAN", config_name="gfpgan", default_value=self.default_setting_values["gfpgan"]),
                ]),
            ]),
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[
                    Label(label="Steps"),
                    Label(label="Cfg Scale"),
                ]),
                HorizontalInterface(widgets=[
                    SpinBox(min=1, max=250, config_name="ddim_steps", step=1),
                    SpinBox(min=1.0, max=30.0, config_name="cfg_scale", step=0.5, double=True)
                ]),
            ]),
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[
                    Label(label="Batch count"),
                    Label(label="Batch size"),
                ]),
                HorizontalInterface(widgets=[
                    SpinBox(min=1, max=250, config_name="batch_count", step=1),
                    SpinBox(min=1, max=8, config_name="batch_size", step=1)
                ]),
            ]),
            VerticalInterface(widgets=[
                Label(label="Sampler"),
                DropDown(options=SAMPLERS, config_name="sampler")
            ]),
            HorizontalInterface(widgets=[Label(label="Advanced settings")]),
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[
                    CheckBox(label="Fixed code", config_name="fixed_code"),
                    CheckBox(label="Use laion400m", config_name="laion400m"),
                ]),
                HorizontalInterface(widgets=[
                    CheckBox(label="use PLMS", config_name="plms"),
                    CheckBox(label="Skip grid", config_name="skip_grid"),
                ]),
            ]),
            VerticalInterface(interfaces=[
                VerticalInterface(widgets=[
                    Label(label="Grid rows"),
                    SpinBox(min=1, max=3, config_name="n_rows", step=1),
                ]),
            ]),
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[
                    Label(label="Latent Channels"),
                    Label(label="Downsampling factor"),
                ]),
                HorizontalInterface(widgets=[
                    SpinBox(min=1, max=12, config_name="C", step=1),
                    SpinBox(min=1, max=12, config_name="f", step=1)
                ]),
            ]),
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[
                    Label(label="Sampler"),
                    Label(label="Precision"),
                ]),
                HorizontalInterface(widgets=[
                    DropDown(options=SAMPLERS, config_name="sampler"),
                    DropDown(options=["full", "autocast"], config_name="sampler"),
                ]),
            ]),
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[
                    Label(label="Total samples"),
                    Label(label="Unconditional guidance scale"),
                ]),
                HorizontalInterface(widgets=[
                    SpinBox(min=1, max=250, config_name="n_samples", step=1),
                    SpinBox(min=1.0, max=50.0, config_name="scale", step=0.1, double=True),
                ]),
            ]),
            VerticalInterface(widgets=[
                Label(label="Out directory"),
                LineEdit(placeholder="Out directory", config_name="outdir"),
            ]),
        ])
