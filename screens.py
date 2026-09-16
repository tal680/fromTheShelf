# screens.py
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


# --- 1. מסך פתיחה ---
class WelcomeScreen(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("מהמדף")
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: green;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("מצילים מזון ומעבירים אותו למי שצריך")
        subtitle.setStyleSheet("font-size: 18px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_business = QPushButton("כניסה כעסק / סופר")
        btn_business.setStyleSheet("font-size: 16px; padding: 10px;")
        btn_business.clicked.connect(
            lambda: self.main_app.login("business", "סופר שופרסל מרכז")
        )

        btn_user = QPushButton("כניסה כעמותה")
        btn_user.setStyleSheet("font-size: 16px; padding: 10px;")
        btn_user.clicked.connect(lambda: self.main_app.login("user", "עמותת פתחון לב"))

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(btn_business)
        layout.addWidget(btn_user)


# --- 2. מסך ראשי (טבלת תרומות) ---
class MainScreen(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        layout = QVBoxLayout(self)

        self.title_label = QLabel("רשימת התרומות")
        self.title_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: green;"
        )
        layout.addWidget(self.title_label)

        # סרגל עליון
        top_bar = QHBoxLayout()

        self.btn_post = QPushButton("+ פרסם תרומה חדשה")
        self.btn_post.setStyleSheet(
            "background-color: #2e7d32; color: white; padding: 8px; font-weight: bold;"
        )
        self.btn_post.clicked.connect(lambda: self.main_app.show_screen(2))

        btn_logout = QPushButton("החלף משתמש")
        btn_logout.clicked.connect(lambda: self.main_app.show_screen(0))

        top_bar.addWidget(self.btn_post)
        top_bar.addStretch()
        top_bar.addWidget(btn_logout)
        layout.addLayout(top_bar)

        # טבלה
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["שם העסק", "מוצר", "כמות", "קטגוריה", "זמן איסוף", "סטטוס / פעולה"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

    def refresh_table(self):
        # מציגים את כל התרומות ברשימה (גם אלו שנלקחו)
        all_donations = self.main_app.donations
        self.table.setRowCount(len(all_donations))

        for row, item in enumerate(all_donations):
            cell_business = QTableWidgetItem(item["business"])
            cell_product = QTableWidgetItem(item["product"])
            cell_quantity = QTableWidgetItem(item["quantity"])
            cell_category = QTableWidgetItem(item["category"])
            cell_time = QTableWidgetItem(item["time"])

            cells = [
                cell_business,
                cell_product,
                cell_quantity,
                cell_category,
                cell_time,
            ]

            # בודקים אם התרומה כבר נלקחה
            is_requested = item["status"] == "נלקחה"

            # אם התרומה נלקחה, משנים את רקע התאים לירוק
            if is_requested:
                for cell in cells:
                    cell.setBackground(QColor("#69e86e"))  # ירוק בהיר

            self.table.setItem(row, 0, cell_business)
            self.table.setItem(row, 1, cell_product)
            self.table.setItem(row, 2, cell_quantity)
            self.table.setItem(row, 3, cell_category)
            self.table.setItem(row, 4, cell_time)

            # יצירת כפתור הפעולה
            btn_view = QPushButton("נלקחה" if is_requested else "צפה בפרטים")
            btn_view.setStyleSheet("font-weight: bold;")

            if is_requested:
                btn_view.setEnabled(False)  # ניטרול הכפתור
            else:
                btn_view.setStyleSheet("color: green; font-weight: bold;")
                btn_view.clicked.connect(
                    lambda _, d=item: self.main_app.open_details(d)
                )

            self.table.setCellWidget(row, 5, btn_view)


# --- 3. מסך פרסום תרומה ---
class PostScreen(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        layout = QVBoxLayout(self)

        title = QLabel("פרסום תרומה חדשה")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: green;")
        layout.addWidget(title)

        layout.addWidget(QLabel("שם המוצר:"))
        self.input_product = QLineEdit()
        layout.addWidget(self.input_product)

        layout.addWidget(QLabel("כמות:"))
        self.input_quantity = QLineEdit()
        layout.addWidget(self.input_quantity)

        layout.addWidget(QLabel("קטגוריה:"))
        self.combo_category = QComboBox()
        self.combo_category.addItems(
            ["מאפים ולחמים", "מוצרי חלב", "פירות וירקות", "מוצרים ארוזים", "אחר"]
        )
        layout.addWidget(self.combo_category)

        layout.addWidget(QLabel("זמן איסוף אחרון:"))
        self.input_time = QLineEdit()
        self.input_time.setPlaceholderText("לדוגמה: עד 20:00")
        layout.addWidget(self.input_time)

        layout.addWidget(QLabel("הערות נוספות:"))
        self.input_notes = QTextEdit()
        layout.addWidget(self.input_notes)

        btn_publish = QPushButton("פרסם תרומה")
        btn_publish.setStyleSheet(
            "background-color: green; color: white; padding: 8px;"
        )
        btn_publish.clicked.connect(self.publish)

        btn_back = QPushButton("ביטול")
        btn_back.clicked.connect(lambda: self.main_app.show_screen(1))

        layout.addWidget(btn_publish)
        layout.addWidget(btn_back)

    def publish(self):
        product_name = self.input_product.text().strip()
        quantity = self.input_quantity.text().strip()

        if not product_name or not quantity:
            QMessageBox.warning(self, "שגיאה", "אנא מלא שם מוצר וכמות")
            return

        new_donation = {
            "id": len(self.main_app.donations) + 1,
            "business": self.main_app.current_user_name,
            "product": product_name,
            "quantity": quantity,
            "category": self.combo_category.currentText(),
            "time": self.input_time.text(),
            "notes": self.input_notes.toPlainText(),
            "status": "זמינה",
            "requested_by": "",
        }

        self.main_app.donations.append(new_donation)

        self.input_product.clear()
        self.input_quantity.clear()
        self.input_time.clear()
        self.input_notes.clear()

        QMessageBox.information(self, "הצלחה", "התרומה פורסמה בהצלחה!")
        self.main_app.show_screen(1)


# --- 4. מסך פרטי תרומה ---
class DetailsScreen(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        layout = QVBoxLayout(self)

        title = QLabel("פרטי התרומה")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: green;")
        layout.addWidget(title)

        self.lbl_business = QLabel()
        self.lbl_product = QLabel()
        self.lbl_quantity = QLabel()
        self.lbl_category = QLabel()
        self.lbl_time = QLabel()
        self.lbl_notes = QLabel()

        self.lbl_status = QLabel()
        self.lbl_status.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: green;"
        )

        layout.addWidget(self.lbl_business)
        layout.addWidget(self.lbl_product)
        layout.addWidget(self.lbl_quantity)
        layout.addWidget(self.lbl_category)
        layout.addWidget(self.lbl_time)
        layout.addWidget(self.lbl_notes)
        layout.addWidget(self.lbl_status)

        self.btn_request = QPushButton("אני רוצה את התרומה הזו")
        self.btn_request.setStyleSheet(
            "background-color: green; color: white; padding: 10px; font-weight: bold;"
        )
        self.btn_request.clicked.connect(self.request)
        layout.addWidget(self.btn_request)

        btn_back = QPushButton("חזרה לרשימה")
        btn_back.clicked.connect(lambda: self.main_app.show_screen(1))
        layout.addWidget(btn_back)

    def load_details(self, donation):
        self.lbl_business.setText(f"שם העסק: {donation['business']}")
        self.lbl_product.setText(f"מוצר: {donation['product']}")
        self.lbl_quantity.setText(f"כמות: {donation['quantity']}")
        self.lbl_category.setText(f"קטגוריה: {donation['category']}")
        self.lbl_time.setText(f"זמן איסוף: {donation['time']}")
        self.lbl_notes.setText(f"הערות: {donation['notes']}")
        self.lbl_status.setText(f"סטטוס תרומה: {donation['status']}")

        if self.main_app.current_user_type == "user" and donation["status"] == "זמינה":
            self.btn_request.show()
        else:
            self.btn_request.hide()

    def request(self):
        donation = self.main_app.selected_donation
        if donation:
            donation["status"] = "נלקחה"
            donation["requested_by"] = self.main_app.current_user_name
            QMessageBox.information(self, "בהצלחה", "התרומה נשמרה עבורך!")
            self.main_app.show_screen(1)
