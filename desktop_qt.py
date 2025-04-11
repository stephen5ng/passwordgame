#!/usr/bin/env python3
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Qt

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(400, 300)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        
        # Username
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setFixedWidth(300)
        
        # Password
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(300)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setFixedWidth(300)
        self.login_button.clicked.connect(self.handle_login)
        
        # Add widgets to layout
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        
        # Set focus to username field
        self.username_input.setFocus()
        
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username == "jhulzo" and password == "password":
            QMessageBox.information(self, "Success", "Login successful!")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")
            self.password_input.clear()
            self.password_input.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec()) 