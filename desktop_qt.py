#!/usr/bin/env python3
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette, QKeyEvent, QCloseEvent

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        
        # Set window flags to prevent closing while allowing keyboard input
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        # Set window to full screen
        self.showFullScreen()
        
        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)
        
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
        
        # Status message
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: red;")
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setFixedWidth(300)
        self.login_button.clicked.connect(self.handle_login)
        
        # Add widgets to layout
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.login_button)
        
        # Set focus to username field
        self.username_input.setFocus()
        
        # Track if login was successful
        self._login_successful = False
    
    def closeEvent(self, event: QCloseEvent):
        # Only allow closing if login was successful
        if not self._login_successful:
            event.ignore()
    
    def keyPressEvent(self, event: QKeyEvent):
        # Block specific system shortcuts
        if (event.key() == Qt.Key_F4 and event.modifiers() == Qt.AltModifier) or \
           (event.key() == Qt.Key_W and event.modifiers() == Qt.ControlModifier) or \
           (event.key() == Qt.Key_Q and (event.modifiers() == Qt.ControlModifier or event.modifiers() == Qt.MetaModifier)):
            event.ignore()
            return
            
        # Handle Enter key for login
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.handle_login()
            return
            
        # Allow all other key events
        super().keyPressEvent(event)
    
    def show_welcome_message(self):
        # Clear the layout
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Create welcome message
        welcome_label = QLabel("WELCOME JEFF HULZO!")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        welcome_label.setAlignment(Qt.AlignCenter)
        
        message_label = QLabel("IT HAS BEEN 30 DAYS SINCE YOU LAST CHANGED YOUR PASSWORD.\nCHANGE YOUR PASSWORD NOW TO CONTINUE.")
        message_label.setStyleSheet("font-size: 18px;")
        message_label.setAlignment(Qt.AlignCenter)
        
        # Create button container with horizontal layout
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignCenter)
        
        # Add OK button
        ok_button = QPushButton("OK")
        ok_button.setFixedWidth(300)
        ok_button.clicked.connect(self.show_password_screen)
        button_layout.addWidget(ok_button)
        
        # Add welcome message to layout
        self.layout.addWidget(welcome_label)
        self.layout.addWidget(message_label)
        self.layout.addWidget(button_container)
    
    def show_password_screen(self):
        # Clear the layout
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Create password prompt
        prompt_label = QLabel("Please choose a password")
        prompt_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        prompt_label.setAlignment(Qt.AlignCenter)
        
        # Create password input
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Enter new password")
        self.new_password_input.setFixedWidth(300)
        self.new_password_input.textChanged.connect(self.validate_password)
        
        # Create error message label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignCenter)
        
        # Create submit button
        submit_button = QPushButton("Submit")
        submit_button.setFixedWidth(300)
        submit_button.clicked.connect(self.handle_password_change)
        
        # Add widgets to layout
        self.layout.addWidget(prompt_label)
        self.layout.addWidget(self.new_password_input)
        self.layout.addWidget(self.error_label)
        self.layout.addWidget(submit_button)
    
    def validate_password(self):
        password = self.new_password_input.text()
        if len(password) > 0 and len(password) < 5:
            self.error_label.setText("Your password must be at least 5 characters.")
        else:
            self.error_label.setText("")
    
    def handle_password_change(self):
        new_password = self.new_password_input.text()
        if len(new_password) < 5:
            self.error_label.setText("Your password must be at least 5 characters.")
            return
        # TODO: Implement password change logic
        self.close()
    
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
    window = LoginWindow()
    window.show()
    sys.exit(app.exec()) 