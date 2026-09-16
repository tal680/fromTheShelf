import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QHBoxLayout,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)


class UIMainScreenCollectorDonation(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        img_label = QLabel("Image")
        layout.addWidget(img_label)

        text_layout = QVBoxLayout()
        title_label = QLabel("Title")
        title_font = title_label.font()
        title_font.setPointSize(16)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        text_layout.addWidget(title_label)

        details_layout = QHBoxLayout()
        amount_label = QLabel("Amount")
        details_layout.addWidget(amount_label)

        city_label = QLabel("City")
        details_layout.addWidget(city_label)

        text_layout.addLayout(details_layout)

        layout.addLayout(text_layout)

        widget = QWidget()
        widget.setLayout(layout)
