import requests
from bs4 import BeautifulSoup as bs

import errors

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/83.0.4103.116 Safari/537.36'}
HOST = 'https://belok.ua'


class ParsBelok:

    url = 'https://belok.ua/{keyword}/'

    def __init__(self, pages=1):

        if pages == 0:
            raise AttributeError('Attribute pages cant be zero')
        else:
            self.pages = pages

    def get_html(self, keyword, params=None):

        self.url = self.url.format(keyword=keyword)
        response = requests.get(self.url, headers=HEADERS, params=params)

        if not response.status_code == 200:
            raise errors.Not200StatusCode(f'Status code is {response.status_code}')
        return response.text

    @staticmethod
    def block_content(html):
        soup = bs(html, 'html.parser')
        block_content = soup.find('div', class_='cat_products row').find_all('div', class_='product')
        return block_content

    def __parse_content(self, html):
        block = self.block_content(html)
        content = []
        for item in block:
            price_old = item.find('span', class_='price-old')
            price_new = item.find('span', class_='price-new')
            if price_old and price_new:
                price_old = price_old.get_text(strip=True)
                price = int(price_new.get_text().split()[0])
                price_new = price_new.get_text(strip=True)
                if price < 500:
                    content.append(
                        {
                            'title': item.find('div', class_='caption').find_next('a').text,
                            'link': item.find('a').get('href'),
                            'price_new': price_new,
                            'price_old': price_old,
                        }
                    )
        return content

    def parse(self, keyword):
        content = []
        for page in range(1, self.pages + 1):
            html = self.get_html(keyword=keyword, params={'?page=': page})
            content.extend(self.__parse_content(html))
        return content