import os
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.interface.tabs.base import Base
from krita_stable_diffusion.interface.widgets.dropdown import DropDown
from krita_stable_diffusion.interface.widgets.label import Label
from krita_stable_diffusion.interface.widgets.button import Button


class PromptTab(Base):
    name = "PromptTab"
    display_name = "Prompts"
    photo_types = [
        "polaroid",
        "CCTV",
        "body cam",
        "professional",
        "abstract",
        "artistic"
    ]
    styles = [
        "abstract",
        "artistic",
        "realistic",
        "sketch",
        "cartoon",
        "comic",
        "watercolor",
        "oil",
        "acrylic",
        "pastel",
        "ink",
        "pencil",
        "marker",
        "crayon",
        "charcoal",
        "digital",
        "mixed media",
        "collage",
        "sculpture",
        "ceramic",
        "glass",
        "metal",
        "wood",
        "stone",
        "fabric",
        "paper",
        "leather",
        "plastic"
    ]

    def photo_callback(self, _element):
        self.handle_button_press(
            "txt2img",
            image_type="photo",
            style=self.photo_types[int(self.config.value("photo_type"))]
        )

    def style_callback(self, _element):
        self.handle_button_press(
            "txt2img",
            image_type="painting",
            style=self.styles[int(self.config.value("painting_type"))]
        )

    def __init__(self):
        super().__init__([
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[
                    Label(label="Photo type"),
                ]),
                HorizontalInterface(widgets=[
                    DropDown(
                        options=self.photo_types,
                        config_name="photo_type"
                    ),
                    Button(
                        label="PHOTO",
                        release_callback=self.photo_callback,
                        config_name="server_connected",
                    ),
                ]),
            ]),
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[
                    Label(label="Style"),
                ]),
                HorizontalInterface(widgets=[
                    DropDown(
                        options=self.styles,
                        config_name="style_type"
                    ),
                    Button(
                        label="PAINTING",
                        release_callback=self.style_callback,
                        config_name="server_connected",
                    ),
                ]),
            ]),
        ])