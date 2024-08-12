import pyautogui
import pyperclip
import time
import openpyxl

# Tạo Workbook mới để lưu dữ liệu
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Messages"

# Chờ trang tải
time.sleep(5)

# Tọa độ ban đầu
initial_x = 350  # Tọa độ x ban đầu
initial_y = 550  # Tọa độ y ban đầu

# Tọa độ để di chuyển con trỏ sau khi click
move_to_x = 700  # Tọa độ x để di chuyển con trỏ
move_to_y = 550  # Tọa độ y để di chuyển con trỏ

# Xác định khoảng cách cuộn xuống
scroll_distance = -95  # Cuộn xuống 95 "đơn vị"

# Biến để lưu trữ nội dung tin nhắn trước đó
previous_text = ""

# Lặp lại cho đến khi không còn tin nhắn nào
while True:
    # Click vào đoạn tin nhắn hiện tại
    pyautogui.click(x=initial_x, y=initial_y)
    
    # Chờ để đảm bảo đoạn tin nhắn được chọn
    time.sleep(3)

    # Di chuyển con trỏ đến vị trí khác trước khi sao chép
    pyautogui.moveTo(x=move_to_x, y=move_to_y)
    
    # Chờ thêm một chút nếu cần
    time.sleep(1)
    
    # Click chuột trái sau khi di chuyển con trỏ
    pyautogui.click()
    
    # Sao chép nội dung bằng Ctrl+A và Ctrl+C
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'c')
    
    # Lấy văn bản từ clipboard
    current_text = pyperclip.paste()
    
    # Kiểm tra nếu không còn dữ liệu mới, hoặc nếu dữ liệu trùng khớp với lần trước, thoát vòng lặp
    if not current_text or current_text == previous_text:
        print("No new messages or duplicate messages detected. Stopping.")
        break
    
    # Ghi dữ liệu vào Excel
    for index, line in enumerate(current_text.split('\n'), start=ws.max_row + 1):
        ws[f"A{index}"] = line
    
    # Lưu nội dung tin nhắn hiện tại để so sánh trong lần lặp tiếp theo
    previous_text = current_text
    
    # Di chuyển con trỏ trở lại vị trí ban đầu
    pyautogui.moveTo(x=initial_x, y=initial_y)
    
    # Cuộn xuống để chuyển đến đoạn tin nhắn tiếp theo
    pyautogui.scroll(scroll_distance)
    
    # Chờ để giao diện cuộn xong
    time.sleep(2)

# Lưu file Excel
wb.save("messages.xlsx")

print("Data has been saved to messages.xlsx")
