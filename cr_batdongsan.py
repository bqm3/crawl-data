import json
import pandas as pd

# Load the JSON data from the file
with open('./databds.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract the required information and store it in a list of dictionaries
articles_data = []
base_url = "https://batdongsan.com.vn/tin-tuc"
for article in data:
    article_info = {
        'title': article.get('title'),
        'excerpt': article.get('excerpt'),
        'link': base_url+article.get('link'),
        'location': article.get('location'),
        'postDate': article.get('postDate'),
    }
    categories = article.get('category', [])
    if categories is None:
        categories = []
    category_names = [cat.get('name') for cat in categories]
    article_info['category_names'] = ', '.join(category_names) if category_names else None
    
    # Extract all tag names, handle if tags is None or empty
    tags = article.get('tags', [])
    if tags is None:
        tags = []
    tag_names = [tag.get('name') for tag in tags]
    article_info['tag_names'] = ', '.join(tag_names) if tag_names else None
    
    # Extract the sponsor name
    sponsor = article.get('sponsor', {})
    sponsor_name = sponsor.get('name', '')
    article_info['sponsor_name'] = sponsor_name

    articles_data.append(article_info)

# Convert the list of dictionaries into a pandas DataFrame
df = pd.DataFrame(articles_data)

# Save the DataFrame to an Excel file
excel_file_path = 'excel_bds.xlsx'  # Specify your desired file name and path
df.to_excel(excel_file_path, index=False, engine='openpyxl')


print("Data has been saved to 'articles_data.xlsx'.")
