import random
from krita import *
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


class OutpaintTab(GenerateTab):
    """
    OutpaintTab interface for text to image generation.
    """
    name = "OutpaintTab"
    display_name = "outpainting"
    do_random_seed = False
    outpaint_node = None

    def move_node(self, _val):
        if self.outpaint_node:
            x = int(self.config.value("outpaint_layer_x", 0))
            y = int(self.config.value("outpaint_layer_y", 0))
            self.outpaint_node.move(x, y)

    def move_node_to(self, x, y):
        if self.outpaint_node:
            self.outpaint_node.move(x, y)

    def create_outpaint_layer(self):
        d = Krita.instance().activeDocument()
        prev_layer = d.activeNode()

        # get layer named "outpaint" if it exists
        layer = d.nodeByName("outpaint")
        if layer is None:
            i = InfoObject()
            i.setProperty("color", "red")
            s = Selection()
            s.select(0, 0, self.max_width, self.max_height, 255)
            n = d.createFillLayer("outpaint", "color", i, s)
            r = d.rootNode()
            c = r.childNodes()
            r.addChildNode(n, c[len(c) - 1])
            n.setOpacity(25)

            # move the layer to the right
            n.setLocked(True)

            d.refreshProjection()

            self.outpaint_node = n

            x = int(self.config.value("outpaint_layer_x", 0))
            y = int(self.config.value("outpaint_layer_y", 0))
            self.move_node_to(x, y)

            if prev_layer:
                d.setActiveNode(prev_layer)

    def random_seed_callback(self, is_checked):
        self.do_random_seed = is_checked
        self.seed_line_edit.widget.setDisabled(self.do_random_seed)

    def generate_callback(self, element):
        if self.do_random_seed:
            seed = str(random.randint(MIN_SEED, MAX_SEED))
            self.seed_line_edit.widget.setText(seed)
        self.outpaint_release_callback(element)

    def handle_tab_click(self, tab_index):
        if tab_index == 3:
            d = Krita.instance().activeDocument()
            if d:
                self.max_width = d.width() / 2
                self.max_height = d.height() / 2
                self.create_outpaint_layer()
        elif self.outpaint_node:
            # delete outpaint_node
            self.outpaint_node.remove()

    def __init__(self):
        self.max_width = 512
        self.max_height = 512
        self.seed_line_edit = LineEdit(
            placeholder="Random seed",
            config_name="outpaint_seed",
            max=MAX_SEED,
            max_width=100,
        )
        self.progress_bar = ProgressBar(
            label="Generating image"
        )
        Application.__setattr__(
            "outpaint_progress_bar",
            self.progress_bar
        )

        super().__init__([
            HorizontalInterface(interfaces=[
                VerticalInterface(interfaces=[
                    HorizontalInterface(widgets=[
                        Label(label="Scheduler")
                    ]),
                    HorizontalInterface(widgets=[
                        DropDown(
                            options=SCHEDULERS,
                            config_name="outpaint_scheduler"
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
                        config_name="outpaint2img_model_version",
                        max_width=100
                    )
                ]),
                VerticalInterface(widgets=[
                    Label(label="Model"),
                    Application.outpaint_available_models_dropdown,
                ])
            ]),
            VerticalInterface(interfaces=[
                SliderSpinnerInterface(
                    label="Pos X",
                    min=0,
                    max=self.max_width,
                    config_name="outpaint_layer_x",
                    min_width=100,
                    callback=self.move_node
                ),
                SliderSpinnerInterface(
                    label="Pos Y",
                    min=0,
                    max=self.max_width,
                    config_name="outpaint_layer_y",
                    min_width=100,
                    callback=self.move_node
                ),
            ]),
            VerticalInterface(widgets=[
                Label(label="Prompt"),
                PlainText(
                    placeholder="prompt",
                    config_name="outpaint_prompt"
                ),
                Label(label="Negative Prompt"),
                PlainText(
                    placeholder="negative_prompt",
                    config_name="outpaint_negative_prompt"
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
                        config_name="outpaint_n_samples",
                        step=1
                    ),
                ]),
                HorizontalInterface(widgets=[
                    # add blank space to align with other columns
                    CheckBox(
                        label="Random seed",
                        config_name="outpaint_randomseed",
                        callback=self.random_seed_callback,
                        checked=True
                    )
                ]),
            ]),
            VerticalInterface(interfaces=[
                SliderSpinnerInterface(
                    label="Steps",
                    min=1,
                    max=250,
                    step=1,
                    min_width=100,
                    config_name="outpaint_steps",
                ),
                SliderSpinnerInterface(
                    label="Scale",
                    min=1.0,
                    max=100.0,
                    step=0.01,
                    double=True,
                    min_width=100,
                    config_name="outpaint_cfg_scale",
                ),
                # HorizontalInterface(widgets=[
                #     Slider(
                #         label="Pos X",
                #         min=0,
                #         max=self.max_width,
                #         config_name="outpaint_layer_x",
                #         min_width=100,
                #         callback=self.move_node
                #     )
                # ]),
                # HorizontalInterface(widgets=[
                #     Slider(
                #         label="Pos Y",
                #         min=0,
                #         max=self.max_width,
                #         config_name="outpaint_layer_y",
                #         min_width=100,
                #         callback=self.move_node
                #     )
                # ]),
                HorizontalInterface(widgets=[
                    Button(
                        label="Generate",
                        release_callback=self.generate_callback,
                        config_name="outpaint_server_connected",
                    ),
                    self.progress_bar,
                ]),
            ]),
        ])