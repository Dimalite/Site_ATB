import requests
from bs4 import BeautifulSoup
import csv  # module for save
import os

URL = 'https://www.atbmarket.com/ru/promo/akciya-ekonomiya'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
    'accept': '*/*'}
FILE = 'products.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='modal fade')
    # print(len(items))

    pds = []
    for item in items:
        pds.append({
            'product': item.find('div', class_='one-days-tit').get_text(strip=True),
            'price': item.find('div', class_='one-action-price-now').get_text(strip=True),
            'count': len(pds),

        })

    print(pds)

    # print(len(pds))
    save_file(pds, FILE)   # # вызов функции для сохранения
    return pds

# функция для сохранения
def save_file(items, path):
    with open(path, 'w', newline='') as file:  # open file for writing
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Товар', 'Цена в UAH', 'Кол-во'])
        for item in items:
            writer.writerow([item['product'], item['price'], item['count']])


def parse():
    # URL = input('Введите URL: ')
    # URL = URL.strip()
    html = get_html(URL)
    # save_file(pds, FILE)

    if html.status_code == 200:
        # print(html.text)  # 1) получил код страницы
        get_content(html.text)
        os.startfile(FILE)  #  Сохранение
    else:
        print("error")


parse()
