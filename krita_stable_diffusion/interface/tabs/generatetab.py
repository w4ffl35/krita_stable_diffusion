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

class Txt2ImgTab(Base):
    """
    Txt2ImgTab interface for the Krita Stable Diffusion plugin.
    :param name: The name of the tab
    :param interfaces: The interfaces to be added to the tab
    """
    HOME = os.path.expanduser("~")
    SDDIR = os.path.join(HOME, "stablediffusion")
    name = "Txt2ImgTab"
    display_name = "Text to Image"
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
        "init_img": os.path.join(SDDIR, "img2img/output.png"),
        "negative_prompt": ""
    }
    photo_types = [
        "polaroid",
        "CCTV",
        "body cam",
        "professional",
        "abstract",
        "artistic"
    ]
    painting_types = []

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

    def txt2img_photo_release_callback(self, _element):
        self.handle_button_press(
            "txt2img",
            image_type="photo",
            style=self.photo_types[int(self.config.value("photo_type"))]
        )

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
            label="text ➔ image",
            release_callback=self.txt2img_button_release_callback,
            config_name="server_connected",
        )
        img2img_button = Button(
            label="text + image ➔ image",
            release_callback=self.img2img_release_callback,
            config_name="server_connected",
        )
        photo_button = Button(
            label="PHOTO",
            release_callback=self.txt2img_photo_release_callback,
            config_name="server_connected",
        )
        super().__init__([
            VerticalInterface(widgets=[
                Label(
                    label="Prompt"
                ),
                PlainText(
                    placeholder="prompt", config_name="prompt"
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
                    Label(label="Photo type"),
                ]),
                HorizontalInterface(widgets=[
                    DropDown(
                        options=self.photo_types,
                        config_name="photo_type"
                    ),
                    photo_button,
                ]),
            ]),
            HorizontalInterface(widgets=[
                txt2img_button,
                img2img_button,
            ]),
            HorizontalInterface(widgets=[
                self.log_widget,
            ]),
        ])
