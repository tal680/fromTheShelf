# main.py
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from data import INITIAL_DONATIONS
from screens import DetailsScreen, MainScreen, PostScreen, WelcomeScreen


class MeHaMadafApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("מהמדף - אפליקציה להצלת מזון")
        self.resize(800, 600)

        self.donations = INITIAL_DONATIONS
        self.current_user_type = ""
        self.current_user_name = ""
        self.selected_donation = None

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.screen_welcome = WelcomeScreen(self)
        self.screen_main = MainScreen(self)
        self.screen_post = PostScreen(self)
        self.screen_details = DetailsScreen(self)

        self.stacked_widget.addWidget(self.screen_welcome)  # index 0
        self.stacked_widget.addWidget(self.screen_main)  # index 1
        self.stacked_widget.addWidget(self.screen_post)  # index 2
        self.stacked_widget.addWidget(self.screen_details)  # index 3

        self.show_screen(0)

    def login(self, user_type, name):
        self.current_user_type = user_type
        self.current_user_name = name

        if user_type == "business":
            self.screen_main.btn_post.show()
        else:
            self.screen_main.btn_post.hide()

        self.show_screen(1)

    def show_screen(self, index):
        if index == 1:
            self.screen_main.refresh_table()
        self.stacked_widget.setCurrentIndex(index)

    def open_details(self, donation):
        self.selected_donation = donation
        self.screen_details.load_details(donation)
        self.show_screen(3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    window = MeHaMadafApp()
    window.show()
    sys.exit(app.exec())
