import requests
from bs4 import BeautifulSoup as bs
import csv

def get_html(url):
    response = requests.get(url)
    return response.text


def get_content(html):
    soup = bs(html, 'lxml')
    cars = soup.find_all('div', class_ = 'list-item list-label')
    for car in cars:
        try:
            name = car.find('h2', class_ = 'name').text.strip()
        except:
            name = ''
        try:
            price = car.find('p', class_ = 'price').text.strip().replace(' ', '').replace("\n", " ")
        except:
            price = ''
        try:
            image = car.find('img', class_ = 'lazy-image').get('data-src').strip()
        except:
            image = 'Image not found :('
        try:
            description = car.find('div', class_ = 'item-info-wrapper').text.strip().replace('\n', ' ').replace(' ', '')
        except:
            description = ''
        
        data = {
                'name': name,
                'price': price,
                'image': image,
                'description': description
        }
        write_csv(data)



def write_csv(data):
    with open('automobiles.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter = '/')
        writer.writerow(
            (
                data['name'],
                data['price'],
                data['image'],
                data['description']
            )
        )


def main():
    for page in range(1,1275):
        print(f'Парсинг {page} страницы...')
        url = f'https://www.mashina.kg/search/all/?page={page}'
        html = get_html(url)
        get_content(html)
        page += 1
main()
