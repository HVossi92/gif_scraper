# Website: https://videoplasty.com/stock-gifs/search?category=other&page=1

import re

import requests
from bs4 import BeautifulSoup as bS

# Local download directory
download_dir = '/Users/h.vosskamp/Downloads/'
# Limit the maximum number of downloads per URL. None = download everything
maxDownloads = 10000
total_downloads = 0

def scrape(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    num_downloads = 0
    gif_container_html_txt = requests.get(url, headers=headers).text
    container_soup = bS(gif_container_html_txt, 'lxml')
    elements = container_soup.find_all("img", src=re.compile("gif"))

    for i, element in enumerate(elements):
        print(f'Download {i + 1} / {len(elements)}')
        gif_url = element['src']
        request = requests.get(gif_url, headers=headers)

        last_slash = gif_url.rfind('/')
        file_name = gif_url[last_slash + 1:-4]
        print(f"Status code: {request.status_code}; Headers: {request.headers['content-type']}; "
              f"Encoding: {request.encoding}; File name: {file_name}")

        with open(download_dir + file_name + '.gif', 'wb') as f:
            f.write(request.content)

        if maxDownloads is not None and i >= maxDownloads - 1:
            break


if __name__ == '__main__':
    # websites to be scraped
    base_url = 'https://support.skype.com/en/faq/FA12330/what-is-the-full-list-of-emoticons'
    # categories = ['other']
    scrape(base_url)
    print("Done")
