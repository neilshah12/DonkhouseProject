import re
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


download_x_ratios = {
    '0.01/0.02': 178 / 847,
    '0.1/0.2': 170 / 847,
    '0.25/0.5': 174 / 847,
    '0.5/1': 162 / 847,
    '1/2': 153 / 847,
    '1/3': 153 / 847,
    '2/4': 153 / 847,
    '2/5': 153 / 847,
    '3/5': 153 / 847,
    '3/6': 153 / 847,
    '4/8': 153 / 847
}


def click_downloads(driver, link, stakes):
    driver.get(link)

    wait = WebDriverWait(driver, 10)
    canvas_locator = (By.TAG_NAME, 'canvas')
    wait.until(EC.presence_of_element_located(canvas_locator))

    canvas = driver.find_element(By.TAG_NAME, 'canvas')
    style = canvas.get_attribute('style')
    canvas_width = float(re.search(r"width:\s*([\d.]+)px", style).group(1))
    canvas_height = float(re.search(r"height:\s*([\d.]+)px", style).group(1))

    time.sleep(5)
    # Calculate button position within the canvas
    download_x_ratio = download_x_ratios[stakes]
    download_y_ratio = 40 / 529.375

    hand_histories_ratio = 1 / 23

    download_x = round((download_x_ratio - 0.5) * canvas_width)
    download_y = round((download_y_ratio - 0.5) * canvas_height)

    print(canvas_height)

    action_chains = ActionChains(driver)
    action_chains.move_to_element_with_offset(canvas, download_x, download_y).click().perform()
    time.sleep(1)
    action_chains.move_to_element_with_offset(canvas, 0, 0).click().perform()
    time.sleep(0.5)
    action_chains.move_to_element_with_offset(canvas, 0, canvas_height * hand_histories_ratio).click().perform()
    time.sleep(1)


def download_logs():
    current_dir= os.getcwd()
    download_dir = os.path.join(current_dir, 'logs')
    prefs = {'download.default_directory': download_dir}


    chrome_options = Options()
    chrome_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
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

    time.sleep(1)
    driver.get('https://donkhouse.com/group/34524')

    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    forms = soup.find(class_='columns').find_all('form')

    for form in forms:
        div_list = list(form.find_all(class_='column is-one-fifth is-marginless'))
        if len(div_list) < 2:
            continue
        elif not re.match(r'(\s+)NLH(\s+)', div_list[0].text):
            continue
        else:
            stakes = div_list[1].text.strip()
            href = form.find(class_='panel-block has-text-white')['href']
            click_downloads(driver, 'https://donkhouse.com' + href, stakes)


try:
    download_logs()
except Exception as exc:
    print(exc)
