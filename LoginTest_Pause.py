from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

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

otp = int(input("Enter your OTP from Email: "))
otpField = browser.find_element(By.ID, "otp")
otpField.send_keys(otp)

verifyButton = browser.find_element(By.ID,"verify_otp")
verifyButton.click()

time.sleep(6)
browser.quit()
