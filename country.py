# -*- coding: utf-8 -*
import sys

import requests
from bs4 import BeautifulSoup


def get_top_twenty_sites(country):
    try:
        html_doc = requests.get(f"https://www.alexa.com/topsites/countries/{country}").content
        soup = BeautifulSoup(html_doc, 'html.parser')
        table = soup.find('div', {'class': 'listings table'})
        children = table.findChildren("a")
        for child in children[1: 21]:
            print(child.text)
    except AttributeError:
        print('請輸入正確的國家縮寫！')


def main(arg):
    get_top_twenty_sites(arg)


if __name__ == "__main__":
    main(sys.argv[1])
