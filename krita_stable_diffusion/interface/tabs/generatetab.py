import os
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.interface.tabs.base import Base
from krita_stable_diffusion.interface.widgets.button import Button
from krita_stable_diffusion.interface.widgets.dropdown import DropDown
from krita_stable_diffusion.interface.widgets.label import Label
from krita_stable_diffusion.interface.widgets.line_edit import LineEdit
from krita_stable_diffusion.interface.widgets.plain_text import PlainText
from krita_stable_diffusion.interface.widgets.spin_box import SpinBox
from krita_stable_diffusion.interface.widgets.progress_bar import ProgressBar
from krita_stable_diffusion.settings import SAMPLERS


class Txt2ImgTab(Base):
    """
    Txt2ImgTab interface for the Krita Stable Diffusion plugin.
    :param name: The name of the tab
    :param interfaces: The interfaces to be added to the tab
    """
    HOME = os.path.expanduser("~")
    SDDIR = os.path.join(HOME, "stablediffusion")
    name = "Txt2ImgTab"
    display_name = "Generate images"
    default_setting_values = {
        "prompt": "A cat",
        "outdir": os.path.join(SDDIR, "txt2img"),
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
        "seed": 42,
        "precision": "autocast",
        "negative_prompt": "",
        "model": 0,
        "model_path": "",
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

    def txt2img_painting_release_callback(self, _element):
        self.handle_button_press(
            "txt2img",
            image_type="painting",
            style=self.painting_types[self.config.value("painting_type")]
        )

    def __init__(self):
        self.log_widget = PlainText(
            placeholder="log",
            config_name="log",
            max_height=50,
            disabled=True
        )
        txt2img_button = Button(
            label="Generate txt2img",
            release_callback=self.txt2img_button_release_callback,
            config_name="server_connected",
        )
        img2img_button = Button(
            label="Generate img2img",
            release_callback=self.img2img_release_callback,
            config_name="server_connected",
        )
        inpaint_button = Button(
            label="Generate inpaint",
            release_callback=self.inpaint_release_callback,
            config_name="server_connected",
        )
        progress_bar = ProgressBar(
            label="Generating image"
        )
        self.progress_bar = progress_bar
        # add progress_bar to the main Controller
        Application.__setattr__("progress_bar", progress_bar)
        Application.__setattr__("connection_label", Label(
            label=f"Not connected to localhost:5000",
            alignment="right",
        ))
        super().__init__([
            VerticalInterface(widgets=[
                Application.connection_label,
                Label(label="Model"),
                DropDown(
                    options=self.available_models,
                    config_name="model"
                ),
                Label(label="Prompt"),
                PlainText(
                    placeholder="prompt", config_name="prompt"
                ),
                Label(label="Negative Prompt"),
                PlainText(
                    placeholder="negative_prompt", config_name="negative_prompt"
                ),
            ]),
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[
                    Label(
                        label="Number of images",
                        max_width=150
                    ),
                    Label(
                        label="Seed"
                    ),
                ]),
                HorizontalInterface(widgets=[
                    SpinBox(
                        min=1,
                        max=250,
                        config_name="n_iter",
                        step=2,
                        min_width=150
                    ),
                    LineEdit(
                        placeholder="Random seed",
                        config_name="seed"
                    ),
                ]),
            ]),
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[
                    Label(label="Sampler")
                ]),
                HorizontalInterface(widgets=[
                    DropDown(options=SAMPLERS, config_name="sampler")
                ]),
            ]),
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[
                    Label(label="Strength"),
                    Label(label="Steps"),
                    Label(label="Scale"),
                ]),
                HorizontalInterface(widgets=[
                    SpinBox(
                        min=0,
                        max=1,
                        config_name="strength",
                        step=0.1,
                        double=True
                    ),
                    SpinBox(
                        min=1,
                        max=250,
                        config_name="ddim_steps",
                        step=1
                    ),
                    SpinBox(
                        min=1.0,
                        max=30.0,
                        config_name="cfg_scale",
                        step=0.5, double=True
                    )
                ]),
            ]),
            VerticalInterface(widgets=[
                txt2img_button,
                img2img_button,
                inpaint_button
            ]),
            HorizontalInterface(widgets=[
                progress_bar,
            ]),
            HorizontalInterface(widgets=[
                self.log_widget,
            ]),
        ])
