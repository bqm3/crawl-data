import pandas as pd
import numpy as np
from time import sleep
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime

service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Thay đổi link website ở đây
driver.get('https://issuu.com/pmcweb.vn/stacks/58ed72871cc84e1f96eb493b1035d9d0')
sleep(random.randint(3, 5))  # Wait for the page to load initially

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
elems = driver.find_elements(By.CSS_SELECTOR, "h3[data-testid='publication-card-title']")
titles = [elem.text for elem in elems]

print(titles)

# Create a DataFrame with the scraped data
df = pd.DataFrame(list(zip(titles)), columns=['Tiêu đề'])
current_date = datetime.now().strftime("%Y%m%d")

# Specify the Excel file path with current date added
excel_file_path = f'{current_date}_data.xlsx'
df.to_excel(excel_file_path, index=False, engine='openpyxl')

print(f"Data has been saved to {excel_file_path}")


# Close the browser
driver.quit()
