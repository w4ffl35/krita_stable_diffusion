from krita import *
from krita_stable_diffusion.interface.interfaces.layout_base import LayoutBase
from krita_stable_diffusion.interface.interfaces.slider_spinner import SliderSpinnerInterface
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface


class BoxSliderInterface(LayoutBase):
    def __init__(self, **kwargs):
        max_width = kwargs.get("max_width", None)
        max_height = kwargs.get("max_height", None)
        callback = kwargs.get("callback", None)
        super().__init__(
            interfaces=[
                VerticalInterface(interfaces=[
                    SliderSpinnerInterface(
                        label="Pos X",
                        min=0,
                        max=max_width,
                        slider_max=max_width,
                        config_name="outpaint_layer_x",
                        min_width=100,
                        callback=callback
                    ),
                    SliderSpinnerInterface(
                        label="Pos Y",
                        min=0,
                        max=max_height,
                        slider_max=max_height,
                        config_name="outpaint_layer_y",
                        min_width=100,
                        callback=callback
                    ),
                ])
            ]
        )
