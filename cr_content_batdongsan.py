import pandas as pd
import numpy as np
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime

# Initialize Chrome WebDriver
# options = Options()
# options.add_argument(r"user-data-dir=C:\Users\minhd\AppData\Local\Google\Chrome\User Data")  # Path to your user profile
# options.add_argument(r"profile-directory=Default")  # Specific profile directory
# options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
# options.add_argument("--disable-web-security")  # Disable web security
# options.add_argument("--allow-running-insecure-content")  # Allow running insecure content
# options.add_argument("--headless")  # Run Chrome in headless mode
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")



service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open the specified webpage
driver.get('https://batdongsan.com.vn/tin-tuc')
time.sleep(random.uniform(3, 5))  # Wait for the page to load initially

def scroll_down():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(2)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Call the function to scroll down gradually
scroll_down()

# Find elements with product titles and links
elems = driver.find_elements(By.CSS_SELECTOR, '.ArticleCardLarge_articleWrapper___8Xih .ArticleCardLarge_articleContent__E_bBy h3 a')
title = [elem.text for elem in elems]
links = [elem.get_attribute('href') for elem in elems]

# Create a DataFrame with the scraped data
df = pd.DataFrame(list(zip(title, links)), columns=['Tiêu đề', 'Link'])

# Create a new column in the DataFrame to store the detailed content
df['Nội dung'] = ''
df['Tags'] = ''
df['Ngày'] = ''

# Iterate through each row in the DataFrame to get content from the links
num_rows = len(df)
# Iterate through each row in the DataFrame to get content from the links
max_rows = 10 if num_rows > 10 else num_rows

# Iterate through each row in the DataFrame
for index, row in df.head(max_rows).iterrows():
    link = row['Link']
    driver.get(link)
    
    # Wait a bit for the page to load
    time.sleep(random.uniform(2, 4))

    try:
        elements_with_tags = driver.find_elements(By.XPATH, "//*[contains(@class, 'tags')]")
        
        # Get <a> tags from the elements containing 'tags'
        a_texts = []
        for element in elements_with_tags:
            a_tags = element.find_elements(By.TAG_NAME, 'a')
            for a in a_tags:
                text = a.text.strip()
                if text:  # Only add if text is not empty
                    a_texts.append(text)
        
        # Save text of the <a> tags to the 'Tags' column, each text separated by a comma
        df.at[index, 'Tags'] = ', '.join(a_texts)

        times  = driver.find_elements(By.CSS_SELECTOR, '.AuthorInfo_authorInfo__zo8Rq .AuthorInfo_postDate__WnkLz')

        df.at[index, 'Ngày'] = times


        # Get detailed content from the page
        paragraphs  = driver.find_elements(By.CSS_SELECTOR, '.content-wrapper .p')
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
excel_file_path = f'{current_date}_batdongsan_with_content.xlsx'
df.to_excel(excel_file_path, index=False, engine='openpyxl')

print(f"Data has been saved to {excel_file_path}")
