from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import logging as log
import sys
import time
import yaml

log.info("parse config file")
with open("config.yaml", "r") as stream:
    user = yaml.safe_load(stream)

log.basicConfig(stream=sys.stdout, level=log.INFO)

# Setup
log.info("set up webdriver")
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--window-size=1920x1080")
# chrome_options.add_argument("--hide-scrollbars")

driver = webdriver.Chrome(
    options=chrome_options,
    service=ChromeService(executable_path=ChromeDriverManager().install()),
)
action = ActionChains(driver)

driver.get("https://agg-thptnguyentrungtruc.k12online.vn")


def text_input(name, input):
    driver.find_element("xpath", f"//input[@placeholder='{name}']").send_keys(input)


def login_button_click():
    button_class = "btn btn-primary btn-login"
    driver.find_element("xpath", f"//button[@class='{button_class}']").click()


log.info("parse config file")
with open("config.yaml", "r") as stream:
    user = yaml.safe_load(stream)

text_input("Tên tài khoản", user["name"])
text_input("Mật khẩu", user["password"])
login_button_click()

time.sleep(0.5)
driver.find_element("xpath", f"//span[contains(text(), 'Kiểm tra, đánh giá')]").click()
time.sleep(0.5)
driver.find_element("xpath", f"//span[contains(text(), 'Bài kiểm tra')]").click()


time.sleep(1000)
