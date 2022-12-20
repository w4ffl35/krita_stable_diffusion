import os
import random
from krita import *
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
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
from krita_stable_diffusion.settings import SCHEDULERS
from krita_stable_diffusion.settings import MIN_SEED, MAX_SEED


class Txt2ImgTab(GenerateTab):
    """
    Txt2ImgTab interface for text to image generation.
    """
    name = "Txt2ImgTab"
    display_name = "txt2img"
    do_random_seed = False

    def random_seed_callback(self, is_checked):
        self.do_random_seed = is_checked
        self.seed_line_edit.widget.setDisabled(self.do_random_seed)

    def generate_callback(self, element):
        if self.do_random_seed:
            seed = str(random.randint(MIN_SEED, MAX_SEED))
            self.seed_line_edit.widget.setText(seed)
        self.txt2img_button_release_callback(element)

    def __init__(self):
        self.seed_line_edit = LineEdit(
            placeholder="Random seed",
            config_name="txt2img_seed",
            max=MAX_SEED,
            max_width=100
        )
        self.progress_bar = ProgressBar(
            label="Generating image"
        )
        Application.__setattr__(
            "txt2img_progress_bar",
            self.progress_bar
        )
        config = Application.krita_stable_diffusion_config
        # find all ckpt files in config.model_path
        self.extra_models = []
        # check recursively for ckpt files
        model_path = config.value("model_path", None)
        if model_path:
            for root, dirs, files in os.walk(model_path):
                for file in files:
                    if file.endswith(".ckpt"):
                        self.extra_models.append(
                            os.path.join
                            (root, file)
                        )

        super().__init__([
            VerticalInterface(widgets=[
                Label(label="Model"),
                DropDown(
                    options=self.available_models + self.extra_models,
                    config_name="txt2img_model"
                ),
                Label(label="Prompt"),
                PlainText(
                    placeholder="prompt",
                    config_name="txt2img_prompt"
                ),
                Label(label="Negative Prompt"),
                PlainText(
                    placeholder="negative_prompt",
                    config_name="txt2img_negative_prompt"
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
                        config_name="txt2img_n_samples",
                        step=2
                    ),
                ]),
                HorizontalInterface(widgets=[
                    # add blank space to align with other columns
                    CheckBox(
                        label="Random seed",
                        config_name="txt2img_randomseed",
                        callback=self.random_seed_callback,
                        checked=True
                    )
                ]),
            ]),
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[
                    Label(label="Scheduler")
                ]),
                HorizontalInterface(widgets=[
                    DropDown(
                        options=SCHEDULERS,
                        config_name="txt2img_scheduler"
                    )
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
                        config_name="txt2img_strength",
                        step=0.1,
                        double=True
                    ),
                    SpinBox(
                        min=1,
                        max=250,
                        config_name="txt2img_ddim_steps",
                        step=1
                    ),
                    SpinBox(
                        min=1.0,
                        max=30.0,
                        config_name="txt2img_cfg_scale",
                        step=0.5,
                        double=True
                    ),
                ]),
                HorizontalInterface(widgets=[
                    Button(
                        label="Generate",
                        release_callback=self.generate_callback,
                        config_name="txt2img_server_connected",
                    ),
                    self.progress_bar,
                ]),
            ]),
        ])