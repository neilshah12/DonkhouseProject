import pyautogui
import webbrowser
import time

# Open donk
url = "https://donkhouse.com/group/34524/90342"
webbrowser.open(url)

# Allow webpage to open fully (better to use Selenium webdriver)
time.sleep(3)

# Download coordinates on a 14-inch Macbook
download_x = 530
download_y = 270

# Move the mouse to the download and click
pyautogui.moveTo(download_x, download_y)
pyautogui.click()

# Transaction log coordinates on a 14-inch Macbook
transaction_x = 900
transaction_y = 650

# Move the mouse to transaction log and click
pyautogui.moveTo(transaction_x, transaction_y)
pyautogui.click()