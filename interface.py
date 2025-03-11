import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMenuBar, QMenu, QAction, QMessageBox
from main import response

class TranslatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Layout utama
        main_layout = QVBoxLayout()

        # Menu Bar
        self.menu_bar = QMenuBar(self)
        file_menu = self.menu_bar.addMenu("File")
        edit_menu = self.menu_bar.addMenu("Edit")
        help_menu = self.menu_bar.addMenu("Help")
        main_layout.addWidget(self.menu_bar)

        # Tambahkan aksi ke menu
        self.initMenuActions(file_menu, edit_menu, help_menu)
        
        # Layout utama untuk teks dan tombol
        layout = QHBoxLayout()

        # Area input (Korean)
        self.korean_text = QTextEdit(self)
        self.korean_text.setPlaceholderText("Input Text")
        layout.addWidget(self.korean_text)

        # Tombol translasi
        button_layout = QVBoxLayout()
        self.kor_to_eng_button = QPushButton("한국어 → English", self)
        self.kor_to_eng_button.setStyleSheet("background-color: green; color: white;")
        
        self.eng_to_kor_button = QPushButton("English → 한국어", self)
        self.eng_to_kor_button.setStyleSheet("background-color: blue; color: white;")

        button_layout.addWidget(self.kor_to_eng_button)
        button_layout.addWidget(self.eng_to_kor_button)

        layout.addLayout(button_layout)

        # Area output (English)
        self.english_text = QTextEdit(self)
        self.english_text.setPlaceholderText("Output Text")
        layout.addWidget(self.english_text)

        main_layout.addLayout(layout)
        self.setLayout(main_layout)
        self.setWindowTitle("Korean-English Translator")
        self.resize(800, 400)

    def initMenuActions(self, file_menu, edit_menu, help_menu):
        # File menu actions
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.openFile)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.saveFile)
        file_menu.addAction(save_action)
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu actions
        clear_action = QAction("Clear Text", self)
        clear_action.triggered.connect(self.clearText)
        edit_menu.addAction(clear_action)
        
        # Help menu actions
        about_action = QAction("About", self)
        about_action.triggered.connect(self.showAbout)
        help_menu.addAction(about_action)
    
    def openFile(self):
        QMessageBox.information(self, "Open File", "Fungsi open file belum diimplementasikan.")
    
    def saveFile(self):
        QMessageBox.information(self, "Save File", "Fungsi save file belum diimplementasikan.")
    
    def clearText(self):
        self.korean_text.clear()
        self.english_text.clear()
    
    def toggleMenu(self):
        self.menu_bar.setVisible(not self.menu_bar.isVisible())
    
    def showAbout(self):
        QMessageBox.information(self, "About", "Korean-English Translator v1.0\nDibuat dengan PyQt5")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator_ui = TranslatorUI()
    translator_ui.show()
    sys.exit(app.exec_())
