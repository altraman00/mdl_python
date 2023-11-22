import os

import html2text
import requests
from bs4 import BeautifulSoup


# url = 'https://47.110.81.206:10000/%E4%B8%93%E6%A0%8F/%E9%AB%98%E5%B9%B6%E5%8F%91%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A140%E9%97%AE/'
# r = requests.get(url, verify=False)
# soup = BeautifulSoup(r.content, 'html.parser')
#
# li_list = soup.find_all('li')
# result_map = {}
# for li in li_list:
#     # Extract href from the li
#     article_name = li.find('a').text
#     li_href = li.find('a')['href']
#     result_map[article_name] = li_href
#
# # print(result_map)
# print(json.dumps(result_map, ensure_ascii=False))


# ===============

def download_image(url, save_path):
    response = requests.get(url, stream=True, verify=False)
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=128):
            f.write(chunk)


def process_html(html_content, output_directory):
    soup = BeautifulSoup(html_content, 'html.parser')

    div_to_remove = soup.find('div', class_='book-sidebar')
    if div_to_remove:
        div_to_remove.extract()

    # Convert HTML to Markdown using html2text
    markdown_content = html2text.html2text(str(soup))

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Download images and update image URLs in Markdown
    base_url = 'https://47.110.81.206:10000/%E4%B8%93%E6%A0%8F/%E9%AB%98%E5%B9%B6%E5%8F%91%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A140%E9%97%AE'
    for img_tag in soup.find_all('img'):
        img_src = img_tag.get('src')
        if img_src:
            img_url = img_src if img_src.startswith('http') else f"{base_url}/{img_src}"
            img_filename = os.path.basename(img_url)

            img_path = os.path.join(output_directory, img_filename)
            print('img_url===>', img_url)
            print('img_path===>', img_path)
            # Download the image
            download_image(img_url, img_path)

            # Update the image URL in the Markdown content
            markdown_content = markdown_content.replace(img_src, img_filename)

    # Save Markdown content to a file
    markdown_file_path = os.path.join(output_directory, 'output.md')
    with open(markdown_file_path, 'w', encoding='utf-8') as markdown_file:
        markdown_file.write(markdown_content)

    print(f"Markdown file saved at: {markdown_file_path}")


output_directory = '/Users/zunker/Desktop/高并发系统设计/py'  # Replace with the desired output directory

# url = 'https://47.110.81.206:10000/%E4%B8%93%E6%A0%8F/%E9%AB%98%E5%B9%B6%E5%8F%91%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A140%E9%97%AE/00%20%E5%BC%80%E7%AF%87%E8%AF%8D%20%20%E4%B8%BA%E4%BB%80%E4%B9%88%E4%BD%A0%E8%A6%81%E5%AD%A6%E4%B9%A0%E9%AB%98%E5%B9%B6%E5%8F%91%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A1%EF%BC%9F.md.html'
url = 'https://47.110.81.206:10000/%E4%B8%93%E6%A0%8F/%E9%AB%98%E5%B9%B6%E5%8F%91%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A140%E9%97%AE/01%20%20%E9%AB%98%E5%B9%B6%E5%8F%91%E7%B3%BB%E7%BB%9F%EF%BC%9A%E5%AE%83%E7%9A%84%E9%80%9A%E7%94%A8%E8%AE%BE%E8%AE%A1%E6%96%B9%E6%B3%95%E6%98%AF%E4%BB%80%E4%B9%88%EF%BC%9F.md.html'
r = requests.get(url, verify=False)
process_html(r.content, output_directory)
