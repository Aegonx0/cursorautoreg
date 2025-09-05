import sys
import random
import string
import pyperclip
import time
from faker import Faker
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AutomationWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def run(self):
        try:
            options = Options()
            options.add_argument("--incognito")
            driver = webdriver.Chrome(options=options)
            driver.maximize_window()

            driver.get("https://temp-mail.org/en/")
            copy_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button#click-to-copy"))
            )
            time.sleep(random.uniform(1,2))
            copy_btn.click()
            time.sleep(random.uniform(0.5,1.5))
            temp_email = pyperclip.paste()

            driver.get("https://authenticator.cursor.sh/sign-up")
            fake = Faker()
            first_name = fake.first_name()
            last_name = fake.last_name()

            first_name_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Your first name']"))
            )
            time.sleep(random.uniform(0.5,1.5))
            first_name_input.clear()
            first_name_input.send_keys(first_name)
            time.sleep(random.uniform(0.3,1.0))

            last_name_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Your last name']"))
            )
            time.sleep(random.uniform(0.5,1.5))
            last_name_input.clear()
            last_name_input.send_keys(last_name)
            time.sleep(random.uniform(0.3,1.0))

            email_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Your email address']"))
            )
            time.sleep(random.uniform(0.5,1.5))
            email_input.clear()
            email_input.send_keys(temp_email)
            time.sleep(random.uniform(0.3,1.0))

            continue_btn = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continue')]"))
            )
            time.sleep(random.uniform(0.5,1.5))
            continue_btn.click()
            time.sleep(random.uniform(1,2))

            password = first_name + ''.join(random.choices(string.digits, k=4))
            password_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Create a password']"))
            )
            time.sleep(random.uniform(0.5,1.5))
            password_input.clear()
            password_input.send_keys(password)
            time.sleep(random.uniform(0.3,1.0))

            cont_pwd_btn = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continue')]"))
            )
            time.sleep(random.uniform(0.5,1.5))
            cont_pwd_btn.click()
            time.sleep(random.uniform(2,3))

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class CursorAutoReg(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cursor AutoReg")
        self.setFixedSize(700, 400)
        self.setStyleSheet("background-color: black;")
        self.worker = None
        self.initUI()
        self.startRainbowAnimation()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.header = QLabel("Cursor AutoRegister")
        self.header.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self.header.setStyleSheet("color: white; margin-bottom: 10px;")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.header)

        self.title = QLabel("Made by Aegon")
        self.title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        self.start_btn = QPushButton("Start")
        self.start_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B0000;
                color: white;
                border-radius: 10px;
                padding: 8px;
                min-width: 140px;
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
        self.stop_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B0000;
                color: white;
                border-radius: 10px;
                padding: 8px;
                min-width: 140px;
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
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def stop_automation(self):
        if self.worker:
            self.worker.terminate()
            self.worker = None

    def on_finished(self):
        QMessageBox.information(self, "Done", "Automation finished successfully!")

    def on_error(self, msg):
        QMessageBox.critical(self, "Error", f"Automation failed:\n{msg}")

    def startRainbowAnimation(self):
        self.colors = [QColor("red"), QColor("orange"), QColor("yellow"),
                       QColor("green"), QColor("blue"), QColor("indigo"), QColor("violet")]
        self.color_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateRainbowColor)
        self.timer.start(300)

    def updateRainbowColor(self):
        color = self.colors[self.color_index]
        self.title.setStyleSheet(f"color: {color.name()};")
        self.color_index = (self.color_index + 1) % len(self.colors)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CursorAutoReg()
    window.show()
    sys.exit(app.exec())
