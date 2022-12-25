from krita import *
from krita_stable_diffusion.interface.interfaces.vertical_interface import VerticalInterface
from krita_stable_diffusion.interface.interfaces.horizontal_interface import HorizontalInterface
from krita_stable_diffusion.interface.tabs.base import Base
from krita_stable_diffusion.interface.widgets.line_edit import LineEdit
from krita_stable_diffusion.interface.widgets.button import Button
from krita_stable_diffusion.interface.widgets.password_line_edit import PasswordLineEdit


class LoginTab(Base):
    name = "LoginTab"
    display_name = "Login"

    def login_callback(self, _element):
        # make a post request to localhost:5959/login with username and password
        # if successful, set the token in the config
        # if unsuccessful, show an error message
        # use the requests library
        self.send(
            "login",
            {
                "username": self.username.widget.text(),
                "password": self.password.widget.text()
            }
        )
        self.soc.sendall(b"\x00")


    def join_callback(self, _element):
        print("join")

    def __init__(self):
        self.username = LineEdit(
            label="Username",
            placeholder="Username",
        )
        self.password = PasswordLineEdit(
            label="Password",
            placeholder="Password",
        )
        login = Button(
            label="Login",
            release_callback=self.login_callback
        )
        join = Button(
            label="Join",
            release_callback=self.join_callback
        )
        super().__init__([
            VerticalInterface(
                widgets=[
                    self.username,
                    self.password
                ],
                interfaces=[
                    HorizontalInterface(widgets=[
                        login,
                        join
                    ])
                ]
            ),
        ])