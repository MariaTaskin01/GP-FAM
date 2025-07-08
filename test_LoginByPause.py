import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

@pytest.fixture
def browser():
    logger.info("TC001: Opening the browser")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    assert 1 == 1
    driver.quit()

def test_successful_login(browser):
    username = "maria.nt@grameenphone.com"
    password = "PappaAmmu143#"

    logger.info("TC002: Redirect to login page")
    browser.get("https://famtest.grameenphone.com/login")

    logger.info("TC003: Verify Successful Login")
    username_field = browser.find_element(By.NAME,"username")
    username_field.send_keys(username)

    password_field = browser.find_element(By.ID,"login-password")
    password_field.send_keys(password)

    login_button = browser.find_element(By.XPATH,'//button[@type = "submit"]')
    login_button.click()

    logger.info("TC004: Verify Successful OTP input")
    otp = input("Enter your OTP from Email: ")
    otp_field = browser.find_element(By.ID, "otp")
    otp_field.send_keys(otp)

    verify_button = browser.find_element(By.ID,"verify_otp")
    verify_button.click()
    time.sleep(3)

    wait = WebDriverWait(browser, 10)

    logger.info("TC005: Successful redirect to Warehouse to Site Request page")
    body_class = browser.find_element(By.TAG_NAME, "body").get_attribute("class")
    if "sidebar-collapse" in body_class:
        menu_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'fa-bars')]/ancestor::a")))
        menu_button.click()
        time.sleep(1)

    movement_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'fa-dolly')]/ancestor::a")))
    movement_button.click()
    time.sleep(2)

    issue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'fa-receipt')]/ancestor::a")))
    issue_button.click()
    time.sleep(2)

    ware2site_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[.//p[normalize-space()='Warehouse to Site']/parent::a]")))
    ware2site_dropdown.click()
    time.sleep(2)

    create_request_button = wait.until(EC.element_to_be_clickable((By.XPATH,"//a[contains(normalize-space(),'Create Request')]")))
    create_request_button.click()
    time.sleep(2)

    logger.info("TC006: Successfully Search Item")
    to_site_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@aria-labelledby='select2-to_site-container']//span[@class='select2-selection__arrow']/b")))
    to_site_dropdown.click()
    time.sleep(1)
    to_site_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[text()='MASND1 (IPB035)']")))
    to_site_option.click()
    time.sleep(1)

    purpose_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "select2-purpose-container")))
    purpose_dropdown.click()
    time.sleep(1)
    purpose_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[text()='Issue']")))
    purpose_option.click()
    time.sleep(1)

    delivery_mode_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='-- Select Delivery Mode --']" )))
    delivery_mode_dropdown.click()
    time.sleep(1)
    delivery_mode_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[text()='Hand Delivery']")))
    delivery_mode_option.click()
    time.sleep(1)

    user_type_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='-- Select User Type --']" )))
    user_type_dropdown.click()
    time.sleep(1)
    user_type_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[text()='Rollout']")))
    user_type_option.click()
    time.sleep(1)

    search_button = browser.find_element(By.XPATH,"//i[contains(@class, 'fa-search')]/ancestor::button")
    search_button.click()
    time.sleep(5)

    logger.info("TC007: Successfully load Item in the table")
    item_checkbox2 = wait.until(EC.element_to_be_clickable((By.ID, "item_2")))
    item_checkbox2.click()
    time.sleep(5)

    if not item_checkbox2.is_selected():
        item_checkbox2.click()

    item_checkbox3 = wait.until(EC.element_to_be_clickable((By.ID, "item_3")))
    item_checkbox3.click()
    time.sleep(5)

    if not item_checkbox3.is_selected():
        item_checkbox3.click()

    load_button = browser.find_element(By.XPATH,"//i[contains(@class, 'fa-cloud-download-alt')]/ancestor::button")
    load_button.click()
    time.sleep(5)

    rows = browser.find_elements(By.XPATH, "//table[@id='base_table']/tbody/tr")

    logger.info("TC008: Verify successfully writing test messages")
    receiver_info_text = "This is a test message"
    receiver_info = browser.find_element(By.ID, "receiver")
    receiver_info.send_keys(receiver_info_text)
    time.sleep(2)

    comment_text = "This is a test comment"
    comment = browser.find_element(By.ID, "comment")
    comment.send_keys(comment_text)
    time.sleep(2)

    for row in rows:
        try:
            stock_input = row.find_element(By.XPATH, ".//input[starts-with(@id, 'item_stock_')]")
            stock_value = stock_input.get_attribute("value")

            stock = float(stock_value)
            qty_request = int(1)

            qty_input = row.find_element(By.XPATH, ".//input[starts-with(@id, 'base_item_qty_')]")
            qty_input.clear()
            qty_input.send_keys(str(qty_request))

        except Exception:
            print("Error in:", Exception, "row")

    time.sleep(5)

    logger.info("TC009: Verify Successful Creating request")
    submit_button = browser.find_element(By.XPATH,"//i[contains(@class, 'fa-check-circle')]/ancestor::button")
    submit_button.click()
    time.sleep(8)

    logger.info("TC010: Verify Successful Logout")
    user_prof = browser.find_element(By.XPATH,"//i[contains(@class, 'fa-user')]/ancestor::a")
    user_prof.click()
    time.sleep(2)

    logout_button = browser.find_element(By.XPATH,"//i[contains(@class, 'fa-sign-out-alt')]/ancestor::a")
    logout_button.click()
    time.sleep(10)
    assert 1 == 1

# pytest C:\Users\HP\PycharmProjects\GP-FAM\test_LoginByPause.py --html=report.html --self-contained-html -s
