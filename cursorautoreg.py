import sys
import random
import string
import pyperclip
import re
import time
from faker import Faker
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------- AUTOMATION ----------------
class AutomationWorker(QThread):
    finished = pyqtSignal()

    def run(self):
        options = Options()
        options.add_argument("--incognito")
        driver = webdriver.Chrome(executable_path="C:/path/to/chromedriver.exe", options=options)
        driver.maximize_window()

        driver.get("https://temp-mail.org/en/")
        copy_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button#click-to-copy"))
        )
        copy_btn.click()
        temp_email = pyperclip.paste()

        driver.get("https://authenticator.cursor.sh/sign-up")

        fake = Faker()
        first_name = fake.first_name()
        last_name = fake.last_name()

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "firstName"))).send_keys(first_name)
        driver.find_element(By.NAME, "lastName").send_keys(last_name)
        driver.find_element(By.NAME, "email").send_keys(temp_email)

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue')]"))
        ).click()

        password = first_name + ''.join(random.choices(string.digits, k=4))
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue')]"))
        ).click()

        # Normally fetch verification code here ...
        # Example placeholder:
        time.sleep(3)

        self.finished.emit()

# ---------------- GUI ----------------
class CursorAutoReg(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cursor AutoReg")
        self.setFixedSize(700, 400)
        self.setStyleSheet("background-color: black;")
        self.worker = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Made by Aegon")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: white; margin-bottom: 40px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.start_btn = QPushButton("Start")
        self.start_btn.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B0000;
                color: white;
                border-radius: 15px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #A52A2A;
            }
            QPushButton:pressed {
                background-color: #FF0000;
            }
        """)
        self.start_btn.clicked.connect(self.start_automation)
        layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B0000;
                color: white;
                border-radius: 15px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #A52A2A;
            }
            QPushButton:pressed {
                background-color: #FF0000;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_automation)
        layout.addWidget(self.stop_btn)

        self.setLayout(layout)

    def start_automation(self):
        self.worker = AutomationWorker()
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def stop_automation(self):
        if self.worker:
            self.worker.terminate()
            self.worker = None

    def on_finished(self):
        print("Automation finished")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CursorAutoReg()
    window.show()
    sys.exit(app.exec())
