from bs4 import BeautifulSoup as bS
import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

html_txt = requests.get('https://animaticons.co/downloads/animaticons-camp/', headers=headers).text
soup = bS(html_txt, 'lxml')
elements = soup.find_all('li', {'style': re.compile(r'gif')})

ele_0 = str(elements[0])
pattern = re.compile(r"(?<=').*\.gif")

for i, element in enumerate(elements):
    url = re.search(pattern, str(element)).group()
    print('Download ' + str(i) + " / " + str(len(elements)) + 'from: ' + url)

    r = requests.get(url, headers=headers)
    # Retrieve HTTP meta-data
    print("Status code: " + str(r.status_code) + "; Headers: " + r.headers['content-type'] + "; Encoding: " + r.encoding)

    with open('/home/vossi/Downloads/file_' + str(i) + '.gif', 'wb') as f:
        f.write(r.content)
