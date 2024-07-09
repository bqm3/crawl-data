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
driver.get('https://blog.rever.vn/du-an')
random.randint(3, 5)  # Wait for the page to load initially

# Function to scroll down gradually
try:
    # Wait up to 10 seconds for the button to be present
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/main/div[4]/div/div/div[1]/div[2]/button'))
    )
    button.click()   
    random.randint(2, 3)
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
elems = driver.find_elements(By.CSS_SELECTOR, '.card-content a')
title = [elem.text for elem in elems]
links = [elem.get_attribute('href') for elem in elems]

# Find elements with product details
contents = driver.find_elements(By.CSS_SELECTOR, '.card-text')
content = [elem.text for elem in contents]

types = driver.find_elements(By.CSS_SELECTOR, '.card-summary-list a')
type = [elem.text for elem in types]

dates = driver.find_elements(By.CSS_SELECTOR, '.card-summary-list-item:nth-child(2)')
date = [elem.text for elem in dates]

# Create a DataFrame with the scraped data
df = pd.DataFrame(list(zip(title, content, type, date, links)), columns=['Tiêu đề', 'Tóm tắt', 'Loại', 'Ngày', 'Link'])
df['index_'] = np.arange(1, len(df) + 1)

# Print the DataFrame to check the data
print(df)

# Generate current date in YYYYMMDD format
current_date = datetime.now().strftime("%Y%m%d")

# Specify the Excel file path with current date added
excel_file_path = f'{current_date}_blogrever.xlsx'
df.to_excel(excel_file_path, index=False, engine='openpyxl')

print(f"Data has been saved to {excel_file_path}")

# Close the browser
driver.quit()

# py cr_blogrever.py