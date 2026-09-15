import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout
from PySide6.QtCore import QSize, Qt

app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
# window = QWidget()
# window.show()  # IMPORTANT Windows are hidden by default.

# Start the event loop.
# app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # יצירת כפתור לחיצה
        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")

        self.setFixedSize(QSize(400, 300))

        # Set the central widget of the Window
        self.setCentralWidget(button)

        # הדפסת hello
        # label = QLabel("Hello")
        # font = label.font()
        # font.setPointSize(30)
        # label.setFont(font)
        # label.setAlignment(
        #     Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        # )

        # self.setCentralWidget(label)

        # העלאת תמונה
        # label = QLabel()
        # label.setPixmap(QPixmap("some.png"))

if not QApplication.instance():
    app = QApplication(sys.argv)
else:
    app = QApplication.instance()

window = MainWindow()
window.show()

app.exec()