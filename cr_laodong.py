import pandas as pd
import random
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Chrome WebDriver
service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open the specified webpage
base_url = 'https://laodong.vn/bat-dong-san?page='
num_pages = 2  # Number of pages to scrape
all_data = []

try:
    for page_num in range(1, num_pages + 1):
        # Construct the URL for each page
        url = f"{base_url}{page_num}"
        
        # Open the webpage
        driver.get(url)
        sleep(random.uniform(3, 5))  # Random sleep to mimic human behavior
        
        # Find elements with product titles and links
        elems = driver.find_elements(By.CSS_SELECTOR, '.link-title h2')
        titles = [elem.text for elem in elems]

        linkhrefs = driver.find_elements(By.CSS_SELECTOR, '.link-title')
        links = [elem.get_attribute('href') for elem in linkhrefs]

        # Find elements with product details
        datess = driver.find_elements(By.CSS_SELECTOR, 'article.p2c.m002 .info .time')
        dates = [elem.text for elem in datess]

        contentss = driver.find_elements(By.CSS_SELECTOR, 'article.p2c.m002 .chapeau')
        contents = [elem.text for elem in contentss]

        # # Find elements with times
        # types = driver.find_elements(By.CSS_SELECTOR, '.horizontalPost__main-cate  a')
        # typecates = [elem.text for elem in types]

        # Append data to the list
        for title, summary, date, link in zip(titles, contents, dates, links):
            all_data.append({
                'Tiêu đề': title,
                'Tóm tắt': summary,
                'Ngày': date,
                'Link': link
            })

except Exception as e:
    print(f"Error scraping page {page_num}: {str(e)}")

finally:
   
    # Create a DataFrame from the scraped data
    df = pd.DataFrame(all_data)

    # Generate current date in YYYYMMDD format
    current_date = datetime.now().strftime("%Y%m%d")

    # Specify the Excel file path with current date added
    excel_file_path = f'{current_date}_laodong.xlsx'

    # Save the DataFrame to the Excel file
    df.to_excel(excel_file_path, index=False, engine='openpyxl')

    print(f"Data has been saved to {excel_file_path}")
    # Close the browser
    driver.quit()

# py cr_laodong.py