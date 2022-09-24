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

log.basicConfig(stream=sys.stdout, level=log.INFO)

log.info("set up webdriver")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
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
driver.find_element(By.CLASS_NAME, "select2-results__option").click()
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
time.sleep(1)

# Screenshot and save tkb
log.info("taking screenshot")
tkb = driver.find_element(By.ID, "printTableHS").screenshot_as_png
with open("tkb.png", "wb") as f:
    f.write(tkb)

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
