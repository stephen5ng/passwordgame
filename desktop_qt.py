#!/usr/bin/env python3
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent, QCloseEvent, QPixmap
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QDialog, QHBoxLayout)

class SecretWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("HULZO SECRETS")
        self.setFixedSize(400, 200)
        
        layout = QVBoxLayout(self)
        
        message = QLabel("MEET TONIGHT AT 8PM TO DISCUSS BETRAYAL OF DOCTOR PROFESSOR.")
        message.setAlignment(Qt.AlignCenter)
        message.setWordWrap(True)
        layout.addWidget(message)
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

class LoginWindow(QMainWindow):
    def __init__(self, skip_to=None):
        super().__init__()
        self.setWindowTitle("Login")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.showFullScreen()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)
        
        self._login_successful = False
        
        if skip_to == "1":
            self.show_password_screen()
        elif skip_to == "2":
            self.show_fake_desktop()
        else:
            self.show_login_screen()
    
    def show_login_screen(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setFixedWidth(300)
        
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(300)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red;")
        
        self.login_button = QPushButton("Login")
        self.login_button.setFixedWidth(300)
        self.login_button.clicked.connect(self.handle_login)
        
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.login_button)
        
        self.username_input.setFocus()
    
    def closeEvent(self, event: QCloseEvent):
        if not self._login_successful:
            event.ignore()
    
    def keyPressEvent(self, event: QKeyEvent):
        if (event.key() == Qt.Key_F4 and event.modifiers() == Qt.AltModifier) or \
           (event.key() == Qt.Key_W and event.modifiers() == Qt.ControlModifier) or \
           (event.key() == Qt.Key_Q and (event.modifiers() == Qt.ControlModifier or event.modifiers() == Qt.MetaModifier)):
            event.ignore()
            return
            
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.handle_login()
            return
            
        super().keyPressEvent(event)
    
    def show_welcome_message(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        welcome_label = QLabel("WELCOME JEFF HULZO!")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        welcome_label.setAlignment(Qt.AlignCenter)
        
        message_label = QLabel("IT HAS BEEN 30 DAYS SINCE YOU LAST CHANGED YOUR PASSWORD.\nYOU MUST CHANGE YOUR PASSWORD NOW FOR ACCESS.")
        message_label.setStyleSheet("font-size: 18px;")
        message_label.setAlignment(Qt.AlignCenter)
        
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignCenter)
        
        ok_button = QPushButton("OK")
        ok_button.setFixedWidth(300)
        ok_button.clicked.connect(self.show_password_screen)
        button_layout.addWidget(ok_button)
        
        self.layout.addWidget(welcome_label)
        self.layout.addWidget(message_label)
        self.layout.addWidget(button_container)
    
    def show_password_screen(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        prompt_label = QLabel("Please choose a new password")
        prompt_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        prompt_label.setAlignment(Qt.AlignCenter)
        
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Enter new password")
        self.new_password_input.setFixedWidth(300)
        self.new_password_input.textChanged.connect(self.validate_password)
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignCenter)
        
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedWidth(300)
        self.submit_button.clicked.connect(self.handle_password_change)
        self.submit_button.setEnabled(False)
        
        self.layout.addWidget(prompt_label)
        self.layout.addWidget(self.new_password_input)
        self.layout.addWidget(self.error_label)
        self.layout.addWidget(self.submit_button)
    
    def validate_password(self):
        password = self.new_password_input.text()
        if not password:
            self.error_label.setText("")
            self.submit_button.setEnabled(False)
            return
            
        for constraint in self.password_constraints():
            error = constraint(password)
            if error:
                self.error_label.setText(error)
                self.submit_button.setEnabled(False)
                return
                
        self.error_label.setText("")
        self.submit_button.setEnabled(True)
    
    def password_constraints(self):
        return [
            self._check_min_length,
            self._check_has_number,
            self._check_has_uppercase,
            self._check_has_special_char,
            self._check_has_roman_numeral
        ]
    
    def _check_min_length(self, password):
        if len(password) < 5:
            return "Your password must be at least 5 characters."
        return None
    
    def _check_has_number(self, password):
        if not any(c.isdigit() for c in password):
            return "Your password must include a number."
        return None
    
    def _check_has_uppercase(self, password):
        if not any(c.isupper() for c in password):
            return "Your password must include an uppercase letter."
        return None
    
    def _check_has_special_char(self, password):
        special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
        if not any(c in special_chars for c in password):
            return "Your password must contain a special character."
        return None
    
    def _check_has_roman_numeral(self, password):
        roman_numerals = {'I', 'V', 'X', 'L', 'C', 'D', 'M'}
        if not any(c in roman_numerals for c in password):
            return "Your password must include a Roman numeral."
        return None
    
    def handle_password_change(self):
        new_password = self.new_password_input.text()
        for constraint in self.password_constraints():
            error = constraint(new_password)
            if error:
                self.error_label.setText(error)
                return
        self.show_fake_desktop()
    
    def show_fake_desktop(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        trash_label = QLabel()
        pixmap = QPixmap("trashcan.png")
        scaled_pixmap = pixmap.scaled(pixmap.width() // 4, pixmap.height() // 4, 
                                    Qt.KeepAspectRatio, Qt.SmoothTransformation)
        trash_label.setPixmap(scaled_pixmap)
        trash_label.mousePressEvent = self.show_secret_window
        bottom_layout.addWidget(trash_label)
        
        self.layout.addStretch()
        self.layout.addLayout(bottom_layout)
    
    def show_secret_window(self, event):
        secret_window = SecretWindow(self)
        secret_window.exec()
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username == "jhulzo" and password == "password":
            self.status_label.setText("Login successful!")
            self.status_label.setStyleSheet("color: green;")
            self._login_successful = True
            self.show_welcome_message()
        else:
            self.status_label.setText("Invalid login")
            self.status_label.setStyleSheet("color: red;")
            self.password_input.clear()
            self.password_input.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    skip_to = sys.argv[1] if len(sys.argv) > 1 else None
    window = LoginWindow(skip_to)
    window.show()
    sys.exit(app.exec()) 