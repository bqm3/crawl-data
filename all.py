from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import pandas as pd

service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Đọc file Excel
df = pd.read_excel('./excel_dantri_20240627.xlsx')
# Tạo cột mới trong dataframe để lưu nội dung chi tiết
df['Nội dung'] = ''

# Lặp qua từng dòng trong file Excel để lấy nội dung từ các link
for index, row in df.iterrows():
    link = row['Link']
    driver.get(link)
    
    # Chờ một chút cho trang tải
    time.sleep(random.uniform(3, 4))

    try:
        elements_with_tags = driver.find_elements(By.XPATH, "//*[contains(@class, 'tags')]")
        
        # Lấy các thẻ <a> từ các thẻ chứa 'tags'
        a_texts = []
        for element in elements_with_tags:
            a_tags = element.find_elements(By.TAG_NAME, 'a')
            for a in a_tags:
                text = a.text.strip()
                if text:  # Chỉ thêm nếu text không rỗng
                    a_texts.append(text)
        
        # Lưu text của các thẻ <a> vào cột 'Tags', mỗi text cách nhau bởi dấu phẩy
        df.at[index, 'Tags'] = ', '.join(a_texts)


        # Lấy nội dung chi tiết từ trang
        # Cập nhật các bước này để phù hợp với cấu trúc trang web bạn cần lấy dữ liệu
        paragraphs  = driver.find_elements(By.TAG_NAME, 'p')
        detailed_content = ""

        # Lấy văn bản từ tất cả các thẻ <p>
        for p in paragraphs:
            # Kiểm tra nếu thẻ <p> không nằm trong thẻ footer hoặc có class 'footer'
            if not (
                "footer" in p.get_attribute('class') or  # Kiểm tra class 'footer'
                any(ancestor.tag_name == 'footer' for ancestor in p.find_elements(By.XPATH, "./ancestor::footer"))  # Kiểm tra nếu nằm trong thẻ <footer>
            ):
                detailed_content += p.text + "\n"
        
        # Lưu văn bản này vào dataframe
        df.at[index, 'Content'] = detailed_content.strip()

        print(f"Link từ thẻ chứa 'tags' trong {link}:")
        for a_text in a_texts:
            print(a_text)

    except Exception as e:
        print(f"Không thể lấy dữ liệu từ {link}: {e}")

# Đóng trình duyệt
driver.quit()

# Ghi dữ liệu vào file Excel
df.to_excel('./excel_soha_content.xlsx', index=False)
