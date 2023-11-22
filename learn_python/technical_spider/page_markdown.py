import json

import requests
from bs4 import BeautifulSoup

url = 'https://47.110.81.206:10000/%E4%B8%93%E6%A0%8F/'
r = requests.get(url, verify=False)
print(r.status_code)
html_content = r.content

soup = BeautifulSoup(html_content, 'html.parser')
# print(soup.text)

result_map = {}

# Find all ul elements
ul_list = soup.find_all('ul')

for ul in ul_list:
    # Find all li elements under the ul
    li_list = ul.find_all('li')

    for li in li_list:
        # Extract href from the li
        li_href = li.find('a')['href']

        # Find the nested ul element under the li
        nested_ul = li.find('ul')

        if nested_ul:
            # Find all li elements under the nested ul
            nested_li_list = nested_ul.find_all('li')

            # Create a list to store nested values
            nested_values = []

            for nested_li in nested_li_list:
                # Extract href from the nested li
                nested_href = nested_li.find('a')['href']

                # Add nested values to the list
                nested_values.append(nested_href)

            # Add the li href as the key and the list of nested href as the value
            result_map[li_href] = nested_values
        else:
            # If there are no nested ul elements, add a single entry with the li href
            result_map[li_href] = []

# print(result_map)
print(json.dumps(result_map, ensure_ascii=False))
