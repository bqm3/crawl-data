import pandas as pd
import numpy as np
from time import sleep
import random
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Initialize Chrome WebDriver
service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open the specified webpage
driver.get('https://cafef.vn/bat-dong-san.chn')
random.randint(3, 5)  # Wait for the page to load initially

def scroll_down():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        sleep(2)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Call the function to scroll down gradually
scroll_down()


# Find elements with product titles and links
elems = driver.find_elements(By.CSS_SELECTOR, '.list-main .top5_news h3 a')
title = [elem.text for elem in elems]
links = [elem.get_attribute('href') for elem in elems]

print(elems)

# Find elements with product details
contents = driver.find_elements(By.CSS_SELECTOR, '.list-main .top5_news .sapo')
content = [elem.text for elem in contents]


# Create a DataFrame with the scraped data
df = pd.DataFrame(list(zip(title, content, links)), columns=['Tiêu đề', 'Tóm tắt', 'Link'])

# Print the DataFrame to check the data
print(df)

# Generate current date in YYYYMMDD format
current_date = datetime.now().strftime("%Y%m%d")

# Specify the Excel file path with current date added
excel_file_path = f'{current_date}_cafe.xlsx'
df.to_excel(excel_file_path, index=False, engine='openpyxl')

print(f"Data has been saved to {excel_file_path}")

# Close the browser
driver.quit()

# py cr_blogrever.py