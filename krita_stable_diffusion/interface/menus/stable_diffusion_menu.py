from krita import *
from krita_stable_diffusion.interface.tabs.base import Base
from krita_stable_diffusion.interface.windows.settings_window import SettingsWindow


class StableDiffusionMenu(Base):
    name = "SettingsMenu"
    display_name = "Stable Diffusion"
    default_setting_values = {
        "do_nsfw_filter": False,
        "enable_community_models": False
    }

    def model_path_update(self, name, val):
        Application.update_extra_models()

    def options_clicked(self):
        settings_window = SettingsWindow(callback=self.model_path_update)

    def add_checkmark_setting(self, main_menu, custom_menu, label, setting):
        custom_menu.addAction(label)
        # get totoal item sin main_menu
        total_items = len(custom_menu.actions())
        item_index = total_items - 1
        custom_menu.actions()[item_index].setCheckable(True)
        if self.config.value(
            setting, type=bool
        ):
            custom_menu.actions()[item_index].toggle()
        custom_menu.actions()[item_index].triggered.connect(lambda: self.toggle_setting(setting))

    def toggle_setting(self, setting):
        self.config.setValue(setting, not self.config.value(setting, type=bool))
        self.config.sync()

    def load_menu(self):
        main_menu = Krita.instance().activeWindow().qwindow().menuBar()
        custom_menu = main_menu.addMenu(self.display_name)

        self.add_checkmark_setting(main_menu, custom_menu, "NSFW Filter", "do_nsfw_filter")
        self.add_checkmark_setting(main_menu, custom_menu, "Enable community models", "enable_community_models")

        custom_menu.addAction("Options")
        custom_menu.actions()[-1].triggered.connect(self.options_clicked)


    def __init__(self):
        super().__init__([])
        self.load_menu()
