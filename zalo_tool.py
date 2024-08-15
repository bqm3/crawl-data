import pyautogui as pag
import pyperclip
import time
import openpyxl
import pandas as pd
import pyscreeze
import datetime

# Tạo Workbook mới để lưu dữ liệu
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Messages"

# Chờ trang tải
time.sleep(5)

# Tọa độ ban đầu
initial_x = 300  # Tọa độ x ban đầu
initial_y = 315  # Tọa độ y ban đầu

# Tọa độ để di chuyển con trỏ sau khi click
move_to_x = 1150  # Tọa độ x để di chuyển con trỏ
move_to_y = 315  # Tọa độ y để di chuyển con trỏ

# Tọa độ các điểm click bổ sung
click_x = 630  # Tọa độ x đầu tiên sau khi click vào tin nhắn
click_y = 180  # Tọa độ y đầu tiên sau khi click vào tin nhắn

click2_x = 950  # Tọa độ x thứ hai sau khi click vào tin nhắn
click2_y = 670  # Tọa độ y thứ hai sau khi click vào tin nhắn

click3_x = 1000  # Tọa độ x cuối cùng sau khi sao chép tin nhắn
click3_y = 735  # Tọa độ y cuối cùng sau khi sao chép tin nhắn

# Xác định khoảng cách cuộn xuống
scroll_distance = -66  # Cuộn xuống 66 "đơn vị"

# Biến để lưu trữ nội dung tin nhắn trước đó
previous_text = ""

# Biến để theo dõi số lần cuộn thất bại
scroll_failures = 0

# Danh sách để lưu trữ dữ liệu
titles = []
messages = []

# Lặp lại cho đến khi không còn tin nhắn nào
while True:
    # Click vào đoạn tin nhắn hiện tại
    pag.click(x=initial_x, y=initial_y)
    
    # Chờ để đảm bảo đoạn tin nhắn được chọn
    time.sleep(0.5)

    # Di chuyển và click vào vị trí bổ sung thứ nhất
    pag.moveTo(x=click_x, y=click_y)
    time.sleep(0.5)
    try:
        x, y = pyscreeze.locateCenterOnScreen("edit.png", grayscale=True, confidence=0.5)
        pag.click(x, y)
    except TypeError:
        print("Hình ảnh 'edit.png' không tìm thấy.")
        break
    
    time.sleep(0.5)
    # Di chuyển và click vào vị trí bổ sung thứ hai
    pag.moveTo(x=click2_x, y=click2_y)
    pag.click()
    time.sleep(1)

    # Sao chép nội dung đầu tiên bằng Ctrl+A và Ctrl+C (Tên nhóm)
    pag.hotkey('ctrl', 'a')
    time.sleep(1)
    pag.hotkey('ctrl', 'c')
    
    # Lấy văn bản từ clipboard
    group_name = pyperclip.paste()
    titles.append(group_name)
    pag.click()
    # Di chuyển và click vào vị trí bổ sung thứ ba
    pag.moveTo(x=click3_x, y=click3_y)
    pag.click()

    # Di chuyển con trỏ đến vị trí khác trước khi sao chép nội dung tin nhắn
    pag.moveTo(x=535, y=886)
    pag.click()
    pag.hotkey('ctrl', 'a')
    # Cuộn tin nhắn lên cho đến khi không thể cuộn thêm được nữa
    while True:
        time.sleep(1)
        previous_position = pag.position()
        pag.scroll(1000)
        pag.hotkey('ctrl', 'a')
        time.sleep(1)
        pag.scroll(1000)
        pag.hotkey('ctrl', 'a')
        time.sleep(1)
        pag.scroll(1000)
        pag.hotkey('ctrl', 'a')
        time.sleep(1)
        pag.scroll(1000)
        pag.hotkey('ctrl', 'a')
        time.sleep(1)
        pag.hotkey('ctrl', 'c')
        
        # Kiểm tra nếu cuộn thất bại
        if pag.position() == previous_position:
            break
    
    # Sau khi cuộn hết, thực hiện sao chép nội dung tin nhắn
    
    time.sleep(1)
    pag.hotkey('ctrl', 'c')
    
    # Lấy văn bản từ clipboard
    message_text = pyperclip.paste()
    messages.append(message_text)
    
    # Kiểm tra nếu không còn dữ liệu mới hoặc nếu dữ liệu trùng khớp với lần trước
    if not message_text or message_text == previous_text:
        print("No new messages or duplicate messages detected. Stopping.")
        break
    
    # Lưu nội dung tin nhắn hiện tại để so sánh trong lần lặp tiếp theo
    previous_text = message_text
    
    # Di chuyển con trỏ trở lại vị trí ban đầu
    pag.moveTo(x=initial_x, y=initial_y)
    
    # Cố gắng cuộn xuống để chuyển đến đoạn tin nhắn tiếp theo
    pag.scroll(scroll_distance)
    
    # Chờ để giao diện cuộn xong
    time.sleep(2)
    
    # Kiểm tra nếu cuộn thất bại
    if pag.position() == (initial_x, initial_y):
        scroll_failures += 1
    else:
        scroll_failures = 0  # Đặt lại số lần thất bại nếu cuộn thành công
    
    # Nếu cuộn thất bại 3 lần liên tiếp, tăng tọa độ y và thử lại
    if scroll_failures >= 3:
        initial_y += 100  # Tăng tọa độ y lên 100 đơn vị
        move_to_y = initial_y  # Cập nhật tọa độ y mới cho move_to

        # Nếu y vượt quá một giới hạn nhất định, thoát vòng lặp
        if initial_y > 1000:  # Điều chỉnh giới hạn này tùy thuộc vào giao diện của bạn
            print("Reached maximum scroll position. Stopping.")
            break

        scroll_failures = 0  # Đặt lại số lần thất bại sau khi thay đổi y

# Tạo DataFrame từ danh sách đã lưu
df = pd.DataFrame({
    'Tên nhóm': titles,
    'Messages': messages
})

current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f"messages_{current_time}.xlsx"

# Lưu DataFrame vào file Excel với tên file động
df.to_excel(file_name, index=False)

print(f"Data has been saved to {file_name}")
