import json
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
from krita_stable_diffusion.settings import SAMPLERS


class Txt2ImgTab(Base):
    """
    Txt2ImgTab interface for the Krita Stable Diffusion plugin.
    :param name: The name of the tab
    :param interfaces: The interfaces to be added to the tab
    """

    name = "Txt2ImgTab"
    display_name = "Text to Image"
    default_setting_values = {
        "prompt": "A cat",
        "outdir": "/home/joe/.stablediffusion/txt2img",
        "skip_grid": True,
        "skip_save": False,
        "ddim_steps": 50,
        "plms": True,
        "laion400m": False,
        "fixed_code": True,
        "ddim_eta": 0.0,
        "n_iter": 1,
        "H": 512,
        "W": 512,
        "C": 4,
        "f": 8,
        "n_samples": 1,
        "n_rows": 0,
        "scale": 7.5,
        "from-file": False,
        # "config": "",
        # "ckpt": "",
        "seed": 42,
        "precision": "autocast",
    }

    def txt2img_button_release_callback(self, _element):
        data = {}
        for k,v in self.default_setting_values.items():
            if k == "seed":
                v = self.seed()
            else:
                v = self.config.value(k)
            data[k] = v
        self.send(data, "txt2img")


    def __init__(self):
        super().__init__([
            VerticalInterface(widgets=[
                Label(label="Prompt"),
                PlainText(placeholder="prompt", config_name="prompt"),
                Label(label="Seed"),
                LineEdit(placeholder="Random seed", config_name="seed"),
                Label(label="Out directory"),
                LineEdit(placeholder="Out directory", config_name="outdir"),
                Button(label="Generate Image", release_callback=self.txt2img_button_release_callback),
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
                    Label(label="Sample frequency"),
                    Label(label="Total samples"),
                    Label(label="Unconditional guidance scale"),
                ]),
                HorizontalInterface(widgets=[
                    SpinBox(min=1, max=250, config_name="n_iter", step=2),
                    SpinBox(min=1, max=250, config_name="n_samples", step=1),
                    SpinBox(min=1.0, max=50.0, config_name="scale", step=0.1, double=True),
                ]),
            ]),
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[
                    Label(label="Width"),
                    Label(label="Height"),
                ]),
                HorizontalInterface(widgets=[
                    SpinBox(min=256, max=512, config_name="W", step=8),
                    SpinBox(min=256, max=512, config_name="H", step=8)
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
        ])
