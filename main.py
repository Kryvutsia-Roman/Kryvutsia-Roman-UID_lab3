import sys
import os
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFrame)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPixmap, QPalette, QBrush, QColor

class SurveyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.questions = [
            "Яку останню книгу ви читали?",
            "Якого жанру вона була?",
            "Хто її автор?",
            "Чи прочитав би ти її ще раз?",
            "Чи порадиш ти прочитати її ще комусь?"
        ]
        self.current_question = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Форма опитування (Qt)")
        self.setFixedSize(800, 600)
        self.set_background("Media/background.jpg")

        # Головний контейнер
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Питання
        self.question_label = QLabel(self.questions[self.current_question])
        self.question_label.setStyleSheet("""
            font-size: 24px; font-weight: bold; color: white;
            background-color: rgba(0, 0, 0, 100); padding: 15px; border-radius: 8px;
        """)
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignCenter)

        # Поле вводу
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Введіть відповідь...")
        self.answer_input.setFixedWidth(400)
        self.answer_input.setStyleSheet("padding: 12px; font-size: 18px; border-radius: 5px;")

        # Кнопка
        self.next_button = QPushButton("Далі")
        self.next_button.setFixedWidth(150)
        self.next_button.setCursor(Qt.PointingHandCursor)
        self.next_button.setStyleSheet("""
            QPushButton { padding: 12px; font-size: 18px; background-color: #f0f0f0; border-radius: 5px; }
            QPushButton:hover { background-color: #e0e0e0; }
        """)
        self.next_button.clicked.connect(self.save_answer)

        self.main_layout.addWidget(self.question_label)
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(self.answer_input)
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

        # Створення кастомного модального вікна (оверлею)
        self.overlay = QFrame(self)
        self.overlay.setGeometry(0, 0, 800, 600)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 180);") # Затемнення
        self.overlay.hide()

        self.modal_box = QFrame(self.overlay)
        self.modal_box.setFixedSize(300, 150)
        self.modal_box.move(250, 225) # Центрування
        self.modal_box.setStyleSheet("background-color: white; border-radius: 10px;")
        
        modal_layout = QVBoxLayout(self.modal_box)
        self.modal_text = QLabel("")
        self.modal_text.setAlignment(Qt.AlignCenter)
        self.modal_text.setStyleSheet("color: black; font-size: 16px; font-weight: bold;")
        
        close_btn = QPushButton("Зрозуміло")
        close_btn.clicked.connect(lambda: self.overlay.hide())
        close_btn.setStyleSheet("padding: 8px; background-color: #ddd; border-radius: 4px;")
        
        modal_layout.addWidget(self.modal_text)
        modal_layout.addWidget(close_btn, alignment=Qt.AlignCenter)

    def show_modal(self, text):
        self.modal_text.setText(text)
        self.overlay.show()
        self.overlay.raise_()

    def set_background(self, img_path):
        if os.path.exists(img_path):
            palette = QPalette()
            img = QPixmap(img_path)
            palette.setBrush(QPalette.Window, QBrush(img.scaled(self.size(), Qt.KeepAspectRatioByExpanding)))
            self.setPalette(palette)
            self.setAutoFillBackground(True)

    def save_answer(self):
        answer = self.answer_input.text().strip()
        if not answer:
            self.show_modal("Будь ласка,\nвведіть відповідь!")
            return

        try:
            if not os.path.exists("Media"): os.makedirs("Media")
            with open("Media/answers.txt", "a", encoding="utf-8") as f:
                f.write(f"{self.questions[self.current_question]} {answer}\n")
        except Exception as e:
            self.show_modal(f"Помилка запису:\n{e}")
            return

        self.answer_input.clear()
        self.current_question += 1

        if self.current_question < len(self.questions):
            self.question_label.setText(self.questions[self.current_question])
        else:
            self.question_label.setText("Опитування завершено!")
            self.answer_input.hide()
            self.next_button.hide()
            self.show_modal("Дякуємо!\nВсі відповіді збережено.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SurveyApp()
    window.show()
    sys.exit(app.exec())