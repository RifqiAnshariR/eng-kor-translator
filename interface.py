import sys
import os
import re

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QDialog, QTextEdit, QPushButton, QVBoxLayout, 
    QHBoxLayout, QMenuBar, QMenu, QAction, QMessageBox, QProgressBar, QLabel, 
    QSizePolicy
)

from main import ModelHandler
from config import (
    MODEL_NAME, HEADER_FONTSTYLE, LABEL_1_FONTSTYLE, LABEL_2_FONTSTYLE, 
    KOR_ENG_BUTTONSTYLE, ENG_KOR_BUTTONSTYLE, GRAMMAR_BUTTONSTYLE, LOG_DIR, LOG_NAME
)

class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.runModel(MODEL_NAME)
    
    def runModel(self, model_name):
        self.model = ModelHandler(model_name)
    
    def init_ui(self):
        # Main Layout
        main_layout = QVBoxLayout()

        # Menu Bar
        self.menu_bar = QMenuBar(self)
        options_menu = self.menu_bar.addMenu("Options")
        edit_menu = self.menu_bar.addMenu("Edit")
        about_menu = self.menu_bar.addMenu("About")
        main_layout.addWidget(self.menu_bar)
        
        self.setup_menu_actions(options_menu, edit_menu, about_menu)
        
        # Translator Section
        self.translator_header = QLabel("TRANSLATOR")
        self.translator_header.setStyleSheet(HEADER_FONTSTYLE)
        main_layout.addWidget(self.translator_header)
        
        translator_layout = QHBoxLayout()

        # Input Area
        self.translator_input = QTextEdit(self)
        self.translator_input.setPlaceholderText("Input Text...")
        translator_layout.addWidget(self.translator_input)

        # Button Layout
        button_layout = QVBoxLayout()
        self.kor_to_eng_btn = QPushButton("한국어 → English", self)
        self.kor_to_eng_btn.setStyleSheet(KOR_ENG_BUTTONSTYLE)
        self.kor_to_eng_btn.clicked.connect(self.translate_korean_to_english)
        
        self.eng_to_kor_btn = QPushButton("English → 한국어", self)
        self.eng_to_kor_btn.setStyleSheet(ENG_KOR_BUTTONSTYLE)
        self.eng_to_kor_btn.clicked.connect(self.translate_english_to_korean)

        button_layout.addWidget(self.kor_to_eng_btn)
        button_layout.addWidget(self.eng_to_kor_btn)

        translator_layout.addLayout(button_layout)
        
        # Output Area
        self.translator_output = QTextEdit(self)
        self.translator_output.setPlaceholderText("Output Text...")
        translator_layout.addWidget(self.translator_output)
        
        main_layout.addLayout(translator_layout)

        # Grammar Checker Section
        self.grammar_header = QLabel("GRAMMAR CHECKER")
        self.grammar_header.setStyleSheet(HEADER_FONTSTYLE)
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
        feedback_label.setStyleSheet(LABEL_1_FONTSTYLE)

        self.grammar_output = QLabel("Some feedback...")
        self.grammar_output.setWordWrap(True)
        self.grammar_output.setStyleSheet(LABEL_2_FONTSTYLE)
        self.grammar_output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        feedback_layout.addWidget(feedback_label)
        feedback_layout.addWidget(self.grammar_output)

        grammar_layout.addLayout(feedback_layout)

        main_layout.addLayout(grammar_layout)

        # Rating Section
        self.rating_label = QLabel("Rate: --, UNDEFINED")
        self.rating_label.setAlignment(Qt.AlignCenter)
        self.rating_label.setStyleSheet(LABEL_1_FONTSTYLE)
        main_layout.addWidget(self.rating_label)

        self.rating_bar = QProgressBar(self)
        self.rating_bar.setMinimum(0)
        self.rating_bar.setMaximum(10)
        self.rating_bar.setTextVisible(False)
        self.rating_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(self.rating_bar)

        # Check Button
        self.grammar_check_btn = QPushButton("Check Grammar")
        self.grammar_check_btn.setStyleSheet(GRAMMAR_BUTTONSTYLE)
        self.grammar_check_btn.clicked.connect(self.check_grammar)
        main_layout.addWidget(self.grammar_check_btn)

        self.setLayout(main_layout)
        self.setWindowTitle("Korean-English Translator & Grammar Checker")
        self.resize(800, 500)
    
    # Translation Methods
    def translate_korean_to_english(self):
        text = self.translator_input.toPlainText()
        if text:
            result = self.model.generate_response(f"t-to-en {text}")
            self.translator_output.setPlainText(result)
    
    def translate_english_to_korean(self):
        text = self.translator_input.toPlainText()
        if text:
            result = self.model.generate_response(f"t-to-ko {text}")
            self.translator_output.setPlainText(result)
    
    # Grammar Check Methods
    def update_rating_label(self, value):
        if value > 6:
            self.rating_label.setText(f"Rate: {value}/10, EXCELLENT")
            self.rating_bar.setStyleSheet("QProgressBar::chunk { background-color: green; }")
        elif value > 4:
            self.rating_label.setText(f"Rate: {value}/10, GOOD")
            self.rating_bar.setStyleSheet("QProgressBar::chunk { background-color: blue; }")
        else:
            self.rating_label.setText(f"Rate: {value}/10, BAD")
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
            result = self.model.generate_response(f"g-check {text}")

            rating_match = re.search(r"\b(\d{1,2})(?:/10)?\b", result)
            feedback_match = re.search(r"Feedback:\s*(.*)", result, re.DOTALL)
            rating = rating_match.group(1) if rating_match else "0"
            feedback = feedback_match.group(1) if feedback_match else "Something went wrong! Please try submitting it again"

            self.update_rating_bar(rating)
            self.grammar_output.setText(feedback)

    # Menu Methods
    def setup_menu_actions(self, options_menu, edit_menu, about_menu):
        options_menu.addAction(QAction("View Logs", self, triggered=self.view_logs))
        options_menu.addAction(QAction("Exit", self, triggered=self.close))
        
        edit_menu.addAction(QAction("Clear Translator", self, triggered=self.clear_translator))
        edit_menu.addAction(QAction("Clear Grammar Checker", self, triggered=self.clear_grammar))
        
        about_menu.addAction(QAction("About", self, triggered=self.show_about))
    
    def view_logs(self):
        log_dialog = QDialog(self)
        log_dialog.setWindowTitle("Process Logs")
        log_dialog.resize(600, 400)
        log_dialog.setWindowFlags(log_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        layout = QVBoxLayout()

        log_viewer = QTextEdit()
        log_viewer.setReadOnly(True)

        log_path = os.path.join(LOG_DIR, LOG_NAME)
        try:
            with open(log_path, "r", encoding="utf-8") as log_file:
                log_viewer.setPlainText(log_file.read())
        except Exception as e:
            log_viewer.setPlainText(f"Error loading logs: {e}")

        layout.addWidget(log_viewer)

        log_dialog.setLayout(layout)
        log_dialog.exec_()
    
    def clear_translator(self):
        self.translator_input.clear()
    
    def clear_grammar(self):
        self.grammar_input.clear()
    
    def show_about(self):
        QMessageBox.information(self, "About", 
                                "Korean-English Translator and Grammar Checker v1.0\nModel: LGAI EXAONE 2.4B Params\nMade by PyQt5")
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TranslatorApp()
    window.show()
    sys.exit(app.exec_())
