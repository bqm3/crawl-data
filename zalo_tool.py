from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pyautogui
import time
import pyperclip


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
driver = webdriver.Chrome(options=chrome_options)

time.sleep(5)

pyautogui.click(x=300, y=500)

time.sleep(3)
pyautogui.moveTo(x=700, y=600)
time.sleep(1)
pyautogui.hotkey('ctrl', 'a')  
time.sleep(0.5) 
pyautogui.hotkey('ctrl', 'c') 

text = pyperclip.paste()

print("Copied text:", text)
driver.quit()
