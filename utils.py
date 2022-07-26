import threading
import requests
from bs4 import BeautifulSoup

# Getting first pages from OLX
for i in range(1, 3):
    websites = []
    websites.append(
        f'https://www.olx.ua/d/uk/detskiy-mir/detskaya-odezhda/?page={i}')


class Scraper(threading.Thread):
    """ Parsing threads class"""

    def __init__(self, threadId, name, url):
        threading.Thread.__init__(self)
        self.name = name
        self.id = threadId
        self.url = url

    def run(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'html.parser')
        results = []

        for item in soup.select('div[data-cy="l-card"]'):
            image = item.find('img')
            results.append(
                {
                    'title': item.h6.get_text(strip=True),
                    'price': item.p.get_text(strip=True),
                    'image': image['src'],
                }
            )
        return results


for url in websites:
    thread = Scraper(1, "thread"+str(i), url)
    result_dict = thread.run()
