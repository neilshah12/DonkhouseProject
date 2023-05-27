import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get('https://donkhouse.com/login')


username_placeholder = 'Your Username'
password_placeholder = 'Your Password'
username_field = driver.find_element(By.XPATH, "//input[@placeholder='" + username_placeholder + "']")
password_field = driver.find_element(By.XPATH, "//input[@placeholder='" + password_placeholder + "']")

username_field.send_keys('project-test')
password_field.send_keys('project-test')

buttons = driver.find_elements(By.TAG_NAME, 'button')
for button in buttons:
    if button.text == 'Go!':
        button.click()
        break

time.sleep(2)
driver.get('https://donkhouse.com/group/34524/93022')
wait = WebDriverWait(driver, 10)
canvas_locator = (By.TAG_NAME, 'canvas')
wait.until(EC.presence_of_element_located(canvas_locator))
time.sleep(10)


canvas = driver.find_element(By.TAG_NAME, 'canvas')
canvas_width = canvas.rect['width']
canvas_height = canvas.rect['height']

DOWNLOAD_X_RATIO = 42/800
DOWNLOAD_Y_RATIO = 34/500


download_x_offset = round(DOWNLOAD_X_RATIO * canvas_width - canvas_width / 2) 
download_y_offset = round(DOWNLOAD_Y_RATIO * canvas_height - canvas_height / 2)

print(download_x_offset)
print(download_y_offset)

action_chains = ActionChains(driver)
action_chains.move_to_element_with_offset(canvas, download_x_offset, download_y_offset).click().perform()

time.sleep(1000)