from krita import *
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.interface.tabs.base import Base
from krita_stable_diffusion.interface.widgets.button import Button
from krita_stable_diffusion.interface.widgets.progress_bar import ProgressBar
from krita_stable_diffusion.interface.interfaces.model_interface import ModelInterface


class ConvertTab(Base):
    """
    ConvertTab interface for the Krita Stable Diffusion plugin.
    """
    name = "ConvertTab"
    display_name = "Convert ckpt"
    config_name = "convert"
    default_setting_values = {
        "convert_model": "",
        "convert_model_version": "",
        "convert_data_type": "",
        "convert_model_output_type": "",
    }

    def handle_button_press(self, request_type, **kwargs):
        """
        Callback for the convert button.
        :return: None, sends request to stable diffusion
        """
        data = {}
        for k, v in self.default_setting_values.items():
            v = self.config.value(k, v)
            data[k] = v
        self.update_progressbar(request_type, 0, 0)

        # add config options to request data
        data = self.prep_config_options(data)

        data["model_base_path"] = self.config.value("model_base_path", "")

        # send request to the server
        self.send(data, request_type)

    def convert_release_callback(self, _element):
        """
        Callback for the convert button.
        :param _element: passed by the button but not used
        :return: None, sends request to stable diffusion
        """
        self.handle_button_press("convert")


    def __init__(self):
        super().__init__([
            VerticalInterface(interfaces=[
                ModelInterface(
                    section=self.config_name,
                    dropdown=None,
                    show_scheduler=False,
                    show_data_type=True,
                    show_model_output_type=True
                ),
                HorizontalInterface(
                    widgets=[
                        Button(
                            label="Convert",
                            section="Convert",
                            release_callback=self.convert_release_callback
                        ),
                        ProgressBar(label="Convert")
                    ]
                )
            ])
        ])

