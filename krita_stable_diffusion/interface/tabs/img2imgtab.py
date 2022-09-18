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


class Img2ImgTab(Base):
    """
    Img2ImgTab interface for the Krita Stable Diffusion plugin.
    :param name: The name of the tab
    :param interfaces: The interfaces to be added to the tab
    """

    name = "Img2ImgTab"
    display_name = "Image to Image"
    default_setting_values = {
        "prompt": "A cat",
        "init_img": "/home/joe/.stablediffusion/img2img/output.png",
        "negative_prompt": "",
        "outdir": "/home/joe/.stablediffusion/img2img",
        "skip_grid": True,
        "skip_save": False,
        "ddim_steps": 50,
        "plms": False,
        "fixed_code": True,
        "ddim_eta": 0.0,
        "n_iter": 1,
        "C": 4,
        "f": 8,
        "n_samples": 1,
        "n_rows": 0,
        "scale": 5.0,
        "strength": 0.75,
        "sampler": "DDIM",
        "cfg_scale": 7.5,
        "seed": 42
    }

    def img2img_release_callback(self, _element):
        path = self.default_setting_values["init_img"]
        self.config.setValue("init_img", path)
        self.save_active_node_to_png(path, False)
        self.handle_button_press("img2img")

    def img2img_upscale_callback(self):
        pass

    def img2img_inpaint_callback(self):
        pass

    def __init__(self):
        super().__init__([
            VerticalInterface(widgets=[
                Label(label="Prompt"),
                PlainText(placeholder="prompt", config_name="img2img_prompt"),
                Label(label="Seed"),
                LineEdit(placeholder="Random seed", config_name="img2img_seed"),
                Button(label="Apply img2img", release_callback=self.img2img_release_callback),
                # Button(label="Apply img2img upscale", release_callback=self.img2img_upscale_callback),
                # Button(label="Apply img2img inpaint", release_callback=self.img2img_inpaint_callback()),
            ]),
            HorizontalInterface(widgets=[Label(label="Advanced settings")]),
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
                    Label(label="Prescaler for SD upscale"),
                ]),
                HorizontalInterface(widgets=[
                    DropDown(options=UPSCALERS, config_name="upscaler")
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
        ])