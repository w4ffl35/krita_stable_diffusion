import os
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.interface.tabs.base import Base
from krita_stable_diffusion.interface.widgets.label import Label
from krita_stable_diffusion.interface.widgets.line_edit import LineEdit
from krita_stable_diffusion.interface.widgets.spin_box import SpinBox


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
        "ddim_steps": 20,
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
        "init_img": os.path.join(SDDIR, "img2img/output.png"),
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
        # self.save_active_node_to_png(path, False)
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
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[
                    Label(label="Total samples")
                ]),
                HorizontalInterface(widgets=[
                    SpinBox(
                        min=1,
                        max=250,
                        config_name="n_samples",
                        step=1
                    )
                ]),
            ]),
            VerticalInterface(widgets=[
                Label(label="Out directory"),
                LineEdit(placeholder="Out directory", config_name="outdir"),
            ]),
        ])
