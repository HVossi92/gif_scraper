# Website: https://videoplasty.com/stock-gifs/search?category=other&page=1

import re

import requests
from bs4 import BeautifulSoup as bS

# Local download directory
download_dir = '/Users/h.vosskamp/Downloads/'
# Limit the maximum number of downloads per URL. None = download everything
maxDownloads = 10000
total_downloads = 0

def scrape(base_url, j):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    num_downloads = 0
    page_counter = 0
    while True:
        print(f"Current page: {page_counter}")
        category_page_url = base_url + '&page=' + str(page_counter)
        page_counter += 1

        category_page_html_txt = requests.get(category_page_url, headers=headers).text
        category_soup = bS(category_page_html_txt, 'lxml')

        # elements = soup.find_all('li', {'style': re.compile(r'gif')})
        category_elements = category_soup.find_all("a", {"class": "jsx-2951254995 jsx-398815260"})

        if len(category_elements) < 1:
            print(f"No more pages. Page: {page_counter}, URL: {category_page_url}")
            break

        max_iters = len(category_elements) if maxDownloads is None else maxDownloads
        for i, element in enumerate(category_elements):
            gif_container_page = 'https://videoplasty.com' + str(element.get("href"))
            print(f'Download {i + 1} / {max_iters} from: {j} {gif_container_page}')

            gif_container_html_txt = requests.get(gif_container_page, headers=headers).text
            container_soup = bS(gif_container_html_txt, 'lxml')
            container_element = container_soup.find_all("img", src=re.compile("gif"))

            if len(container_element) < 1 or container_element[0].get("src") is None:
                continue

            gif_url = container_element[0].get("src")
            gif_request = requests.get(gif_url, headers=headers)
            # gif_soup = bS(gif_html_txt, 'lxml')
            # gif_elements = gif_soup.find("img", {"class": "jsx-3723502854 jsx-2526214781"})

            last_slash = gif_container_page.rfind('/')
            file_name = gif_container_page[last_slash + 1:-4]

            try:
                print(f"Status code: {gif_request.status_code}; Headers: {gif_request.headers['content-type']}; "
                      f"Encoding: {gif_request.encoding}; File name: {file_name}")
            except Exception as e:
                print(f'Could not print status. {e}')

            try:
                with open(download_dir + file_name + '.gif', 'wb') as f:
                    f.write(gif_request.content)
                num_downloads += 1
            except Exception as e:
                print(f'Could not write file. {e}')

            if maxDownloads is not None and i >= maxDownloads - 1:
                break

    return num_downloads


if __name__ == '__main__':
    # websites to be scraped
    base_url = 'https://videoplasty.com/stock-gifs/search?category='
    categories = ['characters']
    #categories = ['icons', 'characters']
    #categories = ['other']
    total_downloads = 0

    for j, category in enumerate(categories):
        print("")
        print(f"=========> Scraping category {category} {j + 1} / {len(categories)}. {base_url + category}")
        print("")
        total_downloads += scrape(base_url + category, j + 1)

    print(" ")
    print(f"Total downloads: {total_downloads}")
    print("Done")
