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
driver.get('https://thesaigontimes.vn/dia-oc/')
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
elems = driver.find_elements(By.CSS_SELECTOR, '.td_block_inner .td-module-meta-info h3 a')
title = [elem.text for elem in elems]
links = [elem.get_attribute('href') for elem in elems]


# Create a DataFrame with the scraped data
df = pd.DataFrame(list(zip(title, links)), columns=['Tiêu đề','Link'])

# Create a new column in the DataFrame to store the detailed content
df['Tags'] = ''
df['Ngày'] = ''

num_rows = len(df)
# Thay đổi số trang web chi tiết ở đây
max_rows = 3 if num_rows > 3 else num_rows

# Iterate through each row in the DataFrame
for index, row in df.head(max_rows).iterrows():
    link = row['Link']
    driver.get(link)
    
    # Wait a bit for the page to load
    time.sleep(random.uniform(2, 4))

    try:
        elements_with_tags = driver.find_elements(By.CSS_SELECTOR, '.tdb_single_tags ul li a')

        # Initialize an empty list to store tag texts
        a_texts = []

        # Iterate through each element found by the XPath
        for element in elements_with_tags:
            # Get text from the <span> tag
            text = element.text.strip()
            if text:  # Only add if text is not empty
                a_texts.append(text)

        # Save text of the <span> tags to the 'Tags' column, each text separated by a comma
        df.at[index, 'Tags'] = ', '.join(a_texts)

        date_element = driver.find_element(By.CSS_SELECTOR, 'time.entry-date.updated.td-module-date')

        # Extract the datetime attribute value
        date_value = date_element.get_attribute('datetime')
        
        
        # Assign the extracted values to the 'Ngày' column in the DataFrame
        df.at[index, 'Ngày'] = date_value if date_value else 'N/A'


        # Get detailed content from the page
        paragraphs  = driver.find_elements(By.CSS_SELECTOR, '.tdb_single_content p')
        detailed_content = ""

        # Get text from all <p> tags
        for p in paragraphs:
            # Check if the <p> tag is not within a footer tag or has a 'footer' class
            if not (
                "footer" in p.get_attribute('class') or  # Check 'footer' class
                any(ancestor.tag_name == 'footer' for ancestor in p.find_elements(By.XPATH, "./ancestor::footer"))  # Check if within <footer> tag
            ):
                detailed_content += p.text + "\n"
        
        # Save this text to the DataFrame
        df.at[index, 'Content'] = detailed_content.strip()

        print(f"Link từ thẻ chứa 'tags' trong {link}:")
        for a_text in a_texts:
            print(a_text)

    except Exception as e:
        print(f"Không thể lấy dữ liệu từ {link}: {e}")

# Close the browser
driver.quit()

# Generate current date in YYYYMMDD format
current_date = datetime.now().strftime("%Y%m%d")

# Specify the Excel file path with current date added
excel_file_path = f'{current_date}_saigon_with_content.xlsx'
df.to_excel(excel_file_path, index=False, engine='openpyxl')

print(f"Data has been saved to {excel_file_path}")

# py cr_content_saigon.py
