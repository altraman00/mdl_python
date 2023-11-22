import json
import os

import html2text
import requests
from bs4 import BeautifulSoup


def download_image(url, save_path):
    response = requests.get(url, stream=True, verify=False)
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=128):
            f.write(chunk)


def process_html(article_name, html_content, output_directory):
    soup = BeautifulSoup(html_content, 'html.parser')

    div_to_remove = soup.find('div', class_='book-sidebar')
    if div_to_remove:
        div_to_remove.extract()

    # Convert HTML to Markdown using html2text
    markdown_content = html2text.html2text(str(soup))

    pic_output_directory = output_directory + "/assets"
    if not os.path.exists(pic_output_directory):
        os.makedirs(pic_output_directory)

    # Download images and update image URLs in Markdown
    base_url = 'https://47.110.81.206:10000/%E4%B8%93%E6%A0%8F/%E9%AB%98%E5%B9%B6%E5%8F%91%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A140%E9%97%AE'
    for img_tag in soup.find_all('img'):
        img_src = img_tag.get('src')
        if img_src:
            img_url = img_src if img_src.startswith('http') else f"{base_url}/{img_src}"
            img_filename = os.path.basename(img_url)

            img_path = os.path.join(pic_output_directory, img_filename)
            print('img_url===>', img_url)
            print('img_path===>', img_path)
            # Download the image
            download_image(img_url, img_path)

            # Update the image URL in the Markdown content
            # markdown_content = markdown_content.replace(img_src, img_filename)

    # Save Markdown content to a file
    markdown_file_path = os.path.join(output_directory, article_name + '.md')
    with open(markdown_file_path, 'w', encoding='utf-8') as markdown_file:
        markdown_file.write(markdown_content)

    print(f"Markdown file saved at: {markdown_file_path}")


# ===============


base_url = 'https://47.110.81.206:10000/%E4%B8%93%E6%A0%8F/%E9%AB%98%E5%B9%B6%E5%8F%91%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A140%E9%97%AE/'
r = requests.get(base_url, verify=False)
soup = BeautifulSoup(r.content, 'html.parser')

output_directory = '/Users/zunker/Desktop/高并发系统设计/py2'  # Replace with the desired output directory

li_list = soup.find_all('li')
result_map = {}
for li in li_list:
    article_name = li.find('a').text
    li_href = li.find('a')['href']
    result_map[article_name] = li_href
    article_url = base_url + li_href
    r = requests.get(article_url, verify=False)
    article_name = article_name.replace('.md.html', '')
    process_html(article_name, r.content, output_directory)

# print(result_map)
print(json.dumps(result_map, ensure_ascii=False))
