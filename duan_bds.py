import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import random

# Function to scroll down the page
def scroll_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(1, 3))  # Random sleep to mimic human behavior
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Function to extract data from each project card
def extract_data_from_card(card):
    row_data = {}

    # Extract project name
    try:
        row_data['Tên dự án'] = card.find_element(By.CSS_SELECTOR, '.re__prj-card-info h3').text
    except:
        row_data['Tên dự án'] = None

    # Extract project status (Tình trạng)
    try:
        row_data['Tình trạng'] = card.find_element(By.CSS_SELECTOR, '.re__prj-card-info .re__prj-tag-info label').text
    except:
        row_data['Tình trạng'] = None

    # Extract data from .re__prj-card-config-value spans (Thông tin 1, 2, 3)
    elements = card.find_elements(By.CSS_SELECTOR, '.re__prj-card-config-value')
    for i, element in enumerate(elements):
        aria_label = element.get_attribute('aria-label')
        if aria_label:
            row_data[f'Thông tin {i+1}'] = aria_label
        else:
            span_text = element.find_element(By.TAG_NAME, 'span').text if element.find_elements(By.TAG_NAME, 'span') else element.text
            row_data[f'Thông tin {i+1}'] = span_text
    
    # Extract location
    try:
        row_data['Địa chỉ'] = card.find_element(By.CSS_SELECTOR, '.re__prj-card-location').text
    except:
        row_data['Địa chỉ'] = None

    # Extract summary
    try:
        row_data['Tóm tắt'] = card.find_element(By.CSS_SELECTOR, '.re__prj-card-summary').text
    except:
        row_data['Tóm tắt'] = None

    # Extract company
    try:
        row_data['Công ty'] = card.find_element(By.CSS_SELECTOR, '.re__prj-card-contact span').text
    except:
        row_data['Công ty'] = None

    return row_data

# Initialize an empty list to store all data
all_data = []

#======================================================
# Vòng lặp để lấy dữ liệu 
for page_num in range(1, 3):
#====================================================

    service = Service(executable_path="./chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    url = f'https://batdongsan.com.vn/du-an-bat-dong-san/p{page_num}'
    driver.get(url)
    
    scroll_down(driver)
    
    # Find all project cards
    project_cards = driver.find_elements(By.CSS_SELECTOR, '.js__project-card')
    
    # Extract data for each card
    for card in project_cards:
        extracted_data = extract_data_from_card(card)
        all_data.append(extracted_data)
    
    # Close the browser after each page
    driver.quit()
    
    # Sleep a bit before opening a new browser
    time.sleep(random.randint(1, 2))

# Convert to DataFrame
df = pd.DataFrame(all_data)

# Save data to Excel
current_date = time.strftime("%Y%m%d%H%M")
excel_file_path = f'{current_date}_duan_bds.xlsx'
df.to_excel(excel_file_path, index=False, engine='openpyxl')

print(f"Data has been saved to {excel_file_path}")
