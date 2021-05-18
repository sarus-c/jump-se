from bs4 import BeautifulSoup
import requests
import threading


class Scraper:
    def __init__(self, urls):
        self.urls = urls
        self.items = []
        self.scrap()

    def get_content(self, url):
        sk = url.split('##')
        html_text = requests.get(sk[0]).text
        soup = BeautifulSoup(html_text, 'lxml')
        prices = soup.findAll('div', class_='card-section-wrapper js-section-wrapper', limit=3)

        for index, price in enumerate(prices):
            try:
                img = price.find('div', class_='thumbnail').find('img').get('src')
                title_a = price.find('a', class_='product-title js-product-url')
                title = title_a.text.replace('\n', '')
                url = title_a.get('href')
                price_p = price.find('p', class_='product-new-price').contents
                price = price_p[0] + "," + price_p[1].string + " " + price_p[3].string
                item = {
                    'search_id': sk[1],
                    'title': title.strip(),
                    'url': url,
                    'img': img,
                    'price': price
                }

                self.items.append(item)

            except IndexError:
                pass

    def scrap(self):
        t_list = []
        for url in self.urls:
            t = threading.Thread(target=self.get_content, args=[url])
            t.start()
            t_list.append(t)

        for t_item in t_list:
            t_item.join()
