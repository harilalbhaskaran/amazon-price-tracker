import requests
from bs4 import BeautifulSoup
import logging
import logging.handlers
import sys
from fake_useragent import UserAgent


URL = 'https://www.amazon.in/Fujifilm-X-T4-Mirrorless-XF16-80mm-Touchscreen/dp/B08557SY7B/'

proxies = {'http': str(sys.argv[1]), 'https': str(sys.argv[1]), }

ua = UserAgent()
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-IN,en;q=0.9,ml;q=0.8',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-ch-viewport-width': '1920',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'service-worker-navigation-preload': 'true',
    'upgrade-insecure-requests': '1',
    'user-agent': ua.random,
}


def analyze_price(logger):
    app = requests.get(URL, headers=headers, proxies=proxies)
    scrapper = BeautifulSoup(app.content, 'html.parser')
    # print(scrapper.prettify())
    price_whole = scrapper.find("span", {"class": "a-price-whole"}).text
    productTitle = scrapper.find(
        "span", {"id": "productTitle"}).text.strip()[:62]
    float_price = float(price_whole[0:8].replace(',', ''))
    logger.info(productTitle + " - " + str(int(float_price)))
    # print(str(int(float_price)))


def main():

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger_file_handler = logging.handlers.RotatingFileHandler(
        "status.log",
        maxBytes=1024 * 1024,
        backupCount=1,
        encoding="utf8",
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger_file_handler.setFormatter(formatter)
    logger.addHandler(logger_file_handler)

    analyze_price(logger)


if __name__ == "__main__":
    main()
