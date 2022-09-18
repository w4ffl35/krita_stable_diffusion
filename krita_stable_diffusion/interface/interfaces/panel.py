from krita import *
from krita_stable_diffusion.interface.tabs.configtab import ConfigTab
from krita_stable_diffusion.interface.tabs.txt2imgtab import Txt2ImgTab
from krita_stable_diffusion.interface.tabs.upscaletab import UpscaleTab


class KritaDockWidget(DockWidget):
    widget = None

    def update_config(self):
        pass

    def canvasChanged(self, canvas):
        pass

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stable Diffusion (v1.0.0)")
        self.create_interface()

        try:
            self.update_config()
        except:
            pass

        self.setWidget(self.widget)

    def create_interface(self):
        tabs = QTabWidget()
        tabs.addTab(*(Txt2ImgTab().tab()))
        # tabs.addTab(*(Img2ImgTab().tab()))
        tabs.addTab(*(UpscaleTab().tab()))
        tabs.addTab(*(ConfigTab().tab()))

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.widget = QWidget(self)
        self.widget.setLayout(layout)
