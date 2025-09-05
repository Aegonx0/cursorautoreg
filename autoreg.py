import sys
import threading
import time
import random
import string
import pyperclip
import re
from faker import Faker
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

stop_flag = False

def open_chrome_incognito():
    options = Options()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(executable_path="/path/to/chromedriver", options=options)
    return driver

def generate_password(first_name, length=8):
    suffix = ''.join(random.choices(string.digits, k=max(0, length - len(first_name))))
    return first_name + suffix

def get_verification_code(driver, email_subject="Cursor"):
    driver.get("https://temp-mail.org/en/")
    code = None
    for _ in range(30):
        if stop_flag:
            return None
        try:
            mail_list = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.mail div.title-subject"))
            )
            for mail in mail_list:
                if email_subject in mail.text:
                    mail.click()
                    time.sleep(2)
                    code_element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.mail-text"))
                    )
                    match = re.search(r"\b\d{6}\b", code_element.text)
                    if match:
                        code = match.group(0)
                        return code
        except:
            time.sleep(2)
    return code

def run_script():
    global stop_flag
    stop_flag = False
    driver = open_chrome_incognito()
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

    first_name_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "firstName"))
    )
    first_name_input.send_keys(first_name)

    last_name_input = driver.find_element(By.NAME, "lastName")
    last_name_input.send_keys(last_name)

    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys(temp_email)

    continue_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue')]"))
    )
    continue_btn.click()

    password = generate_password(first_name, 8)

    password_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_input.send_keys(password)

    continue_password_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue')]"))
    )
    continue_password_btn.click()

    verification_code = get_verification_code(driver)
    if verification_code is None:
        return

    code_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "verificationCode"))
    )
    code_input.send_keys(verification_code)

    verify_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue')]"))
    )
    verify_btn.click()

    print(f"{first_name} {last_name} {temp_email} {password} {verification_code}")

def start_thread():
    threading.Thread(target=run_script).start()

def stop_script():
    global stop_flag
    stop_flag = True

class CursorAutoReg(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cursor AutoReg")
        self.setFixedSize(500, 300)
        self.setStyleSheet("background-color: black;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.start_btn = QPushButton("Start")
        self.start_btn.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.start_btn.setStyleSheet("background-color: #4B0082; color: white; border-radius: 10px;")
        self.start_btn.clicked.connect(start_thread)
        layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.stop_btn.setStyleSheet("background-color: #4B0082; color: white; border-radius: 10px;")
        self.stop_btn.clicked.connect(stop_script)
        layout.addWidget(self.stop_btn)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CursorAutoReg()
    window.show()
    sys.exit(app.exec())
