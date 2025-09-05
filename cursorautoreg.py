import sys
import random
import string
import pyperclip
import re
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

# ---------------- AUTOMATION ----------------
class AutomationWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def run(self):
        try:
            options = Options()
            options.add_argument("--incognito")
            driver = webdriver.Chrome(options=options)  # FIXED: no executable_path
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

            # TODO: implement verification email fetching properly
            time.sleep(3)

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

# ---------------- GUI ----------------
class CursorAutoReg(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cursor AutoReg")
        self.setFixedSize(900, 500)
        self.setStyleSheet("background-color: black;")
        self.worker = None
        self.initUI()
        self.startRainbowAnimation()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel("Made by Aegon")
        self.title.setFont(QFont("Segoe UI", 36, QFont.Weight.Bold))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        self.start_btn = QPushButton("Start")
        self.start_btn.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B0000;
                color: white;
                border-radius: 12px;
                padding: 10px;
                min-width: 160px;
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
        self.stop_btn.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B0000;
                color: white;
                border-radius: 12px;
                padding: 10px;
                min-width: 160px;
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

    # Rainbow animation for "Made by Aegon"
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
