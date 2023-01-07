import random
from krita import *
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.interface.interfaces.slider_spinner import SliderSpinnerInterface
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.interface.widgets.line_edit import LineEdit
from krita_stable_diffusion.interface.widgets.progress_bar import ProgressBar
from krita_stable_diffusion.interface.widgets.spin_box import SpinBox
from krita_stable_diffusion.interface.widgets.checkbox import CheckBox
from krita_stable_diffusion.interface.widgets.button import Button
from krita_stable_diffusion.interface.widgets.label import Label
from krita_stable_diffusion.settings import MAX_SEED, MIN_SEED


class GenerateSettingsInterface(VerticalInterface):
    seed_line_edit = None
    section = None
    do_random_seed = False

    def random_seed_callback(self, is_checked):
        self.do_random_seed = is_checked
        self.seed_line_edit.widget.setDisabled(self.do_random_seed)

    def generate_callback(self, element):
        if self.do_random_seed:
            seed = str(random.randint(MIN_SEED, MAX_SEED))
            self.seed_line_edit.widget.setText(seed)
        self.section_callback(element)

    def convert_model_callback(self, element):
        config = Application.krita_stable_diffusion_config
        model = config.value(f"{self.section}_model")
        # check if model ends with ckpt
        if model.endswith(".ckpt"):
            Application.convert_model_to_diffusers()

    def __init__(self, **kwargs):
        strength_interface = None
        section = kwargs.get("section", "txt2img")
        self.section = section
        self.section_callback = kwargs.get("section_callback", None)
        self.progress_bar = ProgressBar(label="Converting ckpt file")
        self.convert_callback = kwargs.get("convert_callback", None)
        Application.__setattr__(
            f"{section}_progress_bar",
            self.progress_bar
        )
        self.seed_line_edit = LineEdit(
            placeholder="Random seed",
            config_name=f"{section}_seed",
            max=MAX_SEED,
            max_width=100
        )
        if section in ["img2img", "depth2img"]:
            strength_interface = SliderSpinnerInterface(
                label="Strength",
                config_name=f"{section}_strength",
                min=0,
                max=1.0,
                slider_max=10000,
                step=0.01,
                default=0.5,
                max_width=100,
                double=True
            )
        super().__init__(
            widgets=[],
            interfaces=[
                HorizontalInterface(widgets=[
                    Label(
                        label="Seed",
                        max_width=100
                    ),
                    Label(
                        label="Samples"
                    ),
                ]),
                HorizontalInterface(widgets=[
                    self.seed_line_edit,
                    SpinBox(
                        min=1,
                        max=999,
                        config_name=f"{section}_n_samples",
                        step=1
                    ),
                ]),
                HorizontalInterface(widgets=[
                    # add blank space to align with other columns
                    CheckBox(
                        label="Random seed",
                        config_name=f"{section}_randomseed",
                        callback=self.random_seed_callback,
                        checked=True
                    )
                ]),
                VerticalInterface(interfaces=[
                    HorizontalInterface(widgets=[
                        Label(
                            label="Width"
                        ),
                        Label(
                            label="Height"
                        ),
                    ]),
                    HorizontalInterface(widgets=[
                        SpinBox(
                            min=512,
                            max=1088,
                            config_name=f"{section}_width",
                            step=256,
                        ),
                        SpinBox(
                            min=512,
                            max=1088,
                            config_name=f"{section}_height",
                            step=256,
                        ),
                    ]),
                    strength_interface,
                    SliderSpinnerInterface(
                        label="Steps",
                        min=1,
                        max=255,
                        step=1,
                        min_width=100,
                        config_name=f"{section}_steps",
                    ),
                    SliderSpinnerInterface(
                        label="Scale",
                        min=1.0,
                        max=100.0,
                        slider_max=10000,
                        step=float(0.1),
                        double=True,
                        min_width=100,
                        config_name=f"{section}_scale",
                    ),
                    HorizontalInterface(widgets=[
                        Button(
                            label="Generate",
                            release_callback=self.generate_callback,
                            config_name=f"{section}_server_connected",
                        ),
                        self.progress_bar,
                        Button(
                            label="ckpt to diffusers",
                            release_callback=self.convert_callback
                        ),
                    ]),
                ])
            ]
        )