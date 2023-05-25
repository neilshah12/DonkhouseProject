import re, time, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

current_dir= os.getcwd()
download_dir = os.path.join(current_dir, 'logs')
prefs = {'download.default_directory': download_dir}

chrome_options = Options()
chrome_options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
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

canvas = driver.find_element(By.TAG_NAME, 'canvas')
style = canvas.get_attribute('style')
canvas_width = float(re.search(r"width:\s*([\d.]+)px", style).group(1))
canvas_height = float(re.search(r"height:\s*([\d.]+)px", style).group(1))

time.sleep(5)
# Calculate button position within the canvas
DOWNLOAD_X_RATIO = 178/847
DOWNLOAD_Y_RATIO = 40/529.375
download_x = round((DOWNLOAD_X_RATIO - 0.5) * canvas_width)
download_y = round((DOWNLOAD_Y_RATIO - 0.5) * canvas_height)

action_chains = ActionChains(driver)
action_chains.move_to_element_with_offset(canvas, download_x, download_y).click().perform()
time.sleep(1)
action_chains.move_to_element_with_offset(canvas, 0, 0).click().perform()
time.sleep(5)