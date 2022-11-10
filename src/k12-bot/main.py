from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from urllib3 import response
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import logging as log
import sys
import time
import yaml
import gzip
from ansparser import parse

log.basicConfig(filename="logs.log", level=log.INFO)

log.info("parse config file")
with open("config.yaml", "r") as stream:
    user = yaml.safe_load(stream)


mobile_emulation = {
    "deviceMetrics": {"width": 1366, "height": 786, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
}

# Setup
log.info("set up webdriver")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension("./extensions/always-active-ext.crx")
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
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


def gunzip_bytes_obj(bytes_obj: bytes) -> str:
    return gzip.decompress(bytes_obj).decode()


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


log.info("parsing config file")
with open("config.yaml", "r") as stream:
    user = yaml.safe_load(stream)

# Auth
text_input("Tên tài khoản", user["name"])
text_input("Mật khẩu", user["password"])
login_button_click()

# getting into the exam page
log.info("getting into the exam page")
time.sleep(0.5)
driver.find_element("xpath", f"//span[contains(text(), 'Kiểm tra, đánh giá')]").click()
time.sleep(0.5)
driver.find_element("xpath", f"//span[contains(text(), 'Bài kiểm tra')]").click()
time.sleep(1)

# find total exams
all_tests = driver.find_elements(
    "xpath", "//div[@class='test-item mb-10 happening  exam-sucess']"
)

if len(all_tests) == 0:
    log.info("no active test, exiting")
    quit()

# if there is tests then list them all and the let the user select
log.info("selecting exam")
for i, test in enumerate(all_tests):
    text_name = test.find_element(By.TAG_NAME, "b").get_attribute("innerText")
    print(f"{i+1}. {text_name}")

selected_test = int(input("Input the desired test to be done: ")) - 1
all_tests[selected_test].find_element(By.TAG_NAME, "a").click()
# becaues it's on mobile simulation, a confirmation button is shown
time.sleep(0.5)
driver.find_element(By.XPATH, "//button[contains(text(), 'Tiếp tục')]").click()
time.sleep(0.5)
driver.find_element(By.XPATH, "//button[contains(text(), 'Đồng ý')]").click()
time.sleep(3)
log.info("enter exam")


# refresh for the result exploit
log.info("attemping the exploit")
driver.refresh()
time.sleep(3)

# request that contains the answer
course_site_id = driver.current_url.partition("courseSiteId=")[2]
# request that contains the answer
good_req_url = f"https://agg-thptnguyentrungtruc.k12online.vn/?module=Content.Form&moduleId=1&cmd=redraw&site={course_site_id}&url_mode=rewrite&submitFormId=1&moduleId=1&page=Courseware.Exam.doExam&site={course_site_id}"

found_req = False
for i in range(0, user["max_attemp"]):
    log.info(f"trying to get the `good request` exploit ({i} times)")
    for req in driver.requests:
        if req.response and req.url == good_req_url:
            res_text = gunzip_bytes_obj(req.response.body)
            found_req = True
            break
    if found_req:
        break
    driver.refresh()
    time.sleep(3)

log.info("export the `good response` to a file")
file = open("response-decoded.txt", "w+")
file.write(res_text)
file.close()

log.info("getting correct answers")
correct_answers = parse(res_text, 25, 4)
all_answers = driver.find_elements(By.XPATH, "//div[@class='radio  ']")
all_answers = chunks(all_answers, 4)

log.info("ticking all the question")
for i, question in enumerate(all_answers):
    # click on correct answer
    question[correct_answers[i]].find_element(By.TAG_NAME, "input").click()
    time.sleep(0.5)

log.info("finished")

time.sleep(100000)
