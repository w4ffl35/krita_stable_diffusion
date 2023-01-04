from krita import *
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.interface.tabs.base import Base
from krita_stable_diffusion.interface.widgets.button import Button
from krita_stable_diffusion.interface.widgets.progress_bar import ProgressBar


checkpoint = {
    "name": "",
    "downloaded": False,
    "url": "",
}


class CheckpointDBTab(Base):
    """
    CheckpointDBTab interface for the Krita Stable Diffusion plugin.
    Displays a list of checkpoint files which can be downloaded from a server.
    """

    available_checkpoints = {}

    def convert_release_callback(self, _element):
        """
        Callback for the convert button.
        :param _element: passed by the button but not used
        :return: None, sends request to stable diffusion
        """
        self.handle_button_press("convert")

    def __init__(self):
        self.progress_bar = ProgressBar(label="Convert")
        super().__init__([
            HorizontalInterface(widgets=[
                Button(
                    section="Convert",
                    convert_callback=self.convert_release_callback
                ),
                self.progress_bar
            ])
        ])
