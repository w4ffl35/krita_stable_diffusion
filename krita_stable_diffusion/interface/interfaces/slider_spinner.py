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
        double = kwargs.get("double", False)
        if double:
            step = float(kwargs.get("step", 0.1))
            min = float(kwargs.get("min", 0.0))
            max = float(kwargs.get("max", 1.0))
            value = float(kwargs.get("value", 0.0))
        else:
            step = int(kwargs.get("step", 1))
            min = int(kwargs.get("min", 0))
            max = int(kwargs.get("max", 100))
            value = int(kwargs.get("value", 0))
        self.callback = kwargs.get("callback", None)
        self.label_text = kwargs.get("label", "Label")
        self.label = Label(
            label=self.label_text,
            min_width=kwargs.get("label_min_width", None),
        ) if self.label_text else None
        self.spinbox = SpinBox(
            config_name=kwargs.get("config_name", None),
            min=min,
            max=max,
            step=step,
            callback=lambda val: self.handle_slider(val),
            double=double,
            min_width=kwargs.get("min_width", None),
            max_width=kwargs.get("max_width", None),
        )
        self.slider = Slider(
            config_name=kwargs.get("config_name", None),
            min=min,
            max=max,
            step=step,
            parent=self.spinbox,
            callback=self.slider_callback,
        )
        self.slider.widget.setTickPosition(QSlider.TicksBelow)
        self.slider.widget.setTickInterval(step)
        self.slider.widget.setSingleStep(step)
        self.slider.widget.setPageStep(step)
        self.slider.widget.setOrientation(Qt.Horizontal)
        self.slider.widget.setTracking(True)
        self.slider.widget.setValue(self.spinbox.widget.value())
        self.add_interfaces([
            VerticalInterface(interfaces=[
                HorizontalInterface(widgets=[self.label]),
                HorizontalInterface(widgets=[
                    self.slider,
                    self.spinbox
                ])
            ])
        ])
