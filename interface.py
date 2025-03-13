from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QAction, QMessageBox, QProgressBar, QLabel, QSizePolicy
)
from PyQt5.QtCore import Qt
import sys
from main import main
import re

class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # Main Layout
        main_layout = QVBoxLayout()

        # Menu Bar
        self.menu_bar = QMenuBar(self)
        file_menu = self.menu_bar.addMenu("File")
        edit_menu = self.menu_bar.addMenu("Edit")
        about_menu = self.menu_bar.addMenu("About")
        main_layout.addWidget(self.menu_bar)
        
        self.setup_menu_actions(file_menu, edit_menu, about_menu)
        
        # Translator Section
        self.translator_header = QLabel("TRANSLATOR")
        self.translator_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #333; font-family: Arial;")
        main_layout.addWidget(self.translator_header)
        
        translator_layout = QHBoxLayout()

        # Input Area
        self.input_field = QTextEdit(self)
        self.input_field.setPlaceholderText("Input Text...")
        translator_layout.addWidget(self.input_field)

        # Button Layout
        button_layout = QVBoxLayout()
        self.kor_to_eng_btn = QPushButton("한국어 → English", self)
        self.kor_to_eng_btn.setStyleSheet("background-color: green; color: white; font-size: 15px;")
        self.kor_to_eng_btn.clicked.connect(self.translate_korean_to_english)
        
        self.eng_to_kor_btn = QPushButton("English → 한국어", self)
        self.eng_to_kor_btn.setStyleSheet("background-color: blue; color: white; font-size: 15px;")
        self.eng_to_kor_btn.clicked.connect(self.translate_english_to_korean)

        button_layout.addWidget(self.kor_to_eng_btn)
        button_layout.addWidget(self.eng_to_kor_btn)

        translator_layout.addLayout(button_layout)
        
        # Output Area
        self.output_field = QTextEdit(self)
        self.output_field.setPlaceholderText("Output Text...")
        translator_layout.addWidget(self.output_field)
        
        main_layout.addLayout(translator_layout)

        # Grammar Checker Section
        self.grammar_header = QLabel("GRAMMAR CHECKER")
        self.grammar_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #333; font-family: Arial;")
        main_layout.addWidget(self.grammar_header)

        grammar_layout = QHBoxLayout()
        grammar_layout.setAlignment(Qt.AlignTop)

        # Input Area
        self.grammar_input = QTextEdit(self)
        self.grammar_input.setPlaceholderText("Input Text...")
        self.grammar_input.setMaximumWidth(390)
        grammar_layout.addWidget(self.grammar_input)
        grammar_layout.addSpacing(15)

        # Feedback Area
        feedback_layout = QVBoxLayout()
        feedback_layout.setAlignment(Qt.AlignTop)

        feedback_label = QLabel("Feedback:")
        feedback_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #333; font-family: Arial;")

        self.grammar_feedback = QLabel("Some feedback...")
        self.grammar_feedback.setWordWrap(True)
        self.grammar_feedback.setStyleSheet("font-size: 15px; color: #333; font-family: Arial;")
        self.grammar_feedback.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        feedback_layout.addWidget(feedback_label)
        feedback_layout.addWidget(self.grammar_feedback)

        grammar_layout.addLayout(feedback_layout)

        main_layout.addLayout(grammar_layout)

        # Rating Section
        self.rating_label = QLabel("Rate: 0, UNDEFINED")
        self.rating_label.setAlignment(Qt.AlignCenter)
        self.rating_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #333; font-family: Arial;")
        main_layout.addWidget(self.rating_label)

        self.rating_bar = QProgressBar(self)
        self.rating_bar.setMinimum(0)
        self.rating_bar.setMaximum(10)
        main_layout.addWidget(self.rating_bar)

        # Check Button
        self.grammar_check_btn = QPushButton("Check Grammar")
        self.grammar_check_btn.clicked.connect(self.check_grammar)
        main_layout.addWidget(self.grammar_check_btn)

        self.setLayout(main_layout)
        self.setWindowTitle("Korean-English Translator & Grammar Checker")
        self.resize(800, 500)
    
    # Translation Methods
    def translate_korean_to_english(self):
        text = self.input_field.toPlainText()
        if text:
            result = main(f"t-to-en {text}")
            self.output_field.setPlainText(result)
    
    def translate_english_to_korean(self):
        text = self.input_field.toPlainText()
        if text:
            result = main(f"t-to-ko {text}")
            self.output_field.setPlainText(result)
    
    # Grammar Check Methods
    def update_rating_label(self, value):
        if value > 6:
            self.rating_label.setText(f"Rate: {value}, EXCELLENT")
            self.rating_bar.setStyleSheet("QProgressBar::chunk { background-color: green; }")
        elif value > 4:
            self.rating_label.setText(f"Rate: {value}, GOOD")
            self.rating_bar.setStyleSheet("QProgressBar::chunk { background-color: blue; }")
        else:
            self.rating_label.setText(f"Rate: {value}, BAD")
            self.rating_bar.setStyleSheet("QProgressBar::chunk { background-color: red; }")
    
    def update_rating_bar(self, value):
        try:
            value = int(value.split('/')[0])
        except ValueError:
            value = 0
        
        value = max(1, min(10, value))
        self.rating_bar.setValue(value)
        self.update_rating_label(value)

    def check_grammar(self):
        self.rating_bar.setValue(0)
        text = self.grammar_input.toPlainText()
        if text:
            result = main(f"g-check {text}")

            rating_match = re.search(r"\b(\d{1,2})(?:/10)?\b", result)
            feedback_match = re.search(r"Feedback:\s*(.*)", result, re.DOTALL)

            rating = rating_match.group(1) if rating_match else "1"
            feedback = feedback_match.group(1) if feedback_match else "Something went wrong! Please try submitting it again"

            self.update_rating_bar(rating)
            self.grammar_feedback.setText(feedback)

    # Menu Methods
    def setup_menu_actions(self, file_menu, edit_menu, about_menu):
        file_menu.addAction(QAction("Open", self, triggered=self.open_file))
        file_menu.addAction(QAction("Save", self, triggered=self.save_file))
        file_menu.addAction(QAction("Exit", self, triggered=self.close))
        
        edit_menu.addAction(QAction("Clear Translator", self, triggered=self.clear_translator))
        edit_menu.addAction(QAction("Clear Grammar Checker", self, triggered=self.clear_grammar))
        
        about_menu.addAction(QAction("About", self, triggered=self.show_about))
    
    def open_file(self):
        QMessageBox.information(self, "Open File", "Fungsi open file belum diimplementasikan.")
    
    def save_file(self):
        QMessageBox.information(self, "Save File", "Fungsi save file belum diimplementasikan.")
    
    def clear_translator(self):
        self.input_field.clear()
    
    def clear_grammar(self):
        self.grammar_input.clear()
    
    def show_about(self):
        QMessageBox.information(self, "About", "Korean-English Translator and Grammar Checker v1.0\nMade by PyQt5")

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TranslatorApp()
    window.show()
    sys.exit(app.exec_())
