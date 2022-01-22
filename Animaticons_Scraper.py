# Website: https://animaticons.co/downloads/

import re

import requests
from bs4 import BeautifulSoup as bS

# Local download directory
download_dir = '/Users/h.vosskamp/Downloads/'
# Limit the maximum number of downloads per URL. None = download everything
maxDownloads = None


def scrape(input_url, j):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }

    html_txt = requests.get(input_url, headers=headers).text
    soup = bS(html_txt, 'lxml')
    elements = soup.find_all('li', {'style': re.compile(r'gif')})

    str(elements[0])
    pattern = re.compile(r"(?<=').*\.gif")

    max_iters = len(elements) if maxDownloads is None else maxDownloads

    for i, element in enumerate(elements):
        input_url = re.search(pattern, str(element)).group()
        print(f'Download {i + 1} / {max_iters} from: {j} {input_url}')

        request = requests.get(input_url, headers=headers)

        last_slash = input_url.rfind('/')
        file_name = input_url[last_slash + 1:-4]
        print(f"Status code: {request.status_code}; Headers: {request.headers['content-type']}; "
              f"Encoding: {request.encoding}; File name: {file_name}")

        with open(download_dir + file_name + '.gif', 'wb') as f:
            f.write(request.content)

        if maxDownloads is not None and i >= maxDownloads - 1:
            break


if __name__ == '__main__':
    # websites to be scraped
    baseUrls = ['https://animaticons.co/downloads/animaticons-essential-3/',
                'https://animaticons.co/downloads/animaticons-designer/',
                'https://animaticons.co/downloads/essential-plus/',
                'https://animaticons.co/downloads/essential/',
                'https://animaticons.co/downloads/animaticons-camp/']
    for j, url in enumerate(baseUrls):
        print(f'Scraping URL {j + 1} / {len(baseUrls)}. {url}')
        scrape(url, j + 1)

    print(" ")
    print("Done")
