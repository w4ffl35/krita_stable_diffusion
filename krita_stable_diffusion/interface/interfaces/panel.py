from krita import *
from krita_stable_diffusion.interface.tabs.txt2imgtab import Txt2ImgTab
from krita_stable_diffusion.interface.tabs.img2imgtab import Img2ImgTab
from krita_stable_diffusion.interface.tabs.inpainttab import InpaintTab
from krita_stable_diffusion.interface.tabs.outpainttab import OutpaintTab
from krita_stable_diffusion.interface.tabs.converttab import ConvertTab
from krita_stable_diffusion.interface.tabs.upscaletab import UpscaleTab
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface


class KritaDockWidget(DockWidget):
    widget = None

    def update_config(self):
        pass

    def canvasChanged(self, canvas):
        pass

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Krita Stable Diffusion (v1.0.0)")
        self.create_interface()

        try:
            self.update_config()
        except:
            pass

        self.setWidget(self.widget)

    def create_interface(self):
        tabs = QTabWidget()
        outpaint = OutpaintTab()
        tabs.addTab(*(Txt2ImgTab().tab()))
        tabs.addTab(*(Img2ImgTab().tab()))
        tabs.addTab(*(InpaintTab().tab()))
        tabs.addTab(*(outpaint.tab()))
        tabs.addTab(*(ConvertTab().tab()))
        # tabs.addTab(*(UpscaleTab().tab()))

        # on click of tabs[3]
        tabs.tabBarClicked.connect(lambda i: outpaint.handle_tab_click(i))

        # create a line separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        horizontal_interface = HorizontalInterface(widgets=[
            Application.status_label,
            Application.connection_label
        ])
        layout.addLayout(horizontal_interface)
        layout.addWidget(line)
        self.widget = QWidget(self)
        self.widget.setLayout(layout)
