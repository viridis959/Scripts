# -*- coding: utf-8 -*
import sys

import requests
from bs4 import BeautifulSoup


def get_top_num_sites(num):
    html_doc = requests.get('https://www.alexa.com/topsites').content
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = soup.find('div', {'class': 'listings table'})
    children = table.findChildren("a")
    for child in children[1: num + 1]:
        print(child.text)


def main(arg):
    get_top_num_sites(int(arg))


if __name__ == "__main__":
    main(sys.argv[1])
