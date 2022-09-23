import requests
from bs4 import BeautifulSoup
import logging
import logging.handlers
import os


URL = 'https://www.amazon.in/Fujifilm-X-T4-Mirrorless-XF16-80mm-Touchscreen/dp/B08557SY7B/'

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 9.10; rv:69.0) Gecko/20100101 Firefox/68.0'}


def analyze_price(logger):
    app = requests.get(URL, headers=headers)
    scrapper = BeautifulSoup(app.content, 'html.parser')

    print(scrapper.prettify())

    price_whole = scrapper.find("span", {"class": "a-price-whole"}).text
    productTitle = scrapper.find(
        "span", {"id": "productTitle"}).text.strip()[:62]
    float_price = float(price_whole[0:8].replace(',', ''))
    logger.info(productTitle + " - " + str(int(float_price)))   


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
