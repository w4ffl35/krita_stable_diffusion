from krita import *
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.interface.widgets.slider import Slider
from krita_stable_diffusion.interface.widgets.spin_box import SpinBox
from krita_stable_diffusion.interface.widgets.label import Label


class SliderSpinnerInterface(HorizontalInterface):
    def handle_slider(self, value):
        self.slider.widget.setValue(value)
        self.spinbox.widget.setValue(value)

    def slider_callback(self, value):
        self.spinbox.widget.setValue(value)
        if self.callback:
            self.callback(value)

    def __init__(self, **kwargs):
        super().__init__()
        self.callback = kwargs.get("callback", None)
        self.label_text = kwargs.get("label", "Label")
        self.label = Label(
            label=self.label_text,
            min_width=kwargs.get("label_min_width", None),
        ) if self.label_text else None
        self.spinbox = SpinBox(
            min=kwargs.get("min", 0),
            max=kwargs.get("max", 100),
            step=kwargs.get("step", 1),
            callback=lambda val: self.handle_slider(val),
            double=kwargs.get("double", False),
            min_width=kwargs.get("min_width", None),
            max_width=kwargs.get("max_width", None),
        )
        self.slider = Slider(
            min=kwargs.get("min", 0),
            max=kwargs.get("max", 100),
            config_name=kwargs.get("config_name", None),
            parent=self.spinbox,
            callback=self.slider_callback,
        )
        widgets = [
            self.slider,
            self.spinbox
        ]
        self.add_interfaces([
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[self.label]),
                HorizontalInterface(widgets=widgets)
            ])
        ])
