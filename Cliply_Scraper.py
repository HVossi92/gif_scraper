# Website: https://videoplasty.com/stock-gifs/search?category=other&page=1

import re

import requests
from bs4 import BeautifulSoup as bS

# Local download directory
download_dir = '/Users/h.vosskamp/Downloads/'
# Limit the maximum number of downloads per URL. None = download everything
maxDownloads = 10000
total_downloads = 0

def scrape(base_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    num_downloads = 0
    page_counter = 0
    while True:
        print(f"Current page: {page_counter}")
        category_page_url = base_url + str(page_counter)
        page_counter += 1

        category_page_html_txt = requests.get(category_page_url, headers=headers).text
        category_soup = bS(category_page_html_txt, 'lxml')

        # elements = soup.find_all('li', {'style': re.compile(r'gif')})
        category_elements = category_soup.find_all("img", src=re.compile("gif"))

        if len(category_elements) < 1:
            print(f"No more pages. Page: {page_counter}, URL: {category_page_url}")
            break

        max_iters = len(category_elements) if maxDownloads is None else maxDownloads
        for i, element in enumerate(category_elements):
            gif_container_page = str(element.get("src"))
            print(f'Download {i + 1} / {max_iters} from: {gif_container_page}')

            request = requests.get(gif_container_page, headers=headers)

            last_slash = gif_container_page.rfind('/')
            file_name = gif_container_page[last_slash + 1:-4]

            try:
                print(f"Status code: {request.status_code}; Headers: {request.headers['content-type']}; "
                      f"Encoding: {request.encoding}; File name: {file_name}")
            except Exception as e:
                print(f'Could not print status. {e}')

            try:
                with open(download_dir + file_name + '.gif', 'wb') as f:
                    f.write(request.content)
                num_downloads += 1
            except Exception as e:
                print(f'Could not write file. {e}')

            if maxDownloads is not None and i >= maxDownloads - 1:
                break

    return num_downloads


if __name__ == '__main__':
    # websites to be scraped
    base_url = 'https://cliply.co/browse/page/'

    scrape(base_url)

    print(" ")
    print(f"Total downloads: {total_downloads}")
    print("Done")
