from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import imaplib
import email
import re

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)

browser.get("https://famtest.grameenphone.com/login")

username = "maria.nt@grameenphone.com"
password = "PappaAmmu143#"

usernameField = browser.find_element(By.NAME,"username")
usernameField.send_keys(username)

passwordField = browser.find_element(By.ID,"login-password")
passwordField.send_keys(password)

loginButton = browser.find_element(By.XPATH,'//button[@type = "submit"]')
loginButton.click()

def get_otp_from_email(email_user, email_pass):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_user, email_pass)
    mail.select("inbox")

    # Search for OTP email
    result, data = mail.search(None, 'FROM', '"fam@grameenphone.com"')
    mail_ids = data[0].split()
    latest_email_id = mail_ids[-1]

    # Fetch the email content
    result, message_data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = message_data[0][1]
    msg = email.message_from_bytes(raw_email)

    otp = re.search(r"\b\d{6}\b", msg.get_payload(decode=True).decode())
    if otp:
        return otp.group()
    else:
        return None

otp = get_otp_from_email('maria.nt@grameenphone.com', 'PappaAmmu143#')
otpField = browser.find_element(By.ID, 'otp')
otpField.send_keys(otp)
verifyButton = browser.find_element(By.ID, 'verify_otp')
verifyButton.click()

time.sleep(6)
browser.quit()
