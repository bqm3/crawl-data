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
driver.get('https://www.24h.com.vn/kinh-doanh-c161.html')
random.randint(3, 5)  # Wait for the page to load initially

# Function to scroll down gradually
try:
    # Wait up to 10 seconds for the button to be present
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.cate-24h-foot-home-tour-news-readmore a'))
    )
    button.click()   
    random.randint(2, 3)
    button.click()
    random.randint(2, 3)
    button.click()
    random.randint(2, 3)
    button.click()
    random.randint(2, 3)
except TimeoutException:
    print("Button not found or not clickable within the given time")
    driver.quit()

# Find elements with product titles and links
elems = driver.find_elements(By.CSS_SELECTOR, '.cate-24h-foot-home-latest-list__name a')
title = [elem.text for elem in elems]
links = [elem.get_attribute('href') for elem in elems]

# Find elements with product details
contents = driver.find_elements(By.CSS_SELECTOR, '.cate-24h-foot-home-latest-list__sum')
content = [elem.text for elem in contents]


dates = driver.find_elements(By.CSS_SELECTOR, '.cate-24h-foot-home-latest-list__time')
date = [elem.text for elem in dates]

# Create a DataFrame with the scraped data
df = pd.DataFrame(list(zip(title, content, date, links)), columns=['Tiêu đề', 'Tóm tắt', 'Ngày', 'Link'])
df['index_'] = np.arange(1, len(df) + 1)

# Print the DataFrame to check the data
print(df)

# Generate current date in YYYYMMDD format
current_date = datetime.now().strftime("%Y%m%d")

# Specify the Excel file path with current date added
excel_file_path = f'excel_24h_{current_date}.xlsx'
df.to_excel(excel_file_path, index=False, engine='openpyxl')

print(f"Data has been saved to {excel_file_path}")

# Close the browser
driver.quit()

# py cr_24h.py