from krita import *
from krita_stable_diffusion.interface.tabs.base import Base
from krita_stable_diffusion.interface.widgets.checkbox import CheckBox
from krita_stable_diffusion.interface.widgets.button import Button
from krita_stable_diffusion.interface.widgets.line_edit import LineEdit
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.interface.widgets.progress_bar import ProgressBar
from krita_stable_diffusion.interface.widgets.label import Label
from  krita_stable_diffusion.settings import MODELS


class SettingsWindow(Base):
    """
    SettingsWindow interface for text to image generation.
    """
    name = "SettingsWindow"
    display_name = "Stable Diffusion Options"
    default_setting_values = {
        "model_path_v1": "",
        "model_path_v2": "",
    }
    current_setting_values = {
        "model_path_v1": "",
        "model_path_v2": "",
    }

    def model_path_update(self, name, val):
        self.current_setting_values[name] = valh
        if self.callback:
            self.callback(name, val)

    def download_model(self, model):
        pass

    def delete_model(self, model):
        pass

    def __init__(self, *args, **kwargs):
        self.callback = kwargs.get("callback", None)
        self.config = Application.krita_stable_diffusion_config
        path_line_edit_v1 = LineEdit(
            placeholder="path",
            config_name="model_path_v1",
            update_value=self.model_path_update
        )
        path_line_edit_v2 = LineEdit(
            placeholder="path",
            config_name="model_path_v2",
            update_value=self.model_path_update
        )
        path_line_edit_v1.widget.setText(self.config.value("model_path_v1", ""))
        path_line_edit_v2.widget.setText(self.config.value("model_path_v2", ""))

        super().__init__([
            # VerticalInterface(
            #     widgets=[
            #         Label(label=model),
            #     ],
            #     interfaces=[
            #       HorizontalInterface(widgets=[
            #           ProgressBar(
            #               label="Download",
            #               current_value=self.config.value(model, {
            #                   "progress": 0,
            #               })
            #           ),
            #           Button(label="Download", callback=lambda: self.download_model(model)),
            #           Button(label="Delete", callback=lambda: self.delete_model(model)),
            #       ])
            #     ]
            # ) for model in MODELS
            VerticalInterface(widgets=[
                Label(label="Extra models path (v2)"),
                path_line_edit_v2,
                Label(label="Extra models path (v1)"),
                path_line_edit_v1,
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
        Application.update_extra_models()
        self.close()