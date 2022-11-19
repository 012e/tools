from selenium.webdriver.common.by import By

import logging as log
import time
import yaml
import sys
from ansparser import parse
from botconfig import BotConfig
from botdriver import BotDriver
from utils import decode_gzip_bytes, read_file

log.basicConfig(filename="logs.log", level=log.INFO)
# log.basicConfig(stream=sys.stdout, level=log.DEBUG)


log.info("parse config file")
with open("config.yaml", "r") as stream:
    config = yaml.safe_load(stream)


class K12Bot:
    def __init__(self, config: BotConfig):
        self.config = config
        self.bot = BotDriver(config["browser"])
        self.bot.driver.get("https://agg-thptnguyentrungtruc.k12online.vn")

    def auth(self):
        self.bot.text_input("Tên tài khoản", self.config["username"])
        self.bot.text_input("Mật khẩu", self.config["password"])
        login_button_class = "btn btn-primary btn-login"
        self.bot.driver.find_element(
            By.XPATH, f"//button[@class='{login_button_class}']"
        ).click()

    def auto_select_test(self):
        log.info("entering test page")
        self.bot.click_contains("span", "Kiểm tra, đánh giá")
        self.bot.click_contains("span", "Bài kiểm tra")
        time.sleep(0.5)
        all_tests = self.bot.driver.find_elements(
            By.XPATH, "//div[@class='test-item mb-10 happening  exam-sucess']"
        )

        if len(all_tests) == 0:
            log.info("no active test, exiting")
            quit()

        # if there are tests then list them all and the let the user select
        log.info("selecting test")
        for i, test in enumerate(all_tests):
            text_name = test.find_element(By.TAG_NAME, "b").get_attribute("innerText")
            print(f"{i+1}. {text_name}")

        selected_test = int(input("Input the desired test to be done: ")) - 1
        all_tests[selected_test].find_element(By.TAG_NAME, "a").click()
        time.sleep(1)
        # becaues it's on mobile simulation, a confirmation button is shown
        self.bot.click_contains("button", "Tiếp tục")
        self.bot.click_contains("button", "Đồng ý")
        time.sleep(3)

    def handle_state(self):
        while read_file("state") == "0":
            time.sleep(1)

    def finish_normal_test(self):
        for i, question in enumerate(self.all_questions):
            self.handle_state()
            log.info(f"checked on question {i+1}")
            answers = question.find_elements(By.TAG_NAME, "div")
            answers[self.correct_answers[i]].find_element(By.TAG_NAME, "input").click()
            time.sleep(0.5)

    def finish_single_paged_test(self):
        for i, question in enumerate(self.all_questions):
            self.handle_state()
            log.info(f"checked on question {i+1}")
            answers = question.find_elements(By.TAG_NAME, "div")
            answers[self.correct_answers[i]].find_element(By.TAG_NAME, "input").click()
            time.sleep(1)
            if i != len(self.all_questions) - 1:
                self.bot.click_after_appearance("//a[@title='Câu tiếp']")

    def complete_test(self):
        good_req_url = f"https://agg-thptnguyentrungtruc.k12online.vn/?module=Content.Form&moduleId=1&cmd=redraw&site="
        log.info("attemping the exploit")
        self.bot.driver.refresh()
        time.sleep(1)

        found_req = False
        for i in range(0, self.config["max_attemp"]):
            log.info(f"trying to get the `good request` exploit ({i} times)")
            for req in self.bot.driver.requests:
                if req.response and req.url.startswith(good_req_url):
                    res_text = decode_gzip_bytes(req.response.body)
                    found_req = True
                    break
            if found_req:
                break
            self.bot.driver.refresh()
            time.sleep(3)

        log.info("getting all questions")
        self.all_questions = self.bot.driver.find_elements(
            By.XPATH, "//div[@class='choice-info-val']"
        )
        log.info("getting correct answers")
        self.correct_answers = parse(res_text, len(self.all_questions), 4)  # type: ignore

        log.info("ticking all the question")
        if self.bot.check_exists_by_xpath("//a[@title='Câu tiếp']"):
            self.finish_single_paged_test()
        else:
            self.finish_normal_test()
        time.sleep(1000000)


#
#
#
# log.info("export the `good response` to a file")
# file = open("response-decoded.txt", "w+")
# file.write(res_text)
# file.close()

# log.info("finished")
#
# time.sleep(100000)
k12_bot = K12Bot(config=config)
k12_bot.auth()
k12_bot.auto_select_test()
try:
    k12_bot.complete_test()
finally:
    time.sleep(1000000)
