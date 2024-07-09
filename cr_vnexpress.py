import pandas as pd
import numpy as np
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime

# Initialize Chrome WebDriver
service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open the specified webpage
driver.get('https://vnexpress.net/bat-dong-san/du-an/search?offset=0&limit=100&')
sleep(5)  # Wait for the page to load initially

# Function to scroll down gradually
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
elems = driver.find_elements(By.CSS_SELECTOR, '.content h3 a')
title = [elem.text for elem in elems]
links = [elem.get_attribute('href') for elem in elems]

# Find elements with product details
name_duans = driver.find_elements(By.CSS_SELECTOR, '.content .des')
name_duan = [elem.text for elem in name_duans]

types = driver.find_elements(By.CSS_SELECTOR, '.content .checked')
type = [elem.text for elem in types]

prices = driver.find_elements(By.CSS_SELECTOR, '.content .price')
price = [elem.text for elem in prices]

address = driver.find_elements(By.CSS_SELECTOR, '.content .address')
add = [elem.text for elem in address]

# Create a DataFrame with the scraped data
df1 = pd.DataFrame(list(zip(title, name_duan, type, price, add, links)), columns=['Tên dự án', 'Chủ đầu tư', 'Loại', 'Giá', 'Địa chỉ', 'Link'])
df1['index_'] = np.arange(1, len(df1) + 1)

# Print the DataFrame to check the data
print(df1)

current_date = datetime.now().strftime("%Y%m%d")
# Save the DataFrame to an Excel file
excel_file_path = f'{current_date}_vnexpress.xlsx'
df1.to_excel(excel_file_path, index=False, engine='openpyxl')

print(f"Data has been saved to {excel_file_path}")

# Close the browser
driver.quit()
