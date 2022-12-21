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
    do_random_seed = False

    def random_seed_callback(self, is_checked):
        self.do_random_seed = is_checked
        self.seed_line_edit.widget.setDisabled(self.do_random_seed)

    def generate_callback(self, element):
        if self.do_random_seed:
            seed = str(random.randint(MIN_SEED, MAX_SEED))
            self.seed_line_edit.widget.setText(seed)
        self.section_callback(element)

    def __init__(self, **kwargs):
        section = kwargs.get("section", "txt2img")
        self.section_callback = kwargs.get("section_callback", None)
        self.progress_bar = ProgressBar(label="Generating image")
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
                    SliderSpinnerInterface(
                        label="Steps",
                        min=1,
                        max=100,
                        step=1,
                        min_width=100,
                        config_name="f{section}_steps",
                    ),
                    SliderSpinnerInterface(
                        label="Scale",
                        min=1.0,
                        max=100.0,
                        step=float(0.1),
                        double=True,
                        min_width=100,
                        config_name=f"{section}_cfg_scale",
                    ),
                    HorizontalInterface(widgets=[
                        Button(
                            label="Generate",
                            release_callback=self.generate_callback,
                            config_name=f"{section}_server_connected",
                        ),
                        self.progress_bar,
                    ]),
                ])
            ]
        )