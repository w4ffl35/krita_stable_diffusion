from krita import *
from krita_stable_diffusion.interface.tabs.base import Base
from krita_stable_diffusion.interface.widgets.checkbox import CheckBox
from krita_stable_diffusion.interface.widgets.button import Button
from krita_stable_diffusion.interface.widgets.line_edit import LineEdit
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.interface.widgets.label import Label


class SettingsWindow(Base):
    """
    SettingsWindow interface for text to image generation.
    """
    name = "SettingsWindow"
    display_name = "Stable Diffusion Options"
    default_setting_values = {
        "model_path": "",
    }
    current_setting_values = {
        "model_path": "",
    }

    def model_path_update(self, name, val):
        self.current_setting_values[name] = val

    def __init__(self):
        self.config = Application.krita_stable_diffusion_config
        path_line_edit = LineEdit(
            placeholder="Extra models path",
            config_name="model_path",
            update_value=self.model_path_update
        )
        print(self.config.value("model_path", ""))
        #path_line_edit.widget.setText(self.config.value("model_path", ""))
        super().__init__([
            VerticalInterface(widgets=[
                # drop down for selecting the model
                Label(label="Extra models path"),
                path_line_edit,
            ])
        ])

        self.newDialog = QDialog()

        # set min width and height for newDialog
        self.newDialog.setMinimumWidth(400)
        self.newDialog.setMinimumHeight(400)

        layoutForButtons = QHBoxLayout()
        saveButton = QPushButton("Save")
        cancelButton = QPushButton("Cancel")
        layoutForButtons.addWidget(saveButton)
        layoutForButtons.addWidget(cancelButton)

        saveButton.clicked.connect(self.save)
        cancelButton.clicked.connect(self.cancel)

        self.layout.addLayout(layoutForButtons)

        # create dialog  and show it
        self.newDialog.setLayout(self.layout)
        self.newDialog.setWindowTitle(self.display_name)
        self.newDialog.exec_()  # show the dialog

        # store current setting values
        for k in self.default_setting_values.keys():
            self.current_setting_values[k] = self.config.value(k, self.default_setting_values[k])

    def cancel(self):
        for k in self.default_setting_values.keys():
            self.default_setting_values[k] = self.current_setting_values[k]
        self.close()

    def close(self):
        self.newDialog.close()

    def save(self):
        for k in self.default_setting_values.keys():
            self.config.setValue(k, self.current_setting_values[k])
        self.config.sync()
        self.close()

class StableDiffusionMenu(Base):
    name = "SettingsMenu"
    display_name = "Stable Diffusion"
    default_setting_values = {
        "do_nsfw_filter": False,
        "do_watermark": False,
        "enable_community_models": False
    }

    def options_clicked(self):
        print("settings clicked")
        settings_window = SettingsWindow()

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
        self.add_checkmark_setting(main_menu, custom_menu, "Add Watermark", "do_watermark")
        self.add_checkmark_setting(main_menu, custom_menu, "Enable community models", "enable_community_models")

        custom_menu.addAction("Options")
        custom_menu.actions()[3].triggered.connect(lambda: self.options_clicked())


    def __init__(self):
        super().__init__([])
        self.load_menu()
