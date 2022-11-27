from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import subprocess
import shutil
from PIL import Image
from pathlib import Path
import logging as log
import sys
import os

log.basicConfig(filename="logs.log", level=log.INFO)


def write_file(path: str, content: str):
    file = open(path, "w+")
    file.write(content)
    file.close()


def read_file(path: str, not_exist_default="1") -> str:
    if os.path.isfile(path):
        file = open(path, "r")
        content = file.read()
        file.close()
        return content
    file = open(path, "w+")
    file.write(not_exist_default)
    file.close()
    return not_exist_default


log.info("set up webdriver")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--hide-scrollbars")
driver = webdriver.Chrome(
    options=chrome_options,
    service=ChromeService(executable_path=ChromeDriverManager().install()),
)

driver.get(
    "https://vietschool.vn/thoikhoabieu/tracuuthoikhoabieu/00109e78-0000-0000-0000-000000000000/139"
)

# Select `Hoc sinh`
log.info("clicking on `Hoc Sinh`")
driver.find_element("link text", "Học sinh").click()

# handle class
class_name = "12A1"
log.info(f"finding class {class_name}")
driver.find_element(By.ID, "select2-cbo_lop-container").click()
class_list = driver.find_element(By.ID, "select2-cbo_lop-results")
class_list.find_element("xpath", f"//li[text()='{class_name}']").click()
time.sleep(1)

# handle tkb
log.info("finding newest tkb")
driver.find_element(By.ID, "select2-cbo_tkbhs-container").click()
tkb_name = driver.find_element(By.CLASS_NAME, "select2-results__option")
if tkb_name.get_attribute("innerText") == read_file("old.txt"):
    print("still using old time table")
time.sleep(1)

# Styling before screenshot
log.info("styling")
driver.execute_script(
    """
document.getElementById("printTableHS").style.fontSize = "200%";
document.getElementById("printTableHS").style.padding = "0px 0px 0px 0px";
window.scrollBy(0, 200);
"""
)
time.sleep(2)

# Screenshot and save tkb
log.info("taking screenshot")
tkb = driver.find_element(By.ID, "printTableHS").screenshot_as_png
with open("tkb.png", "wb") as f:
    f.write(tkb)
write_file("old.txt", tkb_name.get_attribute("innerText"))

# stretch  image
log.info("stretch image")
tkb = Image.open("tkb.png")
tkb = tkb.resize((1000, 1000))
tkb.save("tkb.png")


# copy to mega and update background
log.info("update mega and dwm image")
subprocess.run(["mega-put", "tkb.png", "/"])
shutil.copyfile("tkb.png", f"{str(Path.home())}/.dwm/backgrounds/tkb.png")

log.info("done")

driver.quit()
