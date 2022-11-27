from selenium.webdriver.remote.webelement import WebElement
from seleniumwire import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging as log
import sys
import time
import yaml
import gzip
from ansparser import parse
import os

import logging as log


class BotDriver:
    mobile_emulation = {
        "deviceMetrics": {"width": 1366, "height": 786, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
    }
    cwd = os.getcwd()

    def __init__(self, browser: str):
        self.browser = browser
        log.info(f"setting up {browser}")
        if browser == "chrome":
            self.setup_chrome()
        else:
            self.setup_firefox()

    def setup_chrome(self):
        options = webdriver.ChromeOptions()
        options.add_extension(f"{self.cwd}/extensions/always-active-ext.crx")
        options.add_experimental_option("mobileEmulation", self.mobile_emulation)
        self.driver = webdriver.Chrome(
            options=options,
            service=ChromeService(executable_path=ChromeDriverManager().install()),
        )

    def setup_firefox(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", self.mobile_emulation)
        profile.add_extension(f"{self.cwd}/extensions/always-active-ext.xpi")
        self.driver = webdriver.Firefox(
            profile=profile,
            executable_path=GeckoDriverManager().install(),
        )

    def fullpage_screenshot(self, path: str = "/tmp"):
        """
        Only work with firefox driver
        """
        if self.browser == "firefox":
            self.driver.save_full_page_screenshot(path)  # type: ignore
        else:
            log.error("can not take fullpage screenshot with chrome")

    def text_input(self, name: str, input: str):
        log.info(f"inputting {input}, with name {name}")
        self.driver.find_element("xpath", f"//input[@placeholder='{name}']").send_keys(
            input
        )

    def click_contains(self, type: str, text: str):
        log.info(f"clicking on {text} (type {type})")
        time.sleep(0.1)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//{type}[contains(text(), '{text}')]")
            )
        ).click()

    def check_exists_by_xpath(self, xpath) -> tuple[bool, None | WebElement]:
        time.sleep(1)
        try:
            element = self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return (False, None)
        return (True, element)

    def click_after_appearance(self, xpath: str):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        ).click()
