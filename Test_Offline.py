from bs4 import BeautifulSoup as bS

with open('home.html', 'r') as html_file:
    content = html_file.read()
    soup = bS(content, 'lxml')
    cards = soup.find_all('div', class_='card')
    for course in cards:
        name = course.h5.text
        price = course.a.text.split()[-1]
        print(f'{name} costs {price}')
