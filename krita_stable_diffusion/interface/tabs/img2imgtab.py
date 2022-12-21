import random
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.interface.interfaces.slider_spinner import SliderSpinnerInterface
from krita_stable_diffusion.interface.tabs.generatetab import GenerateTab
from krita_stable_diffusion.interface.widgets.progress_bar import ProgressBar
from krita_stable_diffusion.interface.widgets.line_edit import LineEdit
from krita_stable_diffusion.interface.widgets.spin_box import SpinBox
from krita_stable_diffusion.interface.widgets.button import Button
from krita_stable_diffusion.interface.widgets.dropdown import DropDown
from krita_stable_diffusion.interface.widgets.plain_text import PlainText
from krita_stable_diffusion.interface.widgets.label import Label
from krita_stable_diffusion.interface.widgets.checkbox import CheckBox
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.settings import SCHEDULERS, MAX_SEED, MIN_SEED


class Img2ImgTab(GenerateTab):
    """
    Img2ImgTab interface for text to image generation.
    """
    name = "Img2ImgTab"
    display_name = "img2img"
    do_random_seed = False

    def random_seed_callback(self, is_checked):
        self.do_random_seed = is_checked
        self.seed_line_edit.widget.setDisabled(self.do_random_seed)

    def generate_callback(self, element):
        if self.do_random_seed:
            seed = str(random.randint(MIN_SEED, MAX_SEED))
            self.seed_line_edit.widget.setText(seed)
        self.img2img_release_callback(element)

    def __init__(self):
        self.seed_line_edit = LineEdit(
            placeholder="Random Seed",
            config_name="img2img_seed",
            max=MAX_SEED,
            max_width=100,
        )
        self.progress_bar = ProgressBar(
            label="Generating image"
        )
        Application.__setattr__("img2img_progress_bar", self.progress_bar)
        super().__init__([
            HorizontalInterface(interfaces=[
                VerticalInterface(interfaces=[
                    HorizontalInterface(widgets=[
                        Label(label="Scheduler")
                    ]),
                    HorizontalInterface(widgets=[
                        DropDown(
                            options=SCHEDULERS,
                            config_name="img2img_scheduler"
                        )
                    ]),
                ]),
                VerticalInterface(widgets=[
                    Label(label="Version"),
                    DropDown(
                        options=[
                            "v1",
                            "v2",
                        ],
                        config_name="img2img_model_version",
                        max_width=100
                    )
                ]),
                VerticalInterface(widgets=[
                    Label(label="Model"),
                    Application.img2img_available_models_dropdown,
                ])
            ]),
            VerticalInterface(widgets=[
                Label(label="Prompt"),
                PlainText(
                    placeholder="prompt",
                    config_name="img2img_prompt"
                ),
                Label(label="Negative Prompt"),
                PlainText(
                    placeholder="negative_prompt",
                    config_name="img2img_negative_prompt"
                ),
            ]),
            VerticalInterface(interfaces=[
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
                        config_name="img2img_n_samples",
                        step=1,
                    ),
                ]),
                HorizontalInterface(widgets=[
                    # add blank space to align with other columns
                    CheckBox(
                        label="Random seed",
                        config_name="img2img_randomseed",
                        callback=self.random_seed_callback,
                        checked=True
                    )
                ]),
            ]),
            VerticalInterface(interfaces=[
                SliderSpinnerInterface(
                    label="Strength",
                    min=0.0,
                    max=100.0,
                    step=0.01,
                    double=True,
                    min_width=100,
                    config_name="img2img_strength",
                ),
                SliderSpinnerInterface(
                    label="Steps",
                    min=1,
                    max=250,
                    step=1,
                    min_width=100,
                    config_name="img2img_steps",
                ),
                SliderSpinnerInterface(
                    label="Scale",
                    min=1.0,
                    max=100.0,
                    step=0.01,
                    double=True,
                    min_width=100,
                    config_name="img2img_cfg_scale",
                ),
                HorizontalInterface(widgets=[
                    Button(
                        label="Generate",
                        release_callback=self.generate_callback,
                        config_name="server_connected",
                    ),
                    self.progress_bar,
                ]),
            ]),
        ])