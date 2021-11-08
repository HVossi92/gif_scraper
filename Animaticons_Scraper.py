# Website: https://animaticons.co/downloads/animaticons-camp/

import re

import requests
from bs4 import BeautifulSoup as bS

# website to be scraped
baseUrl = 'https://animaticons.co/downloads/animaticons-camp/'
# Local download directory
download_dir = '/home/vossi/Downloads/'
# Limit the maximum number of downloads. None = download everything
maxDownloads = None


def scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }

    html_txt = requests.get(baseUrl, headers=headers).text
    soup = bS(html_txt, 'lxml')
    elements = soup.find_all('li', {'style': re.compile(r'gif')})

    str(elements[0])
    pattern = re.compile(r"(?<=').*\.gif")

    max_iters = len(elements) if maxDownloads is None else maxDownloads

    for i, element in enumerate(elements):
        url = re.search(pattern, str(element)).group()
        print(f'Download {i + 1} / {max_iters} from: {url}')

        request = requests.get(url, headers=headers)

        last_slash = url.rfind('/')
        file_name = url[last_slash + 1:-4]
        print(f"Status code: {request.status_code}; Headers: {request.headers['content-type']}; "
              f"Encoding: {request.encoding}; File name: {file_name}")

        with open(download_dir + file_name + '.gif', 'wb') as f:
            f.write(request.content)

        if maxDownloads is not None and i >= maxDownloads - 1:
            break


if __name__ == '__main__':
    scrape()
