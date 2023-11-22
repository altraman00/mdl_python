import json

import requests
from bs4 import BeautifulSoup

url = 'https://47.110.81.206:10000/%E4%B8%93%E6%A0%8F/%E9%AB%98%E5%B9%B6%E5%8F%91%E7%B3%BB%E7%BB%9F%E8%AE%BE%E8%AE%A140%E9%97%AE/'
r = requests.get(url, verify=False)
print(r.status_code)
html_content = r.content

soup = BeautifulSoup(html_content, 'html.parser')
# print(soup.text)

result_map = {}

li_list = soup.find_all('li')

for li in li_list:
    # Extract href from the li
    article_name = li.find('a').text
    li_href = li.find('a')['href']
    result_map[article_name] = li_href

# print(result_map)
print(json.dumps(result_map, ensure_ascii=False))
