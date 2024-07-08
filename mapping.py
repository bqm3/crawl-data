import pandas as pd

# Đường dẫn tới file Excel chứa từ khóa
keywords_file_path = './Book2.xlsx'
# Đường dẫn tới file Excel chứa nội dung cần kiểm tra
content_file_path = 'excel_soha_content.xlsx'

# Đọc file Excel chứa từ khóa
sheets_dict = pd.read_excel(keywords_file_path, sheet_name=None)

# Hiển thị tên các sheet
print("Sheets trong file Excel chứa từ khóa:", sheets_dict.keys())

# Đọc file Excel chứa nội dung cần kiểm tra
content_df = pd.read_excel(content_file_path)

# Tạo dataframe để lưu kết quả
results = []

# Lặp qua từng dòng nội dung
for idx, row in content_df.iterrows():
    content_text = row['Content']  # Thay 'Detailed Content' bằng tên cột thực tế chứa nội dung
    matching_keywords = []
    matching_labels = []

    # Duyệt qua từng sheet chứa từ khóa
    for sheet_name, sheet_df in sheets_dict.items():
        keywords = sheet_df['keyword'].dropna().tolist()  # Thay 'keyword' bằng tên cột chứa từ khóa
        labels = sheet_df['Nhãn'].dropna().tolist()  # Thay 'Nhãn' bằng tên cột chứa nhãn

        # Kiểm tra từ khóa trong nội dung
        for keyword, label in zip(keywords, labels):
            if keyword.lower() in content_text.lower():  # So sánh không phân biệt hoa thường
                matching_keywords.append(keyword)
                matching_labels.append(label)
    
    # Thêm kết quả vào dataframe
    result = {
        'Content': content_text, 
        'Matching Keywords': ', '.join(matching_keywords), 
        'Matching Labels': ', '.join(matching_labels)
    }
    
    # Thêm từ điển vào danh sách kết quả
    results.append(result)

results_df = pd.DataFrame(results)
# Lưu kết quả vào file Excel
results_df.to_excel('excel_mapping.xlsx', index=False)

print("Đã lưu kết quả vào file excel_mapping.xlsx")
